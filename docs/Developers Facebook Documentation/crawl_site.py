"""
Recursive crawler: bir başlangıç URL'inden başlayarak aynı domain altındaki
sayfaları indirir, hepsini Markdown'a çevirir.

Kullanım:
    python crawl_site.py <START_URL> [--max 100] [--depth 3] [--out output/] \
                         [--include /docs/] [--concurrency 4]

Örnek:
    python crawl_site.py https://developers.facebook.com/docs/graph-api \
        --include /docs/graph-api --max 200 --concurrency 3
"""
import argparse
import asyncio
import json
import os
import re
import signal
import sys
from pathlib import Path
from urllib.parse import urljoin, urldefrag, urlparse

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser
from tqdm.asyncio import tqdm_asyncio

from scrape_page import (
    extract_meta_cms_links,
    html_to_markdown,
    output_path_for_url,
    title_for_output,
)

DEFAULT_TIMEOUT = 60_000
SIDEBAR_LINK_SELECTORS = [
    "a._3cx9[href]",  # Facebook for Developers docs sidebar
    "[aria-label*='documentation' i] a[href]",
    "[aria-label*='docs' i] a[href]",
    "nav a[href]",
    "aside a[href]",
]
CONTENT_SELECTORS_FOR_LINK_PRIORITY = [
    "#documentation_body_pagelet",
    "main",
    "article",
    "[role='main']",
    "#content",
    "#main",
]
DEFAULT_NO_DESCEND_KEYWORDS = ["changelog"]  # 'reference' kaldırıldı: features-reference gibi sayfaların altları takip edilmeli


def normalize(url: str) -> str:
    url, _ = urldefrag(url)
    return url.rstrip("/")


def same_host(url: str, root: str) -> bool:
    return urlparse(url).netloc == urlparse(root).netloc


def matches_filters(url: str, include: list[str], exclude: list[str]) -> bool:
    if include and not any(inc in url for inc in include):
        return False
    if exclude and any(exc in url for exc in exclude):
        return False
    return True


def should_descend(url: str, no_descend_keywords: list[str]) -> bool:
    return not any(keyword in url for keyword in no_descend_keywords)


def looks_like_error_page(title: str, html: str) -> bool:
    return (
        title.strip().lower() == "error"
        or "Sorry, something went wrong" in html
    )


async def fetch(browser: Browser, url: str, timeout: int) -> tuple[str, str] | None:
    """Tek sayfayı render et. (title, html) döndür."""
    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1280, "height": 900},
    )
    page = await context.new_page()
    try:
        last_result: tuple[str, str] | None = None
        for attempt in range(3):
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            try:
                await page.wait_for_load_state("networkidle", timeout=min(timeout, 10_000))
            except Exception:
                pass
            try:
                await page.wait_for_selector(
                    "#documentation_body_pagelet, main, article, [role='main']",
                    timeout=min(timeout, 10_000),
                )
            except Exception:
                pass
            try:
                await page.wait_for_function(
                    """() => {
                        const textLength = document.body?.innerText?.trim().length || 0;
                        const hasMetaCms = Array.from(
                            document.querySelectorAll('script[type="application/json"]')
                        ).some(script => script.textContent?.includes('json_cms_content'));
                        const isMetaDocs = location.hostname === 'developers.facebook.com'
                            && location.pathname.includes('/documentation/');
                        if (isMetaDocs) {
                            return hasMetaCms
                                || document.body?.innerText?.includes("This page isn't available right now");
                        }
                        return textLength > 500 || hasMetaCms;
                    }""",
                    timeout=min(timeout, 15_000),
                )
            except Exception:
                pass

            title = (await page.title()) or url
            html = await page.content()
            last_result = (title, html)
            if not looks_like_error_page(title, html):
                return title, html

            if attempt < 2:
                await asyncio.sleep(2)

        return last_result
    except Exception as exc:
        print(f"[!] Hata: {url} -> {exc}", file=sys.stderr)
        return None
    finally:
        await context.close()


