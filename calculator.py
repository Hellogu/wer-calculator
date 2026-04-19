"""
计算器模块（兼容层）
为了保持向后兼容，此模块导出新的核心模块功能
"""
from core.calculator import calculate_wer_cer, CalculationResult, AlignmentItem
from core.compat import preprocess_text, normalize_numbers

# 保持向后兼容的导出
__all__ = [
    'calculate_wer_cer',
    'CalculationResult',
    'AlignmentItem',
    'preprocess_text',
    'normalize_numbers',
]
