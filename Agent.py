import os
import asyncio
import httpx
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from groq import Groq
import serpapi

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SERPAPI_client = serpapi.Client(api_key=SERP_API_KEY)
GROQAPI_client = Groq(api_key=GROQ_API_KEY)



# Asynchronous function to fetch content from a URL
async def get_content_async(link):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(link, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # Remove unwanted tags
                for tag in soup(["script", "style", "header", "footer", "nav"]):
                    tag.decompose()

                # Extract main content from key tags
                cleaned_text = []
                for elem in soup.find_all(["p", "h2", "h3"]):
                    text = elem.get_text(strip=True)
                    if text:
                        cleaned_text.append(text)

                # Limit content length
                return "\n".join(cleaned_text[:3000])  # Limit to 3000 characters
        except httpx.RequestError as e:
            print(f"Failed to fetch {link}: {e}")
        return None

# Asynchronous function to get web results in parallel
async def get_web_results_async(query, num_results=5):
    print("Fetching web results for the query:", query)
    
    result = SERPAPI_client.search(
        q=query,
        location="india",
        hl="en",
        engine="google",
    )

    links = [link['link'] for link in result.get('organic_results', [])[:num_results]]
    
    # Fetch content for each link asynchronously
    tasks = [get_content_async(link) for link in links]
    content_results = await asyncio.gather(*tasks)

    # Combine content and limit to the first 5000 characters
    content = "\n".join(filter(None, content_results))[:5000]
    return content

# Function to get LLM results
async def get_llm_results(text, query):
    print("Fetching LLM results for query:", query)
    chat_complete = GROQAPI_client.chat.completions.create(
        messages=[      
            {
                "role": "user",
                "content": f" {query} directly from the text {text[:5000]} "  # Limit text to 5000 chars
            }
        ],
        model="mixtral-8x7b-32768",
    )

    return chat_complete.choices[0].message.content

# Main function to fetch results with async web scraping
def fetch_results(query, num_results=5):
    text = asyncio.run(get_web_results_async(query, num_results=num_results))
    return asyncio.run(get_llm_results(text, query))