def _clean_link(href: str, base_url: str) -> str | None:
    if href.startswith(("mailto:", "javascript:", "tel:")):
        return None
    return normalize(urljoin(base_url, href))


def _nav_anchors(soup: BeautifulSoup):
    seen = set()
    for selector in SIDEBAR_LINK_SELECTORS:
        for a in soup.select(selector):
            if id(a) not in seen:
                seen.add(id(a))
                yield a


def _link_text(anchor) -> str:
    text = anchor.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text) or anchor.get("href", "").strip()


def _nav_depth(anchor) -> int:
    list_depth = sum(1 for parent in anchor.parents if parent.name in {"ul", "ol"})
    return max(0, list_depth - 1)


def _json_script_payloads(soup: BeautifulSoup):
    for script in soup.select('script[type="application/json"]'):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            yield json.loads(raw)
        except json.JSONDecodeError:
            continue


def _find_meta_nav_trees(value):
    if isinstance(value, dict):
        nav = value.get("xfb_developer_doc_navigations")
        tree_list = nav.get("tree_list") if isinstance(nav, dict) else None
        if isinstance(tree_list, list):
            yield tree_list

        for child in value.values():
            yield from _find_meta_nav_trees(child)
    elif isinstance(value, list):
        for child in value:
            yield from _find_meta_nav_trees(child)


def _meta_nav_items_from_tree(tree_list: list[dict], base_url: str) -> list[tuple[int, str, str]]:
    by_id = {item.get("id"): item for item in tree_list if isinstance(item, dict)}
    child_ids = {
        child_id
        for item in tree_list
        if isinstance(item, dict)
        for child_id in item.get("children", [])
    }
    roots = [
        item
        for item in tree_list
        if isinstance(item, dict) and item.get("id") not in child_ids
    ]
    if not roots:
        roots = [item for item in tree_list if isinstance(item, dict)]

    out: list[tuple[int, str, str]] = []

    def walk(item: dict, depth: int) -> None:
        text = (item.get("text") or "").strip()
        href = item.get("href")
        if text and href:
            out.append((depth, text, normalize(urljoin(base_url, href))))
        for child_id in item.get("children", []):
            child = by_id.get(child_id)
            if child:
                walk(child, depth + 1)

    for root in roots:
        walk(root, 0)

    return out


def extract_meta_nav_items(html: str, base_url: str) -> list[tuple[int, str, str]]:
    soup = BeautifulSoup(html, "lxml")
    out: list[tuple[int, str, str]] = []
    seen: set[str] = set()

    for payload in _json_script_payloads(soup):
        for tree_list in _find_meta_nav_trees(payload):
            for depth, text, link in _meta_nav_items_from_tree(tree_list, base_url):
                if link not in seen:
                    seen.add(link)
                    out.append((depth, text, link))

    return out


def extract_nav_items(html: str, base_url: str) -> list[tuple[int, str, str]]:
    """Sidebar/nav menüsündeki linkleri, görünen sırayı koruyarak çıkar."""
    soup = BeautifulSoup(html, "lxml")
    out: list[tuple[int, str, str]] = []
    seen: set[str] = set()

    for a in _nav_anchors(soup):
        href = a.get("href")
        if not href:
            continue
        link = _clean_link(href, base_url)
        if link and link not in seen:
            seen.add(link)
            out.append((_nav_depth(a), _link_text(a), link))

    for depth, text, link in extract_meta_nav_items(html, base_url):
        if link not in seen:
            seen.add(link)
            out.append((depth, text, link))

    return out


