import asyncio
from crawl4ai import AsyncWebCrawler
from readability import Document
from bs4 import BeautifulSoup
from weasyprint import HTML
import os

# -----------------------
# 🗨️ Step 1: Ask user for input
# -----------------------
print("📘 Crawl4AI Article-to-PDF Tool")
url = input("Enter the website URL to crawl (e.g., https://example.com): ").strip()
max_depth = int(input("Enter crawl depth (e.g., 2): ").strip())
include_subdomains = input("Include subdomains? (y/n): ").strip().lower() == "y"
obey_robots = input("Obey robots.txt? (y/n): ").strip().lower() == "y"
pdf_filename = input("Enter the output PDF filename (e.g., output.pdf): ").strip()
print("Note: The PDF will be saved in the current directory.")

# -----------------------
# 📥 Step 2: Crawl website
# -----------------------
crawler = AsyncWebCrawler(
    url=url,
    max_depth=max_depth,
    include_subdomains=include_subdomains,
    obey_robots_txt=obey_robots
)

print(f"🔍 Crawling {url} with depth={max_depth}, subdomains={include_subdomains}, obey_robots={obey_robots}...")

results = asyncio.run(
    crawler.arun()
)
print(f"✅ Crawled {len(results)} pages."
      f" Found {len([page for page in results if page['is_article']])} articles."
      f" Found {len([page for page in results if not page['is_article']])} non-articles.")
# -----------------------
# 🧹 Step 3: Filter, clean and collect reader-mode HTML
# -----------------------
os.makedirs("articles", exist_ok=True)
# Create a directory to store the articles
# If it doesn't exist
# os.makedirs("articles", exist_ok=True)
# If it does exist, remove all files in it
for filename in os.listdir("articles"):
    file_path = os.path.join("articles", filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

html_files = []

for i, page in enumerate(results):
    page_url = page["url"]
    html = page["html"]
    
    soup = BeautifulSoup(html, "html.parser")
    has_locale = soup.find("meta", {"property": "og:locale", "content": "en_US"})
    has_type = soup.find("meta", {"property": "og:type", "content": "article"})

    if has_locale and has_type:
        doc = Document(html)
        content_html = doc.summary()
        title = doc.title()

        full_html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Georgia, serif; margin: 2em; }}
                h1 {{ font-size: 1.5em; margin-bottom: 0.5em; }}
            </style>
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            {content_html}
        </body>
        </html>
        """

        filename = f"articles/article_{i+1}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_html)
        html_files.append(filename)
        print(f"✅ Saved: {page_url}")
    else:
        print(f"⏭️ Skipped (not article): {page_url}")

# -----------------------
# 📘 Step 4: Combine HTMLs and generate PDF
# -----------------------
combined_html = "<html><head><meta charset='utf-8'></head><body>"
for file in html_files:
    with open(file, encoding="utf-8") as f:
        combined_html += f.read()
        combined_html += "<div style='page-break-after: always;'></div>"
combined_html += "</body></html>"

HTML(string=combined_html).write_pdf(pdf_filename)
# Save the PDF with the user-specified filename")
print("\n📄 PDF book generated: Website_Articles_Book.pdf")
