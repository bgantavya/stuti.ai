from ddgs import DDGS

class SearchTool:
    def __init__(self, max_results=3):
        self.max_results = max_results

    def search(self, query):
        """Performs a web search and returns a formatted string of results."""
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=self.max_results)
                
                if not results:
                    return "Arre, kuch mila hi nahi internet pe!"

                formatted_results = []
                for r in results:
                    formatted_results.append(f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}")
                
                return "\n\n".join(formatted_results)
        except Exception as e:
            return f"Oops, internet nakhre dikha raha hai: {e}"