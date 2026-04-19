"""
数据库模块（兼容层）
为了保持向后兼容，此模块导出新的数据库管理器功能
"""
from db.db_manager import DatabaseManager
from config import Config

# 创建全局数据库管理器实例
_db_manager = DatabaseManager()

# 为了保持向后兼容，导出旧接口
def get_db_connection():
    """获取数据库连接（兼容旧接口）"""
    import sqlite3
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库（兼容旧接口）"""
    pass  # 新的 DatabaseManager 会自动初始化

def create_table():
    """创建表（兼容旧接口）"""
    pass  # 新的 DatabaseManager 会自动创建

def migrate_add_alignment():
    """迁移 alignment 字段（兼容旧接口）"""
    pass  # 新的 DatabaseManager 已包含此功能

def get_utc8_time():
    """获取 UTC+8 时间（兼容旧接口）"""
    from datetime import datetime, timedelta
    return datetime.utcnow() + timedelta(hours=8)

def save_record(title: str, language: str, metric: str, result: float, total: int,
                substitutions: int, deletions: int, insertions: int,
                reference: str, hypothesis: str, alignment: str = None) -> int:
    """保存记录（兼容旧接口）"""
    from models.calculation_result import CalculationResultModel, AlignmentItemModel
    import json
    
    # 解析 alignment
    alignment_list = []
    if alignment:
        try:
            alignment_data = json.loads(alignment)
            alignment_list = [AlignmentItemModel(**item) for item in alignment_data]
        except:
            pass
    
    record = CalculationResultModel(
        title=title,
        language=language,
        metric=metric,
        result=result,
        total=total,
        substitutions=substitutions,
        deletions=deletions,
        insertions=insertions,
        reference=reference,
        hypothesis=hypothesis,
        alignment=alignment_list
    )
    
    return _db_manager.save_record(record)

def get_all_records() -> list:
    """获取所有记录（兼容旧接口）"""
    records = _db_manager.get_all_records()
    return [record.to_db_dict() for record in records]

def get_records_by_language(language: str) -> list:
    """根据语言获取记录（兼容旧接口）"""
    records = _db_manager.get_records_by_language(language)
    return [record.to_db_dict() for record in records]

def search_records_by_title(keyword: str, language: str = None) -> list:
    """搜索记录（兼容旧接口）"""
    records = _db_manager.search_records_by_title(keyword, language)
    return [record.to_db_dict() for record in records]

def update_record_title(record_id: int, title: str) -> bool:
    """更新记录标题（兼容旧接口）"""
    return _db_manager.update_record_title(record_id, title)

def delete_record(record_id: int) -> bool:
    """删除记录（兼容旧接口）"""
    return _db_manager.delete_record(record_id)

def clear_all_records() -> int:
    """清空所有记录（兼容旧接口）"""
    return _db_manager.clear_all_records()

def get_record_by_id(record_id: int):
    """根据ID获取记录（兼容旧接口）"""
    record = _db_manager.get_record_by_id(record_id)
    if record:
        return record.to_db_dict()
    return None

# 导出 DatabaseManager 供新代码使用
__all__ = [
    'DatabaseManager',
    'get_db_connection',
    'init_db',
    'create_table',
    'migrate_add_alignment',
    'get_utc8_time',
    'save_record',
    'get_all_records',
    'get_records_by_language',
    'search_records_by_title',
    'update_record_title',
    'delete_record',
    'clear_all_records',
    'get_record_by_id',
]
