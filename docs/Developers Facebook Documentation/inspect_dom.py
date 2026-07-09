"""Quick DOM inspection: aday content container'ları listele."""
import asyncio, sys
from playwright.async_api import async_playwright

CANDIDATES = [
    "main", "article", "[role='main']",
    "[data-testid*='doc' i]", "[data-testid*='content' i]",
    "[class*='docContent' i]", "[class*='docsContent' i]",
    "[class*='Content' i]:not(nav):not(header):not(footer)",
    "#content", "#docs", "#main",
]

async def main(url):
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        page = await b.new_page()
        await page.goto(url, wait_until="networkidle", timeout=60000)

        print(f"\nTitle: {await page.title()}\n")
        print(f"{'Selector':<55} {'Count':>6} {'~Chars':>10}")
        print("-" * 75)
        for sel in CANDIDATES:
            try:
                els = await page.query_selector_all(sel)
                if els:
                    text = await els[0].inner_text()
                    print(f"{sel:<55} {len(els):>6} {len(text):>10}")
            except Exception:
                pass

        # Sayfanın en uzun text bloklu div'lerini bul
        print("\nEn uzun text bloklu 5 element (heuristic):")
        results = await page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('div, section, article, main'));
            return els
                .map(el => ({
                    tag: el.tagName.toLowerCase(),
                    id: el.id || '',
                    cls: (el.className || '').toString().slice(0, 60),
                    len: el.innerText?.length || 0,
                    hasNav: el.querySelector('nav') !== null,
                }))
                .filter(x => x.len > 500 && !x.hasNav)
                .sort((a, b) => b.len - a.len)
                .slice(0, 5);
        }""")
        for r in results:
            print(f"  <{r['tag']} id='{r['id']}' class='{r['cls']}'> len={r['len']}")

        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
