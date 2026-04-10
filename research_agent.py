import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self):
        # Initialize Tavily for web search
        tavily_api_key = os.getenv('TAVILY_API_KEY')
        if not tavily_api_key:
            print("Warning: TAVILY_API_KEY not found. Using mock data.")
            self.tavily = None
        else:
            self.tavily = TavilyClient(api_key=tavily_api_key)
    
    def search_company_news(self, company_name, promoter_name=None):
        """
        Search for news about the company and promoter
        """
        if not self.tavily:
            # Return mock data for development
            return self._get_mock_data(company_name, promoter_name)
        
        search_results = []
        
        # Search for company news
        company_query = f"{company_name} Indian company news 2026"
        try:
            response = self.tavily.search(query=company_query, search_depth="advanced")
            search_results.extend(response.get('results', [])[:5])
        except Exception as e:
            print(f"Error searching company: {e}")
        
        # Search for promoter if provided
        if promoter_name:
            promoter_query = f"{promoter_name} business news legal cases"
            try:
                response = self.tavily.search(query=promoter_query, search_depth="advanced")
                search_results.extend(response.get('results', [])[:3])
            except Exception as e:
                print(f"Error searching promoter: {e}")
        
        # Search for sector trends
        sector_query = f"{company_name} industry sector trends India 2026"
        try:
            response = self.tavily.search(query=sector_query, search_depth="basic")
            search_results.extend(response.get('results', [])[:2])
        except Exception as e:
            print(f"Error searching sector: {e}")
        
        return search_results
    
    def _get_mock_data(self, company_name, promoter_name):
        """
        Mock data for development when API keys aren't available
        """
        return [
            {
                "title": f"{company_name} Reports 15% Revenue Growth in Q4",
                "content": f"{company_name} has announced strong quarterly results with 15% revenue growth. The company's EBITDA margins improved by 200 basis points.",
                "url": "https://economictimes.indiatimes.com/mock1",
                "sentiment": "positive"
            },
            {
                "title": f"Court Case Update: {company_name} involved in tax dispute",
                "content": f"A tax dispute involving {company_name} has been ongoing since 2023. The company has contested the demand of ₹2.5 crores.",
                "url": "https://www.livemint.com/mock2",
                "sentiment": "negative"
            },
            {
                "title": f"Sector Headwind: New RBI regulations impact {company_name}'s industry",
                "content": "RBI's new guidelines on lending could impact working capital availability in the sector. Industry bodies have raised concerns.",
                "url": "https://www.business-standard.com/mock3",
                "sentiment": "negative"
            },
            {
                "title": f"{promoter_name} appointed to industry board",
                "content": f"{promoter_name}, promoter of {company_name}, has been appointed to the CII national committee, reflecting industry recognition.",
                "url": "https://www.financialexpress.com/mock4",
                "sentiment": "positive"
            }
        ] if promoter_name else [
            {
                "title": f"{company_name} Expands Manufacturing Capacity",
                "content": f"{company_name} is investing ₹50 crores in new manufacturing facility in Gujarat.",
                "url": "https://economictimes.indiatimes.com/mock1",
                "sentiment": "positive"
            }
        ]