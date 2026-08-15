import urllib.request
import urllib.parse
import json
import re
from typing import List, Dict, Any

class ExternalSearchService:
    """
    Lightweight web search service using public web search endpoints (e.g. DuckDuckGo API/HTML parser)
    to retrieve real-time search context when current information is requested or corpus knowledge is sparse.
    Zero third-party API key requirement.
    """

    def fetch_web_context(self, query: str, max_results: int = 4) -> List[Dict[str, Any]]:
        results = []
        try:
            encoded_q = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_q}"
            
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
            )

            with urllib.request.urlopen(req, timeout=3.5) as resp:
                html = resp.read().decode('utf-8', errors='ignore')

            # Parse titles, links, and snippets using regex from DDG HTML response
            # Format pattern: <a class="result__a" href="...">title</a> ... <a class="result__snippet">snippet</a>
            articles = re.findall(r'<a class="result__a" href="([^"]+)">(.*?)</a>.*?<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)

            for raw_link, raw_title, raw_snippet in articles[:max_results]:
                # Clean HTML tags
                title = re.sub(r'<[^>]+>', '', raw_title).strip()
                snippet = re.sub(r'<[^>]+>', '', raw_snippet).strip()
                
                # Unpack DDG redirect link if necessary
                link = raw_link
                if "uddg=" in link:
                    parsed_qs = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
                    if "uddg" in parsed_qs:
                        link = parsed_qs["uddg"][0]

                if title and snippet:
                    results.append({
                        "title": title,
                        "url": link,
                        "snippet": snippet,
                        "source": urllib.parse.urlparse(link).netloc or "Web Reference"
                    })

        except Exception as e:
            # Graceful fallback if internet fetch times out or network is restricted
            print(f"[ExternalSearchService] Web search fetch skipped/failed: {e}")

        return results

external_search_service = ExternalSearchService()
