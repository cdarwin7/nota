from pydantic import BaseModel
from typing import Optional

class CrawlJob(BaseModel):
    url: str
    max_depth: int = 2
    include_subdomains: bool = False
    obey_robots_txt: bool = True
    bypass_cache: bool = True
