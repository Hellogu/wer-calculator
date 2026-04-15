"""
SQLite 数据库操作
"""
import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = 'wer_calculator.db'


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    if not os.path.exists(DB_PATH):
        create_table()


def create_table():
    """创建历史记录表"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            title VARCHAR(255),
            language VARCHAR(10) NOT NULL,
            metric VARCHAR(10) NOT NULL,
            result REAL NOT NULL,
            total INTEGER NOT NULL,
            substitutions INTEGER NOT NULL,
            deletions INTEGER NOT NULL,
            insertions INTEGER NOT NULL,
            reference TEXT NOT NULL,
            hypothesis TEXT NOT NULL,
            alignment TEXT
        )
    ''')

    conn.commit()
    conn.close()


def migrate_add_alignment():
    """迁移：添加 alignment 字段到现有表"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 检查 alignment 字段是否存在
    cursor.execute("PRAGMA table_info(history)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'alignment' not in columns:
        cursor.execute('ALTER TABLE history ADD COLUMN alignment TEXT')
        conn.commit()

    conn.close()


def get_utc8_time():
    """获取 UTC+8 时间"""
    return datetime.utcnow() + timedelta(hours=8)


def save_record(title: str, language: str, metric: str, result: float, total: int,
                substitutions: int, deletions: int, insertions: int,
                reference: str, hypothesis: str, alignment: str = None) -> int:
    """
    保存计算记录（包含详细统计）
    返回：记录ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 使用 UTC+8 时间
    timestamp = get_utc8_time().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO history (timestamp, title, language, metric, result, total, substitutions, deletions, insertions, reference, hypothesis, alignment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, title, language, metric, result, total, substitutions, deletions, insertions, reference, hypothesis, alignment))

    record_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return record_id


def get_all_records() -> list:
    """
    获取所有历史记录
    返回：记录列表
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, timestamp, title, language, metric, result, total, substitutions, deletions, insertions, reference, hypothesis, alignment
        FROM history
        ORDER BY timestamp DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    # 转换为字典列表
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'timestamp': row['timestamp'],
            'title': row['title'],
            'language': row['language'],
            'metric': row['metric'],
            'result': row['result'],
            'total': row['total'],
            'substitutions': row['substitutions'],
            'deletions': row['deletions'],
            'insertions': row['insertions'],
            'reference': row['reference'],
            'hypothesis': row['hypothesis'],
            'alignment': row['alignment']
        })

    return records


def get_records_by_language(language: str) -> list:
    """
    按语言获取历史记录
    返回：记录列表
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, timestamp, title, language, metric, result, total, substitutions, deletions, insertions, reference, hypothesis, alignment
        FROM history
        WHERE language = ?
        ORDER BY timestamp DESC
    ''', (language,))

    rows = cursor.fetchall()
    conn.close()

    # 转换为字典列表
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'timestamp': row['timestamp'],
            'title': row['title'],
            'language': row['language'],
            'metric': row['metric'],
            'result': row['result'],
            'total': row['total'],
            'substitutions': row['substitutions'],
            'deletions': row['deletions'],
            'insertions': row['insertions'],
            'reference': row['reference'],
            'hypothesis': row['hypothesis'],
            'alignment': row['alignment']
        })

    return records


def get_record_by_id(record_id: int) -> dict:
    """
    根据ID获取单条记录
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, timestamp, title, language, metric, result, total, substitutions, deletions, insertions, reference, hypothesis, alignment
        FROM history
        WHERE id = ?
    ''', (record_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'id': row['id'],
            'timestamp': row['timestamp'],
            'title': row['title'],
            'language': row['language'],
            'metric': row['metric'],
            'result': row['result'],
            'total': row['total'],
            'substitutions': row['substitutions'],
            'deletions': row['deletions'],
            'insertions': row['insertions'],
            'reference': row['reference'],
            'hypothesis': row['hypothesis'],
            'alignment': row['alignment']
        }
    return None


def delete_record(record_id: int) -> bool:
    """
    删除单条记录
    返回：是否成功
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM history WHERE id = ?', (record_id,))
    
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    
    return affected > 0


def clear_all_records() -> bool:
    """
    清空所有记录
    返回：是否成功
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM history')
    
    conn.commit()
    conn.close()
    
    return True


def update_record_title(record_id: int, title: str) -> bool:
    """
    更新记录标题
    返回：是否成功
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE history SET title = ? WHERE id = ?', (title, record_id))
    
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    
    return affected > 0


def search_records_by_title(keyword: str, language: str = None) -> list:
    """
    按标题关键词搜索历史记录
    参数：
        keyword: 搜索关键词
        language: 可选，按语言过滤
    返回：记录列表
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 使用 LIKE 进行模糊搜索
    search_pattern = f'%{keyword}%'
    
    if language:
        cursor.execute('''
            SELECT id, timestamp, title, language, metric, result, total, substitutions, deletions, insertions, reference, hypothesis, alignment
            FROM history
            WHERE title LIKE ? AND language = ?
            ORDER BY timestamp DESC
        ''', (search_pattern, language))
    else:
        cursor.execute('''
            SELECT id, timestamp, title, language, metric, result, total, substitutions, deletions, insertions, reference, hypothesis, alignment
            FROM history
            WHERE title LIKE ?
            ORDER BY timestamp DESC
        ''', (search_pattern,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # 转换为字典列表
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'timestamp': row['timestamp'],
            'title': row['title'],
            'language': row['language'],
            'metric': row['metric'],
            'result': row['result'],
            'total': row['total'],
            'substitutions': row['substitutions'],
            'deletions': row['deletions'],
            'insertions': row['insertions'],
            'reference': row['reference'],
            'hypothesis': row['hypothesis'],
            'alignment': row['alignment']
        })
    
    return records
