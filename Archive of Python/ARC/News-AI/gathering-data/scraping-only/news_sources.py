# news_sources.py

NEWS_SOURCES = [
    # BBC News
    {
        'name': 'BBC News',
        'base_url': 'https://www.bbc.com',
        'url': 'https://www.bbc.com/news',
        'selectors': {
            'article_links': 'a[href*="/news/"]',
            'title': 'h1',
            'content': ['div[data-component="text-block"]', 'article']
        },
        'max_articles': 15
    },
    
    # Reuters
    {
        'name': 'Reuters',
        'base_url': 'https://www.reuters.com',
        'url': 'https://www.reuters.com/world/',
        'selectors': {
            'article_links': 'a[href*="/world/"]',
            'title': 'h1',
            'content': ['div[data-testid="ArticleBody"]', 'div[class*="ArticleBody"]']
        },
        'max_articles': 15
    },
    
    # CNN
    {
        'name': 'CNN',
        'base_url': 'https://www.cnn.com',
        'url': 'https://www.cnn.com/world',
        'selectors': {
            'article_links': 'a[href*="/2024/"]',
            'title': 'h1',
            'content': ['.article__content', 'article']
        },
        'max_articles': 10
    },
    
    # Al Jazeera
    {
        'name': 'Al Jazeera',
        'base_url': 'https://www.aljazeera.com',
        'url': 'https://www.aljazeera.com/news/',
        'selectors': {
            'article_links': 'a[href*="/news/"]',
            'title': 'h1',
            'content': ['.wysiwyg', '.article-content']
        },
        'max_articles': 10
    },
    
    # The Guardian
    {
        'name': 'The Guardian',
        'base_url': 'https://www.theguardian.com',
        'url': 'https://www.theguardian.com/world',
        'selectors': {
            'article_links': 'a[href*="/world/"]',
            'title': 'h1',
            'content': ['.article-body-commercial-selector', 'article']
        },
        'max_articles': 10
    },
    
    # Financial Times
    {
        'name': 'Financial Times',
        'base_url': 'https://www.ft.com',
        'url': 'https://www.ft.com/world',
        'selectors': {
            'article_links': 'a[href*="/content/"]',
            'title': 'h1',
            'content': ['.article__content', '.content-body']
        },
        'max_articles': 8
    },
    
    # AP News
    {
        'name': 'AP News',
        'base_url': 'https://apnews.com',
        'url': 'https://apnews.com/hub/world-news',
        'selectors': {
            'article_links': 'a[href*="/article/"]',
            'title': 'h1',
            'content': ['.RichTextStoryBody', '.Article']
        },
        'max_articles': 12
    },
    
    # Bloomberg
    {
        'name': 'Bloomberg',
        'base_url': 'https://www.bloomberg.com',
        'url': 'https://www.bloomberg.com/world',
        'selectors': {
            'article_links': 'a[href*="/news/articles/"]',
            'title': 'h1',
            'content': ['.body-copy', '.article-body']
        },
        'max_articles': 8
    }
]

# Template for adding new sources:
"""
{
    'name': 'Source Name',
    'base_url': 'https://www.example.com',
    'url': 'https://www.example.com/news',
    'selectors': {
        'article_links': 'a[href*="/article/"]',  # CSS selector for article links
        'title': 'h1',                           # CSS selector for article title
        'content': ['.article-content', 'article']  # List of CSS selectors for content (in order of preference)
    },
    'max_articles': 10  # Maximum number of articles to scrape per collection
}
"""
