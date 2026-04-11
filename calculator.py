"""
WER/CER 计算核心算法
"""
import re


def preprocess_text(text: str, language: str) -> str:
    """
    预处理文本
    - 去除多余空格
    - 英文转小写
    - 去除特殊符号（保留字母、数字、中日文）
    """
    # 首先去除多余空格，合并成一个空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 英文转小写
    if language == 'en':
        text = text.lower()
        # 英文：只保留字母、数字和空格（用于分词）
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # 再次清理多余空格
        text = re.sub(r'\s+', ' ', text).strip()
    elif language == 'zh':
        # 中文：只保留中文字符
        text = re.sub(r'[^\u4e00-\u9fff]', '', text)
    elif language == 'ja':
        # 日文：只保留日文假名和汉字
        text = re.sub(r'[^\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]', '', text)

    return text


def backtrack(dp_matrix, ref_items, hyp_items):
    """
    回溯找对齐路径
    """
    i, j = len(ref_items), len(hyp_items)
    alignment = []

    while i > 0 or j > 0:
        if i == 0:
            # 只剩插入
            alignment.append({
                'type': 'insertion',
                'ref': None,
                'hyp': hyp_items[j - 1]
            })
            j -= 1
        elif j == 0:
            # 只剩删除
            alignment.append({
                'type': 'deletion',
                'ref': ref_items[i - 1],
                'hyp': None
            })
            i -= 1
        else:
            # 比较三个方向
            substitution_cost = dp_matrix[i - 1][j - 1]
            deletion_cost = dp_matrix[i - 1][j]
            insertion_cost = dp_matrix[i][j - 1]
            current_cost = dp_matrix[i][j]

            if ref_items[i - 1] == hyp_items[j - 1]:
                # 正确匹配
                alignment.append({
                    'type': 'correct',
                    'ref': ref_items[i - 1],
                    'hyp': hyp_items[j - 1]
                })
                i -= 1
                j -= 1
            elif current_cost == substitution_cost + 1:
                # 替换
                alignment.append({
                    'type': 'substitution',
                    'ref': ref_items[i - 1],
                    'hyp': hyp_items[j - 1]
                })
                i -= 1
                j -= 1
            elif current_cost == deletion_cost + 1:
                # 删除
                alignment.append({
                    'type': 'deletion',
                    'ref': ref_items[i - 1],
                    'hyp': None
                })
                i -= 1
            else:
                # 插入
                alignment.append({
                    'type': 'insertion',
                    'ref': None,
                    'hyp': hyp_items[j - 1]
                })
                j -= 1

    # 反转对齐结果（从后往前回溯的）
    alignment.reverse()
    return alignment


def calculate_wer(reference: str, hypothesis: str) -> dict:
    """
    计算英文 WER (Word Error Rate)
    按词（word）分割计算
    """
    # 按空格分割成词列表
    ref_words = reference.split()
    hyp_words = hypothesis.split()

    if len(ref_words) == 0:
        return {
            'metric': 'WER',
            'result': 0.0,
            'total': 0,
            'substitutions': 0,
            'deletions': 0,
            'insertions': 0,
            'alignment': []
        }

    # 动态规划矩阵
    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]

    # 初始化
    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j

    # 填表
    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                deletion = d[i - 1][j] + 1
                insertion = d[i][j - 1] + 1
                d[i][j] = min(substitution, deletion, insertion)

    # 回溯找对齐
    alignment = backtrack(d, ref_words, hyp_words)

    # 统计
    substitutions = sum(1 for a in alignment if a['type'] == 'substitution')
    deletions = sum(1 for a in alignment if a['type'] == 'deletion')
    insertions = sum(1 for a in alignment if a['type'] == 'insertion')

    wer = (substitutions + deletions + insertions) / len(ref_words) * 100

    return {
        'metric': 'WER',
        'result': round(wer, 2),
        'total': len(ref_words),
        'substitutions': substitutions,
        'deletions': deletions,
        'insertions': insertions,
        'alignment': alignment
    }


def calculate_cer(reference: str, hypothesis: str) -> dict:
    """
    计算中/日文 CER (Character Error Rate)
    按字符分割计算
    """
    ref_chars = list(reference)
    hyp_chars = list(hypothesis)

    if len(ref_chars) == 0:
        return {
            'metric': 'CER',
            'result': 0.0,
            'total': 0,
            'substitutions': 0,
            'deletions': 0,
            'insertions': 0,
            'alignment': []
        }

    # 动态规划矩阵
    d = [[0] * (len(hyp_chars) + 1) for _ in range(len(ref_chars) + 1)]

    # 初始化
    for i in range(len(ref_chars) + 1):
        d[i][0] = i
    for j in range(len(hyp_chars) + 1):
        d[0][j] = j

    # 填表
    for i in range(1, len(ref_chars) + 1):
        for j in range(1, len(hyp_chars) + 1):
            if ref_chars[i - 1] == hyp_chars[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                deletion = d[i - 1][j] + 1
                insertion = d[i][j - 1] + 1
                d[i][j] = min(substitution, deletion, insertion)

    # 回溯找对齐
    alignment = backtrack(d, ref_chars, hyp_chars)

    # 统计
    substitutions = sum(1 for a in alignment if a['type'] == 'substitution')
    deletions = sum(1 for a in alignment if a['type'] == 'deletion')
    insertions = sum(1 for a in alignment if a['type'] == 'insertion')

    cer = (substitutions + deletions + insertions) / len(ref_chars) * 100

    return {
        'metric': 'CER',
        'result': round(cer, 2),
        'total': len(ref_chars),
        'substitutions': substitutions,
        'deletions': deletions,
        'insertions': insertions,
        'alignment': alignment
    }


def calculate_metric(reference: str, hypothesis: str, language: str) -> dict:
    """
    根据语言计算对应的指标
    """
    # 预处理文本
    ref_processed = preprocess_text(reference, language)
    hyp_processed = preprocess_text(hypothesis, language)

    if language == 'en':
        return calculate_wer(ref_processed, hyp_processed)
    else:  # zh 或 ja
        return calculate_cer(ref_processed, hyp_processed)
