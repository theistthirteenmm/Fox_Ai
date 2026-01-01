# 🧠 Fox Learning & Teaching System Guide
## راهنمای سیستم یادگیری و آموزش Fox

Fox AI Assistant now includes a comprehensive learning system that allows users to teach Fox custom responses, facts, and knowledge. This creates a truly personalized AI experience that adapts to each user's preferences and needs.

## 🎯 Core Features

### 1. Custom Response Teaching
Teach Fox specific responses to trigger words or phrases:
```bash
/teach سلام سلام عزیز! چطوری؟
/teach چطوری عالی هستم! تو چطوری؟
/teach خداحافظ خداحافظ! مراقب خودت باش
```

### 2. Fact Learning
Store factual information by topic:
```bash
/learn ایران پایتخت ایران تهران است
/learn برنامه‌نویسی Python زبان برنامه‌نویسی قدرتمندی است
/learn موسیقی موسیقی کلاسیک آرامش‌بخش است
```

### 3. Learning Statistics
View what Fox has learned:
```bash
/learned
```

## 🔧 Technical Architecture

### Learning Data Structure
Each user has a separate learning file: `data/profiles/{username}_learning.json`

```json
{
  "custom_responses": {
    "سلام": {
      "response": "سلام عزیز! چطوری؟",
      "taught_at": "2024-01-15T10:30:00",
      "usage_count": 5
    }
  },
  "learned_facts": {
    "ایران": [
      {
        "fact": "پایتخت ایران تهران است",
        "taught_at": "2024-01-15T10:35:00"
      }
    ]
  },
  "cultural_knowledge": {},
  "personal_preferences": {},
  "daily_routines": {},
  "teaching_sessions": [],
  "learned_phrases": []
}
```

### Integration with LLM Engine
The learning system is integrated at the LLM level:

1. **Response Priority**: Learned responses are checked first before AI generation
2. **Trigger Matching**: Case-insensitive substring matching for triggers
3. **Usage Tracking**: Automatic counting of how often learned responses are used
4. **Fact Retrieval**: Topic-based fact lookup for relevant questions

### Learning System Classes

#### FoxLearningSystem
- `teach_response(trigger, response)` - Teach custom responses
- `teach_fact(topic, fact)` - Store factual information
- `teach_culture(country, info)` - Cultural knowledge
- `teach_routine(name, description)` - Daily routines
- `teach_preference(category, preference)` - Personal preferences
- `get_learned_response(input)` - Retrieve learned responses
- `get_learning_stats()` - Learning statistics

## 🎮 Usage Examples

### Basic Teaching Session
```bash
# Start Fox
python cli/main.py

# Teach greetings
/teach سلام سلام دوست عزیز!
/teach صبح‌بخیر صبح‌تون بخیر! امروز چه برنامه‌ای دارید؟

# Teach facts
/learn تهران تهران پایتخت ایران و بزرگترین شهر کشور است
/learn Python Python یکی از محبوب‌ترین زبان‌های برنامه‌نویسی است

# Test learned responses
سلام
# Fox responds: سلام دوست عزیز!

تهران چطور شهریه؟
# Fox responds: راجع به تهران: تهران پایتخت ایران و بزرگترین شهر کشور است

# Check learning stats
/learned
```

### Advanced Teaching
```bash
# Teach personality responses
/teach خسته‌ام بیا استراحت کن! چای می‌خوری؟
/teach حوصله‌م سر رفته بیا یه بازی کنیم یا فیلم ببینیم!

# Teach preferences
/teach موسیقی‌ات چیه من موسیقی کلاسیک و راک دوست دارم

# Teach cultural info
/learn نوروز نوروز جشن سال نو ایرانی است که در اول فروردین جشن گرفته می‌شود
```

## 🔄 Learning Workflow

1. **User teaches Fox**: `/teach` or `/learn` commands
2. **Data storage**: Information saved to user-specific JSON file
3. **Response integration**: LLM engine checks learned data first
4. **Usage tracking**: Automatic counting and statistics
5. **Continuous learning**: Fox gets smarter with each interaction

## 🌟 Benefits

### For Users
- **Personalized responses** tailored to individual preferences
- **Cultural adaptation** with region-specific knowledge
- **Memory persistence** across sessions
- **Custom personality** development over time

### For Families
- **Multi-user support** with separate learning profiles
- **Shared knowledge** within family context
- **Individual preferences** respected per user
- **Collaborative teaching** by family members

## 🚀 Future Enhancements

### Planned Features
- **Automatic learning** from conversation patterns
- **Context-aware responses** based on time/mood
- **Learning from corrections** when users provide feedback
- **Export/import** learning data between users
- **Learning recommendations** based on usage patterns

### Advanced Capabilities
- **Sentiment learning** to match user emotional states
- **Topic clustering** for better fact organization
- **Response variations** to avoid repetitive answers
- **Learning confidence** scoring for response quality

## 🔒 Privacy & Security

- **Local storage**: All learning data stored locally
- **User isolation**: Each user's learning data is separate
- **No cloud sync**: Learning data never leaves the device
- **Data control**: Users can view and modify their learning data

## 📊 Monitoring & Analytics

### Learning Statistics
- Number of custom responses taught
- Facts learned by topic
- Usage frequency of learned responses
- Learning session history
- Most active learning categories

### Performance Metrics
- Response accuracy improvement
- User satisfaction with learned responses
- Learning retention over time
- System performance impact

## 🛠️ Troubleshooting

### Common Issues
1. **Learning not working**: Check if learning system is initialized
2. **Responses not used**: Verify trigger word matching
3. **Data not persisting**: Check file permissions in data/profiles/
4. **Performance issues**: Monitor learning file size

### Debug Commands
```bash
# Check learning file
cat data/profiles/{username}_learning.json

# View learning stats
/learned

# Test specific trigger
/teach test این یک تست است
test
```

## 📝 Best Practices

### Effective Teaching
1. **Use clear triggers** that are easy to remember
2. **Keep responses natural** and conversational
3. **Organize facts by topic** for better retrieval
4. **Test learned responses** regularly
5. **Update outdated information** as needed

### Learning Strategy
1. **Start with common phrases** like greetings
2. **Add personal preferences** gradually
3. **Include cultural context** relevant to user
4. **Build topic-specific knowledge** areas
5. **Maintain response variety** to avoid monotony

The Fox Learning System transforms your AI assistant into a truly personalized companion that grows smarter and more helpful with every interaction!
