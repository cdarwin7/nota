import asyncio
from crawl4ai import AsyncWebCrawler

print("📘 Crawl4AI Test Tool")
url = input("Enter the website URL to test crawl (e.g., https://example.com): ").strip()

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        print(f"🔍 Crawling the first 300 characters of {url}...")
        print(result.markdown[:300])  # Print first 300 chars

if __name__ == "__main__":
    asyncio.run(main())