"""
Single-page scraper: tek bir URL'i alır, JS render eder, temiz Markdown'a çevirir.

Kullanım:
    python scrape_page.py <URL> [-o output.md]

Örnek:
    python scrape_page.py https://developers.facebook.com/docs/graph-api -o graph-api.md
"""
import argparse
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.async_api import async_playwright

DEFAULT_TIMEOUT = 60_000
REMOVE_SELECTORS = [
    "nav", "header", "footer",
    '[role="banner"]', '[role="navigation"]', '[role="contentinfo"]',
    "script", "style", "noscript",
    ".cookie", "#cookie", "[class*='cookie' i]",
    "[aria-label*='breadcrumb' i]",
]


def slugify(url: str) -> str:
    path = urlparse(url).path.strip("/").replace("/", "-")
    return re.sub(r"[^a-zA-Z0-9._-]", "_", path) or "index"


def safe_path_part(value: str) -> str:
    value = unquote(value).strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("._-")
    return value or "index"


def output_path_for_url(base_dir: Path, url: str) -> Path:
    parts = [safe_path_part(part) for part in urlparse(url).path.split("/") if part]
    if not parts:
        return base_dir / "home.md"
    return base_dir / f"{'__'.join(parts)}.md"


def title_from_markdown(markdown: str) -> str | None:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", markdown)
    if not match:
        return None
    title = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", match.group(1)).strip()
    return title or None


def title_for_output(page_title: str, markdown: str) -> str:
    if page_title.strip() and page_title.strip() != "Developer Platform":
        return page_title
    return title_from_markdown(markdown) or page_title


def absolutize_links(soup: BeautifulSoup, base_url: str) -> None:
    for tag, attr in (("a", "href"), ("img", "src")):
        for el in soup.find_all(tag):
            val = el.get(attr)
            if val and not val.startswith(("http://", "https://", "data:", "mailto:", "#")):
                el[attr] = urljoin(base_url, val)


CONTENT_SELECTORS = [
    "#documentation_body_pagelet",  # Facebook for Developers
    "main",
    "article",
    "[role='main']",
    "#content",
    "#main",
    ".markdown-body",  # GitHub-flavored docs
]


def _json_script_payloads(soup: BeautifulSoup):
    for script in soup.select('script[type="application/json"]'):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            yield json.loads(raw)
        except json.JSONDecodeError:
            continue


def _find_json_cms_content(value):
    if isinstance(value, dict):
        raw_content = value.get("json_cms_content")
        if isinstance(raw_content, str):
            try:
                yield json.loads(raw_content)
            except json.JSONDecodeError:
                pass

        for child in value.values():
            yield from _find_json_cms_content(child)
    elif isinstance(value, list):
        for child in value:
            yield from _find_json_cms_content(child)


def _children(node: dict) -> list:
    children = node.get("children")
    if children is None:
        return []
    return children if isinstance(children, list) else [children]


def _clean_text(value: str) -> str:
    return re.sub(r"[ \t]+", " ", value.replace("\xa0", " ")).strip()


def _join_inline(parts: list[str]) -> str:
    return re.sub(r"[ \t]+", " ", "".join(parts)).strip()


def _render_cms_text(node, base_url: str) -> str:
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, (int, float)):
        return str(node)
    if isinstance(node, list):
        return "".join(_render_cms_text(child, base_url) for child in node)
    if not isinstance(node, dict):
        return ""

    component_type = node.get("type", "")
    props = node.get("props") or {}
    if component_type == "DeveloperLatestApiVersion":
        return props.get("latestApiVersion", "")

    return "".join(_render_cms_text(child, base_url) for child in _children(node))


def _render_cms_inline(node, base_url: str) -> str:
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, (int, float)):
        return str(node)
    if isinstance(node, list):
        return _join_inline([_render_cms_inline(child, base_url) for child in node])
    if not isinstance(node, dict):
        return ""

    component_type = node.get("type", "")
    props = node.get("props") or {}
    text = _join_inline([_render_cms_inline(child, base_url) for child in _children(node)])

    if component_type in {"DMCCommonA", "GalaxyHTMLA"}:
        href = props.get("href")
        if href and text:
            return f"[{text}]({urljoin(base_url, href)})"
        return text
    if component_type in {"GalaxyHTMLEm", "DMCCommonEm"}:
        return f"*{text}*" if text else ""
    if component_type in {"GalaxyHTMLStrong", "DMCCommonStrong"}:
        return f"**{text}**" if text else ""
    if component_type in {"GalaxyHTMLCode", "DMCCommonCode", "DeveloperCode"}:
        return f"`{text}`" if text else ""
    if component_type == "DeveloperLatestApiVersion":
        return props.get("latestApiVersion", "")
    if component_type in {"DEVHorizonImg", "DMCCommonImage", "img"}:
        src = props.get("src")
        if not src:
            return text
        alt = props.get("alt") or "Image"
        return f"![{alt}]({urljoin(base_url, src)})"

    return text


