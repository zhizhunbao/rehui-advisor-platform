# 发现脚本 - 从各平台发现新资源
from scripts.data.discover.discover_github import DiscoverGitHubScript
from scripts.data.discover.discover_hackernews import DiscoverHackerNewsScript
from scripts.data.discover.discover_reddit import DiscoverRedditScript
from scripts.data.discover.discover_huggingface import DiscoverHuggingFaceScript
from scripts.data.discover.discover_stackoverflow import DiscoverStackOverflowScript
from scripts.data.discover.discover_devto import DiscoverDevToScript
from scripts.data.discover.discover_producthunt import DiscoverProductHuntScript
from scripts.data.discover.discover_rss import DiscoverRSSScript
from scripts.data.discover.discover_awesome import DiscoverAwesomeScript
from scripts.data.discover.discover_medium import DiscoverMediumScript

__all__ = [
    "DiscoverGitHubScript",
    "DiscoverHackerNewsScript",
    "DiscoverRedditScript",
    "DiscoverHuggingFaceScript",
    "DiscoverStackOverflowScript",
    "DiscoverDevToScript",
    "DiscoverProductHuntScript",
    "DiscoverRSSScript",
    "DiscoverAwesomeScript",
    "DiscoverMediumScript",
]
