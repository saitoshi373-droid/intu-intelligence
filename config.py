import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GMAIL_USER = os.getenv("GMAIL_USER", "saitoshi373@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO", "saitoshi373@gmail.com")

RSS_SOURCES = {
    "思考力・認知科学": [
        ("MindShift KQED", "https://www.kqed.org/mindshift/feed"),
        ("Big Think", "https://bigthink.com/feed/"),
        ("Greater Good Science Center", "https://greatergood.berkeley.edu/feeds/news"),
        ("The Conversation - Psychology", "https://theconversation.com/us/topics/psychology/articles.atom"),
    ],
    "日本の教育": [
        ("文部科学省", "https://www.mext.go.jp/rss/index.xml"),
        ("NHK教育・文化", "https://www3.nhk.or.jp/rss/news/cat05.xml"),
        ("教育新聞", "https://www.kyobun.co.jp/feed/"),
        ("朝日新聞教育", "https://www.asahi.com/rss/asahi/edu.rdf"),
    ],
    "海外の教育": [
        ("Education Week", "https://www.edweek.org/feed"),
        ("The Guardian Education", "https://www.theguardian.com/education/rss"),
        ("MIT News Education", "https://news.mit.edu/rss/topic/education"),
        ("OECD Education Today", "https://oecdedutoday.com/feed/"),
    ],
    "脳科学・神経科学": [
        ("Neuroscience News", "https://neurosciencenews.com/feed/"),
        ("Dana Foundation", "https://dana.org/news/feed/"),
        ("Scientific American", "https://www.scientificamerican.com/feed/"),
    ],
    "TQテスト関連": [
        ("Assessment Research", "https://www.tandfonline.com/feed/rss/rced20"),
        ("Educational Measurement", "https://onlinelibrary.wiley.com/feed/rss/14756986"),
        ("The Conversation - Education", "https://theconversation.com/us/topics/education/articles.atom"),
    ],
    "アイデアクエスト関連": [
        ("Creativity Research Journal", "https://www.tandfonline.com/feed/rss/hcrj20"),
        ("Psychology of Creativity", "https://www.psychologytoday.com/intl/basics/creativity/feed"),
        ("IDEO Design Thinking", "https://www.ideo.com/feed"),
    ],
    "偉人・著名人の名言": [
        ("BrainyQuote RSS", "https://www.brainyquote.com/feeds/authors"),
        ("Farnam Street", "https://fs.blog/feed/"),
        ("Brain Pickings / The Marginalian", "https://www.themarginalian.org/feed/"),
    ],
    "権威・専門家の発言": [
        ("Brookings Education", "https://www.brookings.edu/topic/education/feed/"),
        ("Stanford Education", "https://ed.stanford.edu/news/rss.xml"),
        ("MIT News - Learning", "https://news.mit.edu/rss/topic/learning"),
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
    "哲学・論理学": [
        ("Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/rss/sep.xml"),
        ("Philosophy Now", "https://philosophynow.org/rss"),
        ("3 Quarks Daily Philosophy", "https://3quarksdaily.com/category/philosophy/feed"),
    ],
    "心理学・マインドセット": [
        ("APA Psychology News", "https://www.apa.org/rss/news.xml"),
        ("Positive Psychology", "https://positivepsychology.com/feed/"),
        ("Mindset Works", "https://www.mindsetworks.com/feed"),
    ],
    "歴史×教育の変遷": [
        ("History of Education Society", "https://www.historyofeducation.org.uk/feed/"),
        ("Paedagogica Historica", "https://www.tandfonline.com/feed/rss/cpdh20"),
        ("Aeon - Education", "https://aeon.co/feed.rss"),
    ],
    "政府・政策動向": [
        ("UNESCO Education", "https://www.unesco.org/en/education/rss.xml"),
        ("OECD iLibrary Education", "https://www.oecd-ilibrary.org/education_rss.xml"),
        ("World Bank Education", "https://blogs.worldbank.org/education/feed"),
    ],
    "競合・類似サービス": [
        ("EdSurge Products", "https://www.edsurge.com/products.rss"),
        ("Product Hunt Education", "https://www.producthunt.com/feed?category=education"),
        ("TechCrunch EdTech", "https://techcrunch.com/tag/edtech/feed/"),
    ],
    "動画・YouTube": [
        ("TED Education", "https://www.ted.com/talks/rss"),
        ("Big Think Video", "https://bigthink.com/videos/feed/"),
    ],
    "SNS上の思考力議論": [
        ("Hacker News", "https://hnrss.org/frontpage?q=thinking+education+learning"),
        ("Reddit r/education", "https://www.reddit.com/r/education/.rss"),
        ("Reddit r/cognitivescience", "https://www.reddit.com/r/cognitivescience/.rss"),
    ],
}

KEYWORDS_FILTER = [
    "thinking", "critical thinking", "cognitive", "education", "learning",
    "brain", "mind", "intelligence", "creativity", "problem solving",
    "思考", "教育", "学習", "脳", "認知", "知能", "創造", "問題解決",
    "mindset", "growth", "metacognition", "reasoning", "philosophy",
    "quote", "wisdom", "research", "study", "assessment",
]

ALL_CATEGORIES = list(RSS_SOURCES.keys())