def _table_cell_text(node, base_url: str) -> str:
    parts = [
        _clean_text(_render_cms_inline(child, base_url))
        for child in _children(node)
    ]
    text = "<br>".join(part for part in parts if part)
    return text.replace("|", "\\|").replace("\n", "<br>")


def _list_item_text(node, base_url: str) -> str:
    parts = [
        _clean_text(_render_cms_inline(child, base_url))
        for child in _children(node)
    ]
    return " ".join(part for part in parts if part)


def _table_rows(node, base_url: str) -> list[list[str]]:
    if not isinstance(node, dict):
        return []
    component_type = node.get("type", "")
    if component_type == "DMCCommonTr":
        return [[_table_cell_text(child, base_url) for child in _children(node)]]

    rows: list[list[str]] = []
    for child in _children(node):
        rows.extend(_table_rows(child, base_url))
    return rows


def _render_cms_table(node, base_url: str) -> str:
    sections = _children(node)
    header_rows: list[list[str]] = []
    body_rows: list[list[str]] = []

    for section in sections:
        section_type = section.get("type", "") if isinstance(section, dict) else ""
        rows = _table_rows(section, base_url)
        if section_type == "DMCCommonThead":
            header_rows.extend(rows)
        else:
            body_rows.extend(rows)

    if not header_rows and body_rows:
        column_count = max(len(row) for row in body_rows)
        header_rows = [[f"Column {index}" for index in range(1, column_count + 1)]]

    if not header_rows:
        return ""

    header = header_rows[0]
    column_count = max(len(header), *(len(row) for row in body_rows or [[]]))
    header = header + [""] * (column_count - len(header))
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * column_count) + " |",
    ]
    for row in body_rows:
        row = row + [""] * (column_count - len(row))
        lines.append("| " + " | ".join(row[:column_count]) + " |")

    return "\n".join(lines)


def _language_from_code_node(node) -> str:
    if not isinstance(node, dict):
        return ""
    props = node.get("props") or {}
    class_name = props.get("class", "")
    match = re.search(r"language-([a-zA-Z0-9_+-]+)", class_name)
    return match.group(1) if match else ""


def _format_last_updated(raw_date: str) -> str:
    try:
        parsed = date.fromisoformat(raw_date)
    except ValueError:
        return raw_date
    return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"


def _render_cms_blocks(node, base_url: str) -> list[str]:
    if node is None:
        return []
    if isinstance(node, str):
        text = _clean_text(node)
        return [text] if text else []
    if isinstance(node, list):
        blocks: list[str] = []
        for child in node:
            blocks.extend(_render_cms_blocks(child, base_url))
        return blocks
    if not isinstance(node, dict):
        return []

    component_type = node.get("type", "")
    props = node.get("props") or {}
    children = _children(node)

    heading_levels = {
        "DMCCommonH1": 1,
        "DeveloperDMCDocsH2": 2,
        "DMCCommonH2": 2,
        "DeveloperDMCDocsH3": 3,
        "DMCCommonH3": 3,
        "DMCCommonH4": 4,
    }
    if component_type in heading_levels:
        text = _clean_text(_render_cms_inline(children, base_url))
        return [f"{'#' * heading_levels[component_type]} {text}"] if text else []
    if component_type in {"DMCCommonP", "p"}:
        text = _clean_text(_render_cms_inline(children, base_url))
        return [text] if text else []
    if component_type == "DMCUiDocsLastUpdated":
        last_updated = props.get("lastUpdated")
        return [f"Updated: {_format_last_updated(last_updated)}"] if last_updated else []
    if component_type == "DeveloperPre":
        code_node = next(
            (child for child in children
             if isinstance(child, dict) and child.get("type") == "DeveloperCode"),
            node,
        )
        language = _language_from_code_node(code_node)
        code = _render_cms_text(children, base_url).strip("\n")
        return [f"```{language}\n{code}\n```"] if code else []
    if component_type == "DMCCommonTable":
        table = _render_cms_table(node, base_url)
        return [table] if table else []
    if component_type in {"DMCCommonUl", "ul"}:
        items = []
        for child in children:
            text = _list_item_text(child, base_url)
            if text:
                items.append(f"- {text}")
        return ["\n".join(items)] if items else []
    if component_type in {"DMCCommonOl", "ol"}:
        items = []
        for index, child in enumerate(children, start=1):
            text = _list_item_text(child, base_url)
            if text:
                items.append(f"{index}. {text}")
        return ["\n".join(items)] if items else []
    if component_type in {"DMCCommonLi", "li"}:
        text = _list_item_text(node, base_url)
        return [text] if text else []
    if component_type in {"DEVHorizonImg", "DMCCommonImage", "img"}:
        text = _render_cms_inline(node, base_url)
        return [text] if text else []

    blocks: list[str] = []
    for child in children:
        blocks.extend(_render_cms_blocks(child, base_url))
    return blocks


