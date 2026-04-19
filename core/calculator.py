"""
核心计算模块
WER/CER 计算实现
"""
from typing import List, Tuple, Optional
from dataclasses import dataclass

from .text_processor import TextProcessor
from .number_normalizer import NumberNormalizer


@dataclass
class AlignmentItem:
    """对齐项"""
    ref: Optional[str]
    hyp: Optional[str]
    type: str  # 'correct', 'substitution', 'deletion', 'insertion'


@dataclass
class CalculationResult:
    """计算结果"""
    metric: str
    result: float
    substitutions: int
    deletions: int
    insertions: int
    total: int
    alignment: List[AlignmentItem]
    reference_processed: str
    hypothesis_processed: str


def calculate_wer_cer(
    reference: str,
    hypothesis: str,
    language: str = 'en',
    metric: str = 'wer'
) -> CalculationResult:
    """
    计算 WER/CER
    
    Args:
        reference: 参考文本
        hypothesis: 识别文本
        language: 语言 ('en', 'zh', 'ja')
        metric: 指标类型 ('wer' 或 'cer')
    
    Returns:
        CalculationResult 包含计算结果和对齐信息
    """
    # 文本预处理
    processor = TextProcessor(language)
    ref_processed = processor.process(reference)
    hyp_processed = processor.process(hypothesis)
    
    # 数字归一化（仅中文和英文）
    if language in ['zh', 'en']:
        normalizer = NumberNormalizer()
        ref_processed = normalizer.normalize(ref_processed, language)
        hyp_processed = normalizer.normalize(hyp_processed, language)
    
    # 分词
    if metric == 'wer':
        ref_items = ref_processed.split()
        hyp_items = hyp_processed.split()
    else:  # cer
        ref_items = list(ref_processed)
        hyp_items = list(hyp_processed)
    
    # 计算编辑距离和对齐
    distance, alignment = _compute_alignment(ref_items, hyp_items)
    
    # 统计错误
    substitutions = sum(1 for item in alignment if item.type == 'substitution')
    deletions = sum(1 for item in alignment if item.type == 'deletion')
    insertions = sum(1 for item in alignment if item.type == 'insertion')
    total = len(ref_items)
    
    # 计算错误率
    if total > 0:
        result = ((substitutions + deletions + insertions) / total) * 100
    else:
        result = 0.0
    
    return CalculationResult(
        metric=metric.upper(),
        result=round(result, 2),
        substitutions=substitutions,
        deletions=deletions,
        insertions=insertions,
        total=total,
        alignment=alignment,
        reference_processed=ref_processed,
        hypothesis_processed=hyp_processed
    )


def _compute_alignment(
    ref_items: List[str],
    hyp_items: List[str]
) -> Tuple[int, List[AlignmentItem]]:
    """
    计算对齐
    
    Args:
        ref_items: 参考文本分词结果
        hyp_items: 识别文本分词结果
    
    Returns:
        (编辑距离, 对齐列表)
    """
    m, n = len(ref_items), len(hyp_items)
    
    # 动态规划矩阵
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # 填充矩阵
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_items[i - 1] == hyp_items[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # 删除
                    dp[i][j - 1],      # 插入
                    dp[i - 1][j - 1]   # 替换
                )
    
    # 回溯找对齐路径
    alignment = _backtrack(dp, ref_items, hyp_items, m, n)
    
    return dp[m][n], alignment


def _backtrack(
    dp: List[List[int]],
    ref_items: List[str],
    hyp_items: List[str],
    i: int,
    j: int
) -> List[AlignmentItem]:
    """
    回溯找对齐路径
    
    Args:
        dp: 动态规划矩阵
        ref_items: 参考文本分词结果
        hyp_items: 识别文本分词结果
        i: 当前行索引
        j: 当前列索引
    
    Returns:
        对齐列表
    """
    alignment = []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref_items[i - 1] == hyp_items[j - 1]:
            # 匹配
            alignment.append(AlignmentItem(
                ref=ref_items[i - 1],
                hyp=hyp_items[j - 1],
                type='correct'
            ))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # 替换
            alignment.append(AlignmentItem(
                ref=ref_items[i - 1],
                hyp=hyp_items[j - 1],
                type='substitution'
            ))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # 删除
            alignment.append(AlignmentItem(
                ref=ref_items[i - 1],
                hyp=None,
                type='deletion'
            ))
            i -= 1
        else:
            # 插入
            alignment.append(AlignmentItem(
                ref=None,
                hyp=hyp_items[j - 1],
                type='insertion'
            ))
            j -= 1
    
    alignment.reverse()
    return alignment