def extract_links(html: str, base_url: str, nav_only: bool = False) -> list[str]:
    """Render edilmiş sayfadaki linkleri, sidebar linkleri önce gelecek şekilde çıkar."""
    soup = BeautifulSoup(html, "lxml")
    out: list[str] = []
    seen: set[str] = set()

    def add(href: str) -> None:
        link = _clean_link(href, base_url)
        if link and link not in seen:
            seen.add(link)
            out.append(link)

    for a in _nav_anchors(soup):
        href = a.get("href")
        if href:
            add(href)

    for _, _, link in extract_meta_nav_items(html, base_url):
        add(link)

    content_roots = soup.select(",".join(CONTENT_SELECTORS_FOR_LINK_PRIORITY))

    def is_inside_content(tag) -> bool:
        return any(root in tag.parents for root in content_roots)

    # Facebook docs gibi sitelerde aktif bölüme göre açılan sidebar linkleri
    # çoğunlukla ana içerik container'ının dışındadır; max limitlerinde bunları
    # gövde içi örnek/reference linklerinden önce kuyruğa almak gerekir.
    for a in soup.find_all("a", href=True):
        if not is_inside_content(a):
            add(a["href"])

    if nav_only:
        return out

    for a in soup.find_all("a", href=True):
        add(a["href"])

    for link in extract_meta_cms_links(html, base_url):
        add(link)

    return out


def record_nav_items(
    html: str,
    base_url: str,
    root: str,
    include: list[str],
    exclude: list[str],
    nav_items: list[tuple[int, str, str]],
    nav_seen: set[str],
) -> None:
    for depth, text, link in extract_nav_items(html, base_url):
        if (link not in nav_seen
                and same_host(link, root)
                and matches_filters(link, include, exclude)):
            nav_seen.add(link)
            nav_items.append((depth, text, link))


def write_sidebar_index(
    out_dir: Path,
    start_url: str,
    visited: set[str],
    nav_items: list[tuple[int, str, str]],
) -> Path:
    lines = [
        "# Sidebar Index",
        "",
        f"_Source: {start_url}_",
        "",
        "---",
        "",
        f"Downloaded pages: {len(visited)}",
        f"Discovered sidebar/nav links: {len(nav_items)}",
        "",
        "## Menu",
        "",
    ]

    for depth, text, link in nav_items:
        indent = "  " * depth
        label = text.replace("[", "\\[").replace("]", "\\]")
        if link in visited:
            target = os.path.relpath(output_path_for_url(out_dir, link), out_dir)
            target = Path(target).as_posix()
        else:
            target = link
            label = f"{label} (not downloaded)"
        lines.append(f"{indent}- [{label}]({target})")

    index_path = out_dir / "index.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return index_path


def _markdown_warnings(markdown: str) -> list[str]:
    warnings: list[str] = []
    stripped = markdown.strip()
    if len(stripped) < 500:
        warnings.append("short_content")
    if "|" not in markdown and re.search(r"(?m)^(Property|Parameter|Name|Key)\s*$", markdown):
        warnings.append("possible_flattened_table")
    if "```" not in markdown and re.search(r"(?m)^(curl -X|HTTP/\d|\{\s*$)", markdown):
        warnings.append("possible_unfenced_code")
    if not re.search(r"(?m)^##\s+", markdown) and len(stripped) > 1000:
        warnings.append("missing_section_headings")
    return warnings


def write_crawl_report(
    out_dir: Path,
    start_url: str,
    visited: set[str],
    queued: set[str],
    page_results: list[dict],
    max_pages: int,
) -> Path:
    downloaded = [item for item in page_results if item.get("status") == "ok"]
    failed = [item for item in page_results if item.get("status") != "ok"]
    warning_items = [item for item in downloaded if item.get("warnings")]
    pending = sorted(queued - visited)

    lines = [
        "# Crawl Report",
        "",
        f"_Source: {start_url}_",
        "",
        "---",
        "",
        f"Visited pages: {len(visited)}",
        f"Downloaded files: {len(downloaded)}",
        f"Failed pages: {len(failed)}",
        f"Queued but not visited: {len(pending)}",
        f"Max pages: {max_pages}",
        "",
    ]

    if warning_items:
        lines.extend(["## Warnings", ""])
        for item in warning_items:
            rel_path = os.path.relpath(item["path"], out_dir)
            rel_path = Path(rel_path).as_posix()
            warning_text = ", ".join(item["warnings"])
            lines.append(f"- [{item['title']}]({rel_path}) - {warning_text}")
        lines.append("")

    if failed:
        lines.extend(["## Failed Pages", ""])
        for item in failed:
            lines.append(f"- {item['url']} - {item.get('error', 'failed')}")
        lines.append("")

    if pending:
        lines.extend(["## Not Yet Visited", ""])
        for url in pending[:100]:
            lines.append(f"- {url}")
        if len(pending) > 100:
            lines.append(f"- ... and {len(pending) - 100} more")
        lines.append("")

    report_path = out_dir / "crawl_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return report_path