def meta_cms_json_to_markdown(html: str, base_url: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for payload in _json_script_payloads(soup):
        for cms_tree in _find_json_cms_content(payload):
            blocks = _render_cms_blocks(cms_tree, base_url)
            markdown = "\n\n".join(block for block in blocks if block.strip())
            if markdown:
                return re.sub(r"\n{3,}", "\n\n", markdown).strip() + "\n"
    return ""


def extract_main(soup: BeautifulSoup, custom_selector: str | None = None) -> BeautifulSoup:
    for sel in REMOVE_SELECTORS:
        for el in soup.select(sel):
            el.decompose()

    if custom_selector:
        found = soup.select_one(custom_selector)
        if found:
            return found

    for sel in CONTENT_SELECTORS:
        found = soup.select_one(sel)
        if found:
            return found

    return (
        soup.find(id=re.compile("content|main|docs", re.I))
        or soup.find(class_=re.compile("content|main|docs|article", re.I))
        or soup.body
        or soup
    )


def html_to_markdown(html: str, base_url: str, content_selector: str | None = None) -> str:
    if content_selector is None:
        cms_markdown = meta_cms_json_to_markdown(html, base_url).strip()
        if cms_markdown:
            return cms_markdown + "\n"

    soup = BeautifulSoup(html, "lxml")
    absolutize_links(soup, base_url)
    main = extract_main(soup, content_selector)
    markdown = md(
        str(main),
        heading_style="ATX",
        bullets="-",
        code_language="",
        strip=["script", "style"],
    )
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = markdown.strip()

    if len(markdown) < 200:
        fallback = meta_cms_json_to_markdown(html, base_url).strip()
        if fallback:
            markdown = fallback

    return markdown + "\n"


def extract_meta_cms_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links: list[str] = []
    seen: set[str] = set()

    def add(href: str | None) -> None:
        if not href:
            return
        link = urljoin(base_url, href)
        if link not in seen:
            seen.add(link)
            links.append(link)

    def walk(node) -> None:
        if isinstance(node, dict):
            props = node.get("props") or {}
            add(props.get("href"))
            add(props.get("src"))
            for child in _children(node):
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    for payload in _json_script_payloads(soup):
        for cms_tree in _find_json_cms_content(payload):
            walk(cms_tree)

    return links


async def scrape(url: str, output: Path, timeout: int = DEFAULT_TIMEOUT,
                 wait_selector: str | None = None,
                 content_selector: str | None = None) -> Path:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()

        await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        try:
            await page.wait_for_load_state("networkidle", timeout=min(timeout, 10_000))
        except Exception:
            pass

        if wait_selector:
            try:
                await page.wait_for_selector(wait_selector, timeout=15_000)
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
        await browser.close()

    markdown = html_to_markdown(html, url, content_selector)
    title = title_for_output(title, markdown)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"# {title}\n\n_Source: {url}_\n\n---\n\n{markdown}",
        encoding="utf-8",
    )
    return output


def main() -> int:
    ap = argparse.ArgumentParser(description="HTML → Markdown (JS rendered)")
    ap.add_argument("url", help="Hedef URL")
    ap.add_argument("-o", "--output", help="Çıktı dosyası (.md)")
    ap.add_argument("--wait", help="Beklenecek CSS selector (opsiyonel)")
    ap.add_argument("--content", help="İçerik konteyner CSS seçicisi (otomatik tespiti override eder)")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = ap.parse_args()

    out = Path(args.output) if args.output else output_path_for_url(Path("output"), args.url)
    result = asyncio.run(scrape(args.url, out, args.timeout, args.wait, args.content))
    print(f"OK -> {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
