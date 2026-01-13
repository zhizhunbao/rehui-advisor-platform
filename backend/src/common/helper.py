"""
集中管理所有工具函数

使用方式:
    from src.common.helper import format_datetime, generate_id, truncate
"""
import re
from datetime import datetime, timezone
from uuid import uuid4


# ========== ID 生成 ==========
def generate_id() -> str:
    """生成 UUID"""
    return str(uuid4())


def generate_short_id(length: int = 8) -> str:
    """生成短 ID"""
    return uuid4().hex[:length]


# ========== 时间处理 ==========
def now_utc() -> datetime:
    """获取当前 UTC 时间"""
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime | None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    if dt is None:
        return ""
    return dt.strftime(fmt)


def format_date(dt: datetime | None, fmt: str = "%Y-%m-%d") -> str:
    """格式化日期"""
    if dt is None:
        return ""
    return dt.strftime(fmt)


# ========== 字符串处理 ==========
def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断字符串"""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def slugify(text: str) -> str:
    """转换为 URL 友好的 slug"""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def capitalize_first(text: str) -> str:
    """首字母大写"""
    if not text:
        return text
    return text[0].upper() + text[1:]


# ========== 文件处理 ==========
def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def get_file_extension(filename: str) -> str:
    """获取文件扩展名（小写）"""
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[-1].lower()


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除不安全字符"""
    # 移除路径分隔符和其他危险字符
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    # 移除控制字符
    filename = re.sub(r"[\x00-\x1f\x7f]", "", filename)
    return filename.strip()


# ========== 数据处理 ==========
def safe_get(data: dict, *keys, default=None):
    """安全获取嵌套字典值"""
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data


def remove_none(data: dict) -> dict:
    """移除字典中值为 None 的键"""
    return {k: v for k, v in data.items() if v is not None}


def chunk_list(lst: list, size: int) -> list[list]:
    """将列表分块"""
    return [lst[i : i + size] for i in range(0, len(lst), size)]


# ========== 分页处理 ==========
def paginate(items: list, page: int = 1, limit: int = 20) -> tuple[list, int]:
    """
    对列表进行分页
    
    Args:
        items: 要分页的列表
        page: 页码（从 1 开始）
        limit: 每页数量
    
    Returns:
        (分页后的列表, 总数)
    
    使用示例:
        items, total = paginate(all_items, page=2, limit=10)
    """
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    return items[start:end], total


def paginate_with_meta(
    items: list, 
    page: int = 1, 
    limit: int = 20
) -> dict:
    """
    对列表进行分页，返回包含元数据的字典
    
    Returns:
        {
            "items": [...],
            "total": 100,
            "page": 1,
            "limit": 20,
            "pages": 5,
            "has_next": True,
            "has_prev": False
        }
    """
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    pages = (total + limit - 1) // limit if limit > 0 else 0
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
    }
