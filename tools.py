from ddgs import DDGS
from google import genai
from typing import Any

class SearchTool:
    def __init__(self, max_results: int = 3) -> None:
        self.max_results = max_results

    def search(self, query: str) -> str:
        """Performs a web search and returns a formatted string of results."""
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=self.max_results)
                
                if not results:
                    return "Arre, kuch mila hi nahi internet pe!"

                formatted_results: list[str] = []
                for r in results:
                    formatted_results.append(f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}")
                
                return "\n\n".join(formatted_results)
        except Exception as e:
            return f"Oops, internet nakhre dikha raha hai: {e}"
        
    # DDGS_whois = {

    # }

class Memory:
    def __init__(self) -> None:
        self.facts: list[str] = []

    def getFacts(self) -> list[str]:
        return self.facts

    def addFact(self, fact: str) -> None:
        self.facts.append(fact)

class GS:
    grounding_tool: Any = genai.types.Tool(
        google_search=genai.types.GoogleSearch()
    )