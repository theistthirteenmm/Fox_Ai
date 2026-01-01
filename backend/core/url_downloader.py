"""
URL Dataset Downloader
دانلود دیتاست از آدرس اینترنتی
"""
import requests
import json
import csv
import os
from backend.core.fox_learning import FoxLearningSystem
from backend.core.user_profiles import user_manager

class URLDatasetDownloader:
    def __init__(self):
        self.data_dir = "data/url_datasets"
        self.ensure_data_dir()
        
    def ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)
        
    def download_from_url(self, url):
        """دانلود فایل از URL"""
        print(f"📥 دانلود از: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            return response.text
            
        except Exception as e:
            raise Exception(f"خطا در دانلود: {str(e)}")
            
    def parse_dataset(self, content, url):
        """تجزیه دیتاست"""
        print("🔍 تجزیه دیتاست...")
        
        data = []
        
        try:
            # تشخیص نوع فایل از URL
            if url.endswith('.json'):
                data = self.parse_json(content)
            elif url.endswith('.csv'):
                data = self.parse_csv(content)
            elif url.endswith('.txt'):
                data = self.parse_txt(content)
            else:
                # تلاش برای JSON
                try:
                    data = self.parse_json(content)
                except:
                    # تلاش برای CSV
                    try:
                        data = self.parse_csv(content)
                    except:
                        # تلاش برای TXT
                        data = self.parse_txt(content)
                        
        except Exception as e:
            raise Exception(f"خطا در تجزیه: {str(e)}")
            
        return data
        
    def parse_json(self, content):
        """تجزیه JSON"""
        json_data = json.loads(content)
        
        conversations = []
        
        # فرمت‌های مختلف JSON
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    # فرمت {"question": "...", "answer": "..."}
                    if "question" in item and "answer" in item:
                        conversations.append({
                            "q": item["question"],
                            "a": item["answer"]
                        })
                    # فرمت {"q": "...", "a": "..."}
                    elif "q" in item and "a" in item:
                        conversations.append(item)
                    # فرمت {"input": "...", "output": "..."}
                    elif "input" in item and "output" in item:
                        conversations.append({
                            "q": item["input"],
                            "a": item["output"]
                        })
                        
        elif isinstance(json_data, dict):
            # فرمت {"conversations": [...]}
            if "conversations" in json_data:
                return self.parse_json(json.dumps(json_data["conversations"]))
            # فرمت {"data": [...]}
            elif "data" in json_data:
                return self.parse_json(json.dumps(json_data["data"]))
                
        return conversations
        
    def parse_csv(self, content):
        """تجزیه CSV"""
        conversations = []
        
        lines = content.strip().split('\n')
        reader = csv.reader(lines)
        
        headers = next(reader, None)
        if not headers:
            return conversations
            
        for row in reader:
            if len(row) >= 2:
                conversations.append({
                    "q": row[0].strip(),
                    "a": row[1].strip()
                })
                
        return conversations
        
    def parse_txt(self, content):
        """تجزیه TXT"""
        conversations = []
        
        lines = content.strip().split('\n')
        
        for i in range(0, len(lines)-1, 2):
            if i+1 < len(lines):
                q = lines[i].strip()
                a = lines[i+1].strip()
                
                if q and a:
                    conversations.append({
                        "q": q,
                        "a": a
                    })
                    
        return conversations
        
    def save_to_fox(self, data, url):
        """ذخیره در مغز Fox"""
        print("🧠 ذخیره در مغز Fox...")
        
        profile = user_manager.get_current_user_profile()
        fox_learning = FoxLearningSystem(profile)
        
        saved_count = 0
        
        for item in data:
            try:
                if "q" in item and "a" in item:
                    fox_learning.teach_response(item["q"], item["a"])
                    saved_count += 1
                    
                    if saved_count % 10 == 0:
                        print(f"✅ {saved_count} مکالمه ذخیره شد...")
                        
            except Exception as e:
                continue
                
        # ذخیره در فایل
        filename = url.split('/')[-1] or "dataset"
        json_file = os.path.join(self.data_dir, f"{filename}.json")
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"🎉 {saved_count} مکالمه ذخیره شد!")
        print(f"📁 فایل: {json_file}")
        
        return saved_count
        
    def download_and_process(self, url):
        """دانلود و پردازش کامل"""
        try:
            # دانلود
            content = self.download_from_url(url)
            
            # تجزیه
            data = self.parse_dataset(content, url)
            
            if not data:
                return {"error": "هیچ مکالمه‌ای یافت نشد"}
                
            # ذخیره
            saved_count = self.save_to_fox(data, url)
            
            return {
                "success": True,
                "downloaded": len(data),
                "saved": saved_count,
                "url": url
            }
            
        except Exception as e:
            return {"error": str(e)}

# Global instance
url_downloader = URLDatasetDownloader()
