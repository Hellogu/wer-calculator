"""
数据模型模块
定义计算结果的数据结构
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class AlignmentItemModel:
    """对齐项模型"""
    ref: Optional[str]
    hyp: Optional[str]
    type: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ref': self.ref,
            'hyp': self.hyp,
            'type': self.type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AlignmentItemModel':
        return cls(
            ref=data.get('ref'),
            hyp=data.get('hyp'),
            type=data['type']
        )


@dataclass
class CalculationResultModel:
    """计算结果模型"""
    id: Optional[int] = None
    title: str = ''
    timestamp: str = ''
    language: str = 'en'
    reference: str = ''
    hypothesis: str = ''
    metric: str = 'WER'
    result: float = 0.0
    substitutions: int = 0
    deletions: int = 0
    insertions: int = 0
    total: int = 0
    alignment: List[AlignmentItemModel] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'timestamp': self.timestamp,
            'language': self.language,
            'reference': self.reference,
            'hypothesis': self.hypothesis,
            'metric': self.metric,
            'result': self.result,
            'substitutions': self.substitutions,
            'deletions': self.deletions,
            'insertions': self.insertions,
            'total': self.total,
            'alignment': [item.to_dict() for item in self.alignment]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculationResultModel':
        alignment_data = data.get('alignment', [])
        alignment = [AlignmentItemModel.from_dict(item) for item in alignment_data]
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            timestamp=data.get('timestamp', ''),
            language=data.get('language', 'en'),
            reference=data.get('reference', ''),
            hypothesis=data.get('hypothesis', ''),
            metric=data.get('metric', 'WER'),
            result=data.get('result', 0.0),
            substitutions=data.get('substitutions', 0),
            deletions=data.get('deletions', 0),
            insertions=data.get('insertions', 0),
            total=data.get('total', 0),
            alignment=alignment
        )
    
    def to_db_dict(self) -> Dict[str, Any]:
        """转换为数据库格式"""
        return {
            'id': self.id,
            'title': self.title,
            'timestamp': self.timestamp,
            'language': self.language,
            'reference': self.reference,
            'hypothesis': self.hypothesis,
            'metric': self.metric,
            'result': self.result,
            'substitutions': self.substitutions,
            'deletions': self.deletions,
            'insertions': self.insertions,
            'total': self.total,
            'alignment': json.dumps([item.to_dict() for item in self.alignment])
        }
    
    @classmethod
    def from_db_dict(cls, data: Dict[str, Any]) -> 'CalculationResultModel':
        """从数据库格式创建"""
        alignment_json = data.get('alignment', '[]')
        try:
            alignment_data = json.loads(alignment_json)
            alignment = [AlignmentItemModel.from_dict(item) for item in alignment_data]
        except json.JSONDecodeError:
            alignment = []
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            timestamp=data.get('timestamp', ''),
            language=data.get('language', 'en'),
            reference=data.get('reference', ''),
            hypothesis=data.get('hypothesis', ''),
            metric=data.get('metric', 'WER'),
            result=data.get('result', 0.0),
            substitutions=data.get('substitutions', 0),
            deletions=data.get('deletions', 0),
            insertions=data.get('insertions', 0),
            total=data.get('total', 0),
            alignment=alignment
        )