async def worker(
    name: int,
    browser: Browser,
    queue: asyncio.LifoQueue,
    visited: set[str],
    queued: set[str],
    out_dir: Path,
    root: str,
    include: list[str],
    exclude: list[str],
    max_depth: int,
    max_pages: int,
    timeout: int,
    sem: asyncio.Semaphore,
    pbar,
    content_selector: str | None = None,
    nav_only: bool = False,
    no_descend_keywords: list[str] | None = None,
    nav_items: list[tuple[int, str, str]] | None = None,
    nav_seen: set[str] | None = None,
    page_results: list[dict] | None = None,
) -> None:
    no_descend_keywords = no_descend_keywords or []
    nav_items = nav_items if nav_items is not None else []
    nav_seen = nav_seen if nav_seen is not None else set()
    page_results = page_results if page_results is not None else []
    while True:
        try:
            url, depth = await queue.get()
        except asyncio.CancelledError:
            return

        if url in visited or len(visited) >= max_pages:
            queue.task_done()
            continue
        visited.add(url)

        async with sem:
            result = await fetch(browser, url, timeout)
        if result is None:
            page_results.append({
                "url": url,
                "status": "failed",
                "error": "fetch_failed",
            })
            queue.task_done()
            pbar.update(1)
            continue

        title, html = result
        record_nav_items(html, url, root, include, exclude, nav_items, nav_seen)
        markdown = html_to_markdown(html, url, content_selector)
        title = title_for_output(title, markdown)
        out_path = output_path_for_url(out_dir, url)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            f"# {title}\n\n_Source: {url}_\n\n---\n\n{markdown}",
            encoding="utf-8",
        )
        page_results.append({
            "url": url,
            "title": title,
            "path": str(out_path),
            "status": "ok",
            "markdown_chars": len(markdown.strip()),
            "warnings": _markdown_warnings(markdown),
        })

        if depth < max_depth and should_descend(url, no_descend_keywords):
            for link in reversed(extract_links(html, url, nav_only)):
                if (link not in visited
                        and link not in queued
                        and same_host(link, root)
                        and matches_filters(link, include, exclude)):
                    queued.add(link)
                    await queue.put((link, depth + 1))

        pbar.update(1)
        queue.task_done()


