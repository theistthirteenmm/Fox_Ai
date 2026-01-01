"""
Internet Access Module
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_web(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search the web using DuckDuckGo HTML scraping"""
        try:
            # Use DuckDuckGo HTML search
            search_url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Find search results
            result_divs = soup.find_all('div', class_='result')
            
            for div in result_divs[:num_results]:
                try:
                    # Get title and link
                    title_link = div.find('a', class_='result__a')
                    if not title_link:
                        continue
                    
                    title = title_link.get_text(strip=True)
                    url = title_link.get('href', '')
                    
                    # Get snippet
                    snippet_div = div.find('div', class_='result__snippet')
                    snippet = snippet_div.get_text(strip=True) if snippet_div else ''
                    
                    if title and snippet:
                        results.append({
                            'title': title,
                            'url': url,
                            'content': snippet
                        })
                        
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
                results.append({
                    'title': data.get('Heading', 'خلاصه'),
                    'content': data['Abstract'],
                    'url': data.get('AbstractURL', ''),
                    'source': 'DuckDuckGo'
                })
            
            # Get related topics
            for topic in data.get('RelatedTopics', [])[:num_results-1]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('Text', '')[:100] + '...',
                        'content': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo'
                    })
            
            return results[:num_results]
            
        except Exception as e:
            return [{'title': 'خطا در جستجو', 'content': f'خطا: {str(e)}', 'url': '', 'source': 'Error'}]
    
    def get_webpage_content(self, url: str, max_length: int = 2000) -> Dict:
        """Get content from a webpage"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get title
            title = soup.find('title')
            title = title.get_text().strip() if title else 'بدون عنوان'
            
            # Get main content
            content = soup.get_text()
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Truncate if too long
            if len(content) > max_length:
                content = content[:max_length] + '...'
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'title': 'خطا در دریافت محتوا',
                'content': f'خطا: {str(e)}',
                'url': url,
                'status': 'error'
            }
    
    def get_weather(self, city: str = "Tehran") -> Dict:
        """Get weather information"""
        try:
            # Simple weather API (you can replace with a better one)
            query = f"weather in {city}"
            results = self.search_web(query, 1)
            
            if results:
                return {
                    'city': city,
                    'info': results[0]['content'],
                    'source': 'Web Search'
                }
            else:
                return {'city': city, 'info': 'اطلاعات آب و هوا در دسترس نیست', 'source': 'Error'}
                
        except Exception as e:
            return {'city': city, 'info': f'خطا: {str(e)}', 'source': 'Error'}
    
    def get_news(self, topic: str = "Iran", num_results: int = 3) -> List[Dict]:
        """Get latest news"""
        try:
            query = f"latest news {topic}"
            return self.search_web(query, num_results)
        except Exception as e:
            return [{'title': 'خطا در دریافت اخبار', 'content': f'خطا: {str(e)}', 'url': '', 'source': 'Error'}]
    
    def translate_text(self, text: str, target_lang: str = "fa") -> str:
        """Simple translation using web search"""
        try:
            query = f"translate to {target_lang}: {text}"
            results = self.search_web(query, 1)
            
            if results and results[0]['content']:
                return results[0]['content']
            else:
                return f"ترجمه برای '{text}' یافت نشد"
                
        except Exception as e:
            return f"خطا در ترجمه: {str(e)}"
