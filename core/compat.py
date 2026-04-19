"""
兼容层模块
提供新旧代码的兼容性支持
"""
from .calculator import calculate_wer_cer, CalculationResult, AlignmentItem
from .text_processor import TextProcessor
from .number_normalizer import NumberNormalizer


# 保持向后兼容的函数导出
def preprocess_text(text: str, language: str) -> str:
    """
    预处理文本（兼容旧接口）
    """
    processor = TextProcessor(language)
    result = processor.process(text)
    
    # 数字归一化（仅中文和英文）
    if language in ['zh', 'en']:
        normalizer = NumberNormalizer()
        result = normalizer.normalize(result, language)
    
    return result


def normalize_numbers(text: str, language: str) -> str:
    """
    数字归一化（兼容旧接口）
    """
    normalizer = NumberNormalizer()
    return normalizer.normalize(text, language)


# 导出新旧接口
__all__ = [
    'calculate_wer_cer',
    'CalculationResult',
    'AlignmentItem',
    'TextProcessor',
    'NumberNormalizer',
    'preprocess_text',
    'normalize_numbers',
]