async def crawl(
    start_url: str,
    out_dir: Path,
    max_pages: int = 100,
    max_depth: int = 3,
    concurrency: int = 4,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    content_selector: str | None = None,
    nav_only: bool = False,
    no_descend_keywords: list[str] | None = None,
    seed_urls: list[str] | None = None,
) -> int:
    include = include or []
    exclude = exclude or []
    no_descend_keywords = no_descend_keywords or DEFAULT_NO_DESCEND_KEYWORDS
    start_url = normalize(start_url)

    # Sidebar'larda aktif sayfa açıldıkça yeni alt linkler belirdiği için
    # LIFO kullanıyoruz: bir sayfaya girince onun açtığı alt bölümler,
    # eski sibling linklerden önce ziyaret edilir.
    queue: asyncio.LifoQueue = asyncio.LifoQueue()
    await queue.put((start_url, 0))
    visited: set[str] = set()
    queued: set[str] = {start_url}

    # --seed-url ile verilen ek URL'leri depth=0'dan kuyruğa ekle.
    # Bu URL'ler organik keşfe gerek kalmadan direkt indirilir;
    # --include filtresinden muaf tutulur (zaten bilinçli veriliyor).
    for _seed in seed_urls or []:
        _seed = normalize(_seed)
        if _seed not in queued:
            queued.add(_seed)
            await queue.put((_seed, 0))

    nav_items: list[tuple[int, str, str]] = []
    nav_seen: set[str] = set()
    page_results: list[dict] = []
    sem = asyncio.Semaphore(concurrency)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            with tqdm_asyncio(total=max_pages, desc="Crawling") as pbar:
                workers = [
                    asyncio.create_task(
                        worker(i, browser, queue, visited, queued, out_dir, start_url,
                               include, exclude, max_depth, max_pages, timeout, sem, pbar,
                               content_selector, nav_only, no_descend_keywords,
                               nav_items, nav_seen, page_results)
                    )
                    for i in range(concurrency)
                ]
                # queue boşalana kadar veya max_pages dolana kadar bekle
                try:
                    while not queue.empty() and len(visited) < max_pages:
                        await asyncio.sleep(0.5)
                    # Kalanları bitir
                    await queue.join()
                finally:
                    for w in workers:
                        w.cancel()
                    await asyncio.gather(*workers, return_exceptions=True)
                    await browser.close()
    finally:
        write_sidebar_index(out_dir, start_url, visited, nav_items)
        write_crawl_report(out_dir, start_url, visited, queued, page_results, max_pages)

    return len(visited)


def _raise_keyboard_interrupt(signum, frame) -> None:
    raise KeyboardInterrupt


def main() -> int:
    ap = argparse.ArgumentParser(description="Recursive site crawler -> Markdown")
    ap.add_argument("start_url", help="Başlangıç URL'i")
    ap.add_argument("--out", default="output", help="Çıktı klasörü")
    ap.add_argument("--max", type=int, default=100, help="Maks sayfa sayısı")
    ap.add_argument("--depth", type=int, default=3, help="Maks derinlik")
    ap.add_argument("--concurrency", type=int, default=4, help="Paralel worker sayısı")
    ap.add_argument("--include", action="append", default=[],
                    help="URL'de bulunması gereken substring (birden çok kez verilebilir)")
    ap.add_argument("--exclude", action="append", default=[],
                    help="URL'de bulunmaması gereken substring")
    ap.add_argument("--content", help="İçerik konteyner CSS seçicisi")
    ap.add_argument("--nav-only", action="store_true",
                    help="Sadece sidebar/nav linklerini takip et; gövde içi linkleri alma")
    ap.add_argument("--no-descend-keyword", action="append",
                    default=DEFAULT_NO_DESCEND_KEYWORDS.copy(),
                    help="URL bu kelimeyi içeriyorsa alt linkleri takip etme")
    ap.add_argument("--seed-url", action="append", default=[],
                    dest="seed_urls",
                    help=(
                        "Kuyruğa depth=0'dan eklenecek ek URL (birden çok kez verilebilir). "
                        "Dinamik sidebar nedeniyle organik keşfedilemeyen sayfalar için kullanın. "
                        "--include filtresinden muaftır."
                    ))
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = ap.parse_args()

    signal.signal(signal.SIGTERM, _raise_keyboard_interrupt)

    out_dir = Path(args.out)
    try:
        count = asyncio.run(crawl(
            start_url=args.start_url,
            out_dir=out_dir,
            max_pages=args.max,
            max_depth=args.depth,
            concurrency=args.concurrency,
            include=args.include,
            exclude=args.exclude,
            timeout=args.timeout,
            content_selector=args.content,
            nav_only=args.nav_only,
            no_descend_keywords=args.no_descend_keyword,
            seed_urls=args.seed_urls,
        ))
    except KeyboardInterrupt:
        print(f"\n[!] Durduruldu. Kısmi index ve rapor yazıldı: {out_dir}/")
        return 130
    print(f"\n✅ Tamamlandı: {count} sayfa -> {out_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
