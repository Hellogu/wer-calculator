"""
计算服务
封装计算相关的业务逻辑
"""
from typing import Dict, Any, Tuple
from core.calculator import calculate_wer_cer
from models.calculation_result import CalculationResultModel, AlignmentItemModel


class CalculationService:
    """计算服务"""
    
    def calculate(
        self,
        reference: str,
        hypothesis: str,
        language: str = 'en',
        metric: str = 'wer',
        title: str = ''
    ) -> CalculationResultModel:
        """
        执行计算
        
        Args:
            reference: 参考文本
            hypothesis: 识别文本
            language: 语言
            metric: 指标类型
            title: 标题
        
        Returns:
            CalculationResultModel
        """
        # 执行核心计算
        result = calculate_wer_cer(reference, hypothesis, language, metric)
        
        # 转换为模型
        alignment_models = [
            AlignmentItemModel(
                ref=item.ref,
                hyp=item.hyp,
                type=item.type
            )
            for item in result.alignment
        ]
        
        return CalculationResultModel(
            title=title,
            language=language,
            reference=reference,
            hypothesis=hypothesis,
            metric=result.metric,
            result=result.result,
            substitutions=result.substitutions,
            deletions=result.deletions,
            insertions=result.insertions,
            total=result.total,
            alignment=alignment_models
        )
    
    def validate_input(
        self,
        reference: str,
        hypothesis: str,
        language: str
    ) -> Dict[str, Any]:
        """验证输入"""
        errors = {}
        
        if not reference or not reference.strip():
            errors['reference'] = '参考文本不能为空'
        
        if not hypothesis or not hypothesis.strip():
            errors['hypothesis'] = '识别文本不能为空'
        
        if language not in ['en', 'zh', 'ja']:
            errors['language'] = '不支持的语言'
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def get_statistics(self, result: CalculationResultModel) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'error_rate': result.result,
            'substitutions': result.substitutions,
            'deletions': result.deletions,
            'insertions': result.insertions,
            'total': result.total,
            'correct': result.total - result.substitutions - result.deletions,
            'error_breakdown': {
                'substitution_rate': (result.substitutions / result.total * 100) if result.total > 0 else 0,
                'deletion_rate': (result.deletions / result.total * 100) if result.total > 0 else 0,
                'insertion_rate': (result.insertions / result.total * 100) if result.total > 0 else 0,
            }
        }
