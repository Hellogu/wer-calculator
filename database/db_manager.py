"""
数据库管理器
统一管理数据库操作
"""
import sqlite3
import os
import json
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from datetime import datetime, timedelta

from ..config import Config
from ..models.calculation_result import CalculationResultModel, AlignmentItemModel


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._init_db()
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接（上下文管理器）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """初始化数据库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建历史记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    title TEXT DEFAULT '',
                    language TEXT NOT NULL,
                    metric TEXT NOT NULL,
                    result REAL NOT NULL,
                    total INTEGER NOT NULL,
                    substitutions INTEGER NOT NULL,
                    deletions INTEGER NOT NULL,
                    insertions INTEGER NOT NULL,
                    reference TEXT NOT NULL,
                    hypothesis TEXT NOT NULL,
                    alignment TEXT DEFAULT '[]'
                )
            ''')
    
    def save_record(self, record: CalculationResultModel) -> int:
        """保存记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            data = record.to_db_dict()
            
            # 确保时间戳使用 UTC+8
            if not data.get('timestamp'):
                data['timestamp'] = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO history 
                (timestamp, title, language, metric, result, total, 
                 substitutions, deletions, insertions, reference, hypothesis, alignment)
                VALUES 
                (:timestamp, :title, :language, :metric, :result, :total,
                 :substitutions, :deletions, :insertions, :reference, :hypothesis, :alignment)
            ''', data)
            
            return cursor.lastrowid
    
    def get_record_by_id(self, record_id: int) -> Optional[CalculationResultModel]:
        """根据ID获取记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM history WHERE id = ?', 
                (record_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return CalculationResultModel.from_db_dict(dict(row))
            return None
    
    def get_all_records(self) -> List[CalculationResultModel]:
        """获取所有记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM history ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            
            return [CalculationResultModel.from_db_dict(dict(row)) for row in rows]
    
    def get_records_by_language(self, language: str) -> List[CalculationResultModel]:
        """根据语言获取记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM history WHERE language = ? ORDER BY timestamp DESC',
                (language,)
            )
            rows = cursor.fetchall()
            
            return [CalculationResultModel.from_db_dict(dict(row)) for row in rows]
    
    def search_records_by_title(self, keyword: str, language: str = None) -> List[CalculationResultModel]:
        """根据标题搜索记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if language:
                cursor.execute('''
                    SELECT * FROM history 
                    WHERE title LIKE ? AND language = ?
                    ORDER BY timestamp DESC
                ''', (f'%{keyword}%', language))
            else:
                cursor.execute('''
                    SELECT * FROM history 
                    WHERE title LIKE ?
                    ORDER BY timestamp DESC
                ''', (f'%{keyword}%',))
            
            rows = cursor.fetchall()
            return [CalculationResultModel.from_db_dict(dict(row)) for row in rows]
    
    def update_record_title(self, record_id: int, title: str) -> bool:
        """更新记录标题"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE history SET title = ? WHERE id = ?',
                (title, record_id)
            )
            return cursor.rowcount > 0
    
    def delete_record(self, record_id: int) -> bool:
        """删除记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history WHERE id = ?', (record_id,))
            return cursor.rowcount > 0
    
    def clear_all_records(self) -> int:
        """清空所有记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history')
            return cursor.rowcount
