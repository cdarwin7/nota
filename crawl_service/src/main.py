import yaml
import argparse
import json
from crawl4ai import AsyncWebCrawler
from shared.models.crawl_job import CrawlJob
import asyncio

def load_config(path: str) -> CrawlJob:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return CrawlJob(**data)

async def run_crawler(job: CrawlJob):
    crawler = AsyncWebCrawler()
    results = await crawler.arun(
        url=job.url,
        max_depth=job.max_depth,
        include_subdomains=job.include_subdomains,
        obey_robots_txt=job.obey_robots_txt,
        bypass_cache=job.bypass_cache
    )
    return results

def main():
    parser = argparse.ArgumentParser(description="Run a crawl job.")
    parser.add_argument("--config", type=str, required=True, help="Path to crawl job YAML config")
    args = parser.parse_args()

    job = load_config(args.config)
    results = asyncio.run(run_crawler(job))

    output = [r.model_dump() for r in results]
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
