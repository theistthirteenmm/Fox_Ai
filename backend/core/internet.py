"""
Internet Access Module - Fixed Version
"""
import requests
import json
from typing import List, Dict, Optional
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import re

class InternetAccess:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_web(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search the web using Google search"""
        try:
            # Use Google search
            search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Find search results
            result_divs = soup.find_all('div', class_='g')
            
            for div in result_divs[:num_results]:
                try:
                    # Get title
                    title_elem = div.find('h3')
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    
                    # Get link
                    link_elem = div.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    
                    # Get snippet
                    snippet_divs = div.find_all('div', {'data-sncf': '1'}) or div.find_all('span')
                    snippet = ''
                    for span in snippet_divs:
                        text = span.get_text(strip=True)
                        if len(text) > 20:  # Only meaningful snippets
                            snippet = text
                            break
                    
                    if title and snippet:
                        results.append({
                            'title': title,
                            'url': url,
                            'content': snippet,
                            'source': 'Google'
                        })
                        
                except Exception as e:
                    continue
            
            # If no results, try a simple fallback
            if not results:
                results.append({
                    'title': f'جستجو برای: {query}',
                    'url': '',
                    'content': f'متأسفانه نتوانستم اطلاعات دقیقی درباره "{query}" پیدا کنم. لطفاً سوال خود را واضح‌تر بپرسید.',
                    'source': 'System'
                })
            
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            # Return a fallback result
            return [{
                'title': f'خطا در جستجو: {query}',
                'url': '',
                'content': f'متأسفانه در حال حاضر امکان جستجو در اینترنت وجود ندارد. خطا: {str(e)}',
                'source': 'Error'
            }]
    
    def get_news(self, topic: str = "", num_results: int = 5) -> List[Dict]:
        """Get latest news"""
        try:
            query = f"اخبار {topic}" if topic else "آخرین اخبار"
            return self.search_web(query, num_results)
        except Exception as e:
            print(f"News error: {e}")
            return []
    
    def get_weather(self, city: str = "تهران") -> Dict:
        """Get weather information"""
        try:
            query = f"آب و هوا {city}"
            results = self.search_web(query, 1)
            if results:
                return {
                    'city': city,
                    'info': results[0]['content'],
                    'source': results[0]['url']
                }
            return {}
        except Exception as e:
            print(f"Weather error: {e}")
            return {}
    
    def get_webpage_content(self, url: str) -> str:
        """Extract content from a webpage"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit to 2000 characters
            
        except Exception as e:
            return f"خطا در دریافت محتوا: {str(e)}"
