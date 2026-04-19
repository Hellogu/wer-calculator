"""
历史记录服务
封装历史记录相关的业务逻辑
"""
from typing import List, Optional, Dict, Any
from db.db_manager import DatabaseManager
from models.calculation_result import CalculationResultModel
from config import Config


class HistoryService:
    """历史记录服务"""
    
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
    
    def save_calculation(
        self,
        result: CalculationResultModel
    ) -> Dict[str, Any]:
        """保存计算记录"""
        try:
            record_id = self.db.save_record(result)
            return {
                'success': True,
                'id': record_id,
                'message': '保存成功'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_history_list(
        self,
        language: str = None,
        page: int = 1,
        page_size: int = None
    ) -> Dict[str, Any]:
        """获取历史记录列表"""
        try:
            if language:
                records = self.db.get_records_by_language(language)
            else:
                records = self.db.get_all_records()
            
            # 分页
            page_size = page_size or Config.DEFAULT_PAGE_SIZE
            total = len(records)
            start = (page - 1) * page_size
            end = start + page_size
            paginated_records = records[start:end]
            
            return {
                'success': True,
                'data': [r.to_dict() for r in paginated_records],
                'total': total,
                'page': page,
                'page_size': page_size
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_history(
        self,
        keyword: str,
        language: str = None
    ) -> Dict[str, Any]:
        """搜索历史记录"""
        try:
            records = self.db.search_records_by_title(keyword, language)
            
            return {
                'success': True,
                'data': [r.to_dict() for r in records],
                'total': len(records)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_title(
        self,
        record_id: int,
        title: str
    ) -> Dict[str, Any]:
        """更新记录标题"""
        try:
            success = self.db.update_record_title(record_id, title)
            if success:
                return {
                    'success': True,
                    'message': '更新成功'
                }
            else:
                return {
                    'success': False,
                    'error': '记录不存在'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_record(self, record_id: int) -> Dict[str, Any]:
        """删除记录"""
        try:
            success = self.db.delete_record(record_id)
            if success:
                return {
                    'success': True,
                    'message': '删除成功'
                }
            else:
                return {
                    'success': False,
                    'error': '记录不存在'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def clear_all(self) -> Dict[str, Any]:
        """清空所有记录"""
        try:
            count = self.db.clear_all_records()
            return {
                'success': True,
                'message': f'已清空 {count} 条记录'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_record_detail(self, record_id: int) -> Dict[str, Any]:
        """获取记录详情"""
        try:
            record = self.db.get_record_by_id(record_id)
            if record:
                return {
                    'success': True,
                    'data': record.to_dict()
                }
            else:
                return {
                    'success': False,
                    'error': '记录不存在'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取历史记录统计"""
        try:
            records = self.db.get_all_records()
            
            if not records:
                return {
                    'success': True,
                    'data': {
                        'total_records': 0,
                        'average_error_rate': 0,
                        'language_distribution': {},
                        'metric_distribution': {}
                    }
                }
            
            # 计算统计
            total_records = len(records)
            avg_error_rate = sum(r.result for r in records) / total_records
            
            # 语言分布
            lang_dist = {}
            for r in records:
                lang_dist[r.language] = lang_dist.get(r.language, 0) + 1
            
            # 指标分布
            metric_dist = {}
            for r in records:
                metric_dist[r.metric] = metric_dist.get(r.metric, 0) + 1
            
            return {
                'success': True,
                'data': {
                    'total_records': total_records,
                    'average_error_rate': round(avg_error_rate, 2),
                    'language_distribution': lang_dist,
                    'metric_distribution': metric_dist
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
