"""
🔍 Smart User Detection - تشخیص هوشمند کاربر
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re
from collections import Counter

class SmartUserDetection:
    def __init__(self):
        self.profiles_file = "data/profiles/user_signatures.json"
        self.load_signatures()
        
    def load_signatures(self):
        """بارگذاری امضاهای کاربران"""
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'r', encoding='utf-8') as f:
                self.signatures = json.load(f)
        else:
            self.signatures = {}
    
    def save_signatures(self):
        """ذخیره امضاهای کاربران"""
        os.makedirs(os.path.dirname(self.profiles_file), exist_ok=True)
        with open(self.profiles_file, 'w', encoding='utf-8') as f:
            json.dump(self.signatures, f, ensure_ascii=False, indent=2)
    
    def analyze_writing_style(self, text: str) -> Dict:
        """تحلیل سبک نوشتن"""
        # طول جملات
        sentences = re.split(r'[.!?؟]', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / max(len([s for s in sentences if s.strip()]), 1)
        
        # استفاده از علائم نگارشی
        punctuation_usage = {
            'question_marks': text.count('؟') + text.count('?'),
            'exclamations': text.count('!'),
            'dots': text.count('...'),
            'emojis': len(re.findall(r'[😀-🙏]', text))
        }
        
        # کلمات رایج شخصی
        personal_words = re.findall(r'\b(?:من|تو|شما|ما|خودم|خودت|برام|برات|میگم|میگی|بهت|بهم)\b', text.lower())
        
        # سبک سوال پرسیدن
        question_style = {
            'direct_questions': len(re.findall(r'\b(?:چی|چه|کی|کجا|چطور|چرا)\b', text.lower())),
            'polite_requests': len(re.findall(r'\b(?:لطفا|ممنون|متشکرم|خواهش)\b', text.lower()))
        }
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'punctuation': punctuation_usage,
            'personal_words': Counter(personal_words),
            'question_style': question_style,
            'text_length': len(text),
            'word_count': len(text.split())
        }
    
    def extract_content_patterns(self, text: str) -> Dict:
        """استخراج الگوهای محتوایی"""
        # موضوعات مورد علاقه
        topics = {
            'tech': len(re.findall(r'\b(?:کامپیوتر|برنامه|کد|سایت|اپ|تکنولوژی)\b', text.lower())),
            'family': len(re.findall(r'\b(?:خانواده|بچه|فرزند|همسر|مادر|پدر|برادر|خواهر)\b', text.lower())),
            'work': len(re.findall(r'\b(?:کار|شغل|اداره|پروژه|جلسه|مدیر)\b', text.lower())),
            'daily': len(re.findall(r'\b(?:صبح|شب|ناهار|شام|خواب|بیدار)\b', text.lower())),
            'emotions': len(re.findall(r'\b(?:خوشحال|غمگین|عصبانی|آرام|استرس|خسته)\b', text.lower()))
        }
        
        # نحوه صحبت
        speech_patterns = {
            'formal': len(re.findall(r'\b(?:شما|جناب|سرکار|محترم)\b', text.lower())),
            'informal': len(re.findall(r'\b(?:تو|داداش|رفیق|عزیزم)\b', text.lower())),
            'questions': text.count('؟') + text.count('?'),
            'commands': len(re.findall(r'\b(?:بگو|کن|بده|بیار|برو)\b', text.lower()))
        }
        
        return {
            'topics': topics,
            'speech_patterns': speech_patterns
        }
    
    def learn_user_signature(self, username: str, text: str):
        """یادگیری امضای کاربر"""
        if username not in self.signatures:
            self.signatures[username] = {
                'writing_styles': [],
                'content_patterns': [],
                'common_phrases': [],
                'last_updated': datetime.now().isoformat(),
                'message_count': 0
            }
        
        # تحلیل سبک نوشتن
        style = self.analyze_writing_style(text)
        content = self.extract_content_patterns(text)
        
        # اضافه کردن به تاریخچه
        self.signatures[username]['writing_styles'].append(style)
        self.signatures[username]['content_patterns'].append(content)
        self.signatures[username]['message_count'] += 1
        self.signatures[username]['last_updated'] = datetime.now().isoformat()
        
        # استخراج عبارات رایج
        phrases = re.findall(r'\b\w+\s+\w+\b', text.lower())
        self.signatures[username]['common_phrases'].extend(phrases)
        
        # نگهداری فقط 50 نمونه اخیر
        if len(self.signatures[username]['writing_styles']) > 50:
            self.signatures[username]['writing_styles'] = self.signatures[username]['writing_styles'][-50:]
            self.signatures[username]['content_patterns'] = self.signatures[username]['content_patterns'][-50:]
        
        # نگهداری فقط 100 عبارت رایج
        if len(self.signatures[username]['common_phrases']) > 100:
            phrase_counter = Counter(self.signatures[username]['common_phrases'])
            self.signatures[username]['common_phrases'] = [phrase for phrase, count in phrase_counter.most_common(100)]
        
        self.save_signatures()
    
    def calculate_similarity_score(self, text: str, username: str) -> float:
        """محاسبه امتیاز شباهت"""
        if username not in self.signatures or not self.signatures[username]['writing_styles']:
            return 0.0
        
        current_style = self.analyze_writing_style(text)
        current_content = self.extract_content_patterns(text)
        
        user_data = self.signatures[username]
        
        # میانگین سبک‌های قبلی
        avg_style = self._calculate_average_style(user_data['writing_styles'])
        avg_content = self._calculate_average_content(user_data['content_patterns'])
        
        # محاسبه امتیاز شباهت سبک نوشتن
        style_score = 0.0
        
        # طول جمله
        length_diff = abs(current_style['avg_sentence_length'] - avg_style['avg_sentence_length'])
        style_score += max(0, 1 - length_diff / 10) * 0.2
        
        # علائم نگارشی
        punct_score = 0
        for key in current_style['punctuation']:
            if key in avg_style['punctuation']:
                diff = abs(current_style['punctuation'][key] - avg_style['punctuation'][key])
                punct_score += max(0, 1 - diff / 5)
        style_score += (punct_score / len(current_style['punctuation'])) * 0.3
        
        # محاسبه امتیاز محتوا
        content_score = 0.0
        
        # موضوعات
        topic_score = 0
        for topic in current_content['topics']:
            if topic in avg_content['topics']:
                if avg_content['topics'][topic] > 0:
                    similarity = min(current_content['topics'][topic], avg_content['topics'][topic]) / max(current_content['topics'][topic], avg_content['topics'][topic], 1)
                    topic_score += similarity
        content_score += (topic_score / len(current_content['topics'])) * 0.3
        
        # عبارات رایج
        text_phrases = re.findall(r'\b\w+\s+\w+\b', text.lower())
        common_phrases = set(user_data['common_phrases'])
        matching_phrases = sum(1 for phrase in text_phrases if phrase in common_phrases)
        phrase_score = matching_phrases / max(len(text_phrases), 1)
        
        # کلمات کلیدی مشخصه کاربر
        text_words = set(text.lower().split())
        user_words = set()
        for phrase in user_data['common_phrases']:
            user_words.update(phrase.split())
        
        common_words = text_words & user_words
        word_score = len(common_words) / max(len(text_words), 1)
        
        content_score += phrase_score * 0.15 + word_score * 0.15
        
        # امتیاز نهایی
        final_score = (style_score + content_score) / 2
        return min(1.0, max(0.0, final_score))
    
    def _calculate_average_style(self, styles: List[Dict]) -> Dict:
        """محاسبه میانگین سبک نوشتن"""
        if not styles:
            return {}
        
        avg = {
            'avg_sentence_length': sum(s['avg_sentence_length'] for s in styles) / len(styles),
            'punctuation': {},
            'text_length': sum(s['text_length'] for s in styles) / len(styles),
            'word_count': sum(s['word_count'] for s in styles) / len(styles)
        }
        
        # میانگین علائم نگارشی
        punct_keys = set()
        for style in styles:
            punct_keys.update(style['punctuation'].keys())
        
        for key in punct_keys:
            values = [s['punctuation'].get(key, 0) for s in styles]
            avg['punctuation'][key] = sum(values) / len(values)
        
        return avg
    
    def _calculate_average_content(self, contents: List[Dict]) -> Dict:
        """محاسبه میانگین الگوهای محتوایی"""
        if not contents:
            return {'topics': {}, 'speech_patterns': {}}
        
        avg = {'topics': {}, 'speech_patterns': {}}
        
        # میانگین موضوعات
        topic_keys = set()
        for content in contents:
            topic_keys.update(content['topics'].keys())
        
        for key in topic_keys:
            values = [c['topics'].get(key, 0) for c in contents]
            avg['topics'][key] = sum(values) / len(values)
        
        # میانگین الگوهای گفتاری
        speech_keys = set()
        for content in contents:
            speech_keys.update(content['speech_patterns'].keys())
        
        for key in speech_keys:
            values = [c['speech_patterns'].get(key, 0) for c in contents]
            avg['speech_patterns'][key] = sum(values) / len(values)
        
        return avg
    
    def detect_current_user(self, text: str, known_users: List[str], threshold: float = 0.3) -> Tuple[Optional[str], float]:
        """تشخیص کاربر فعلی بر اساس متن"""
        if not known_users:
            return None, 0.0
        
        scores = {}
        for username in known_users:
            score = self.calculate_similarity_score(text, username)
            scores[username] = score
        
        # بهترین امتیاز
        best_user = max(scores, key=scores.get)
        best_score = scores[best_user]
        
        if best_score >= threshold:
            return best_user, best_score
        else:
            return None, best_score
    
    def get_user_statistics(self, username: str) -> Dict:
        """آمار کاربر"""
        if username not in self.signatures:
            return {"error": "کاربر یافت نشد"}
        
        data = self.signatures[username]
        
        return {
            "message_count": data['message_count'],
            "last_updated": data['last_updated'],
            "avg_message_length": sum(s['text_length'] for s in data['writing_styles']) / len(data['writing_styles']) if data['writing_styles'] else 0,
            "common_phrases_count": len(set(data['common_phrases'])),
            "signature_strength": min(data['message_count'] / 20, 1.0)  # قدرت امضا (0-1)
        }

# نمونه استفاده
smart_detector = SmartUserDetection()
