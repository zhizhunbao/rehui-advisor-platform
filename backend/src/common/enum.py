"""
集中管理所有业务枚举

使用方式:
    from src.common.enum import UserStatus, FileType, AssignmentStatus
"""
from enum import Enum


# ========== 用户相关 ==========
class UserType(str, Enum):
    """用户类型"""
    MEMBER = "member"
    ADMIN = "admin"


class UserStatus(str, Enum):
    """用户状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


# ========== 文件相关 ==========
class FileType(str, Enum):
    """文件类型"""
    DOCX = "docx"
    PDF = "pdf"
    NOTEBOOK = "notebook"  # .ipynb
    MARKDOWN = "markdown"
    IMAGE = "image"
    OTHER = "other"


# ========== 学习模块 ==========
class AssignmentStatus(str, Enum):
    """作业状态"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"


class ResourceType(str, Enum):
    """资源类型"""
    LINK = "link"
    PAPER = "paper"
    TUTORIAL = "tutorial"
    DOCS = "docs"
    VIDEO = "video"
    OTHER = "other"


# ========== 通用状态 ==========
class EntityStatus(str, Enum):
    """通用实体状态"""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ========== 数据源 ==========
class DataSourceType(str, Enum):
    """数据源类型"""
    LOCAL = "local"
    SUPABASE = "supabase"
    EXTERNAL = "external"


# ========== 保险模块 ==========
class InsuranceType(str, Enum):
    """保险类型"""
    AUTO = "AUTO"
    HOME = "HOME"
    HEALTH = "HEALTH"
    LIFE = "LIFE"
    RENTERS = "RENTERS"


class InsuranceProviderCode(str, Enum):
    """保险提供商代码"""
    GEICO = "GEICO"
    STATE_FARM = "STATE_FARM"
    PROGRESSIVE = "PROGRESSIVE"
    ALLSTATE = "ALLSTATE"
    FARMERS = "FARMERS"
    USAA = "USAA"
    LIBERTY_MUTUAL = "LIBERTY_MUTUAL"


# ========== 外部 API ==========
GITHUB_API = "https://api.github.com"
RAW_GITHUB = "https://raw.githubusercontent.com"


# ========== 国际化 ==========
class Language(str, Enum):
    """语言"""
    ZH = "zh"
    EN = "en"


class MessageRole(str, Enum):
    """消息角色"""
    USER = "user"
    ASSISTANT = "assistant"
