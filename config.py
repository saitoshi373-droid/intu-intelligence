import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GMAIL_USER = os.getenv("GMAIL_USER", "saitoshi373@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO", "saitoshi373@gmail.com")

RSS_SOURCES = {
    "思考力・認知科学": [
        ("Psychology Today", "https://www.psychologytoday.com/intl/node/feed/rss"),
        ("Big Think", "https://bigthink.com/feed/"),
        ("Scientific American", "https://rss.sciam.com/ScientificAmerican-News"),
        ("Greater Good Science Center", "https://greatergood.berkeley.edu/feeds/news"),
    ],
    "日本の教育": [
        ("文部科学省", "https://www.mext.go.jp/rss/index.xml"),
        ("NHK教育・文化", "https://www3.nhk.or.jp/rss/news/cat05.xml"),
        ("東洋経済education×ICT", "https://toyokeizai.net/list/feed/rss?category_name=education"),
    ],
    "海外の教育": [
        ("Education Week", "https://www.edweek.org/feed"),
        ("The Guardian Education", "https://www.theguardian.com/education/rss"),
        ("MIT News Education", "https://news.mit.edu/rss/topic/education"),
        ("OECD Education", "https://oecdedutoday.com/feed/"),
    ],
    "脳科学・神経科学": [
        ("Neuroscience News", "https://neurosciencenews.com/feed/"),
        ("BrainFacts", "https://www.brainfacts.org/rss/news"),
    ],
    "ビジネス×思考力": [
        ("Harvard Business Review", "https://feeds.hbr.org/harvardbusiness"),
        ("MIT Sloan Management Review", "https://mitsloan.mit.edu/ideas-made-to-matter/rss.xml"),
        ("McKinsey Insights", "https://www.mckinsey.com/rss"),
    ],
    "EdTech・教育テクノロジー": [
        ("EdSurge", "https://www.edsurge.com/news.rss"),
        ("eLearning Industry", "https://elearningindustry.com/feed"),
        ("EdTech Magazine", "https://edtechmagazine.com/k12/rss.xml"),
    ],
    "哲学・批判的思考": [
        ("Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/rss/sep.xml"),
        ("Philosophy Now", "https://philosophynow.org/rss"),
        ("The Conversation Philosophy", "https://theconversation.com/us/topics/philosophy/articles.atom"),
    ],
    "心理学・成長マインドセット": [
        ("APA Psychology News", "https://www.apa.org/rss/news.xml"),
        ("Mindset Works", "https://www.mindsetworks.com/feed"),
        ("Positive Psychology", "https://positivepsychology.com/feed/"),
    ],
}

KEYWORDS_FILTER = [
    "thinking", "critical thinking", "cognitive", "education", "learning",
    "brain", "mind", "intelligence", "creativity", "problem solving",
    "思考", "教育", "学習", "脳", "認知", "知能", "創造", "問題解決",
    "mindset", "growth", "metacognition", "reasoning",
]
