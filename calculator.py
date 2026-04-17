"""
WER/CER 计算核心算法
"""
import re

# 中文数字映射
CHINESE_NUMBERS = {
    '零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
    '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
    '十': '10', '百': '100', '千': '1000', '万': '10000',
    '两': '2', '廿': '20', '卅': '30', '卌': '40'
}

# 英文数字映射
ENGLISH_NUMBERS = {
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
    'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
    'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
    'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
    'eighteen': '18', 'nineteen': '19', 'twenty': '20'
}


def chinese_to_number(text: str) -> str:
    """
    将中文数字转换为阿拉伯数字
    支持: 零-九、十、百、千、万、两、廿、卅、卌
    例如: 二十一 -> 21, 一百零五 -> 105, 三千二百一十 -> 3210
    """
    # 定义中文数字到数值的映射
    cn_to_value = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '两': 2, '廿': 20, '卅': 30, '卌': 40
    }
    # 单位到数值的映射
    unit_to_value = {
        '十': 10, '百': 100, '千': 1000, '万': 10000
    }

    def parse_number(s: str) -> int:
        """解析一个中文数字字符串为整数"""
        if not s:
            return 0

        result = 0
        current = 0
        i = 0
        while i < len(s):
            char = s[i]
            if char in cn_to_value:
                current = cn_to_value[char]
                i += 1
            elif char in unit_to_value:
                unit_val = unit_to_value[char]
                if current == 0:
                    current = 1
                if unit_val >= 10000:
                    result = (result + current) * unit_val
                else:
                    result += current * unit_val
                current = 0
                i += 1
            else:
                i += 1
        result += current
        return result

    # 匹配中文数字模式
    # 包括：十、二十一、一百、一千零五、三千二百一十、两百万等
    pattern = r'[零一二三四五六七八九两廿卅卌十百千万]+'

    def replace_match(m):
        match = m.group(0)
        # 尝试解析为数字
        try:
            num = parse_number(match)
            return str(num)
        except:
            return match

    return re.sub(pattern, replace_match, text)


def english_to_number(text: str) -> str:
    """
    将英文数字单词转换为阿拉伯数字
    支持: zero-twenty
    """
    # 扩展英文数字映射，支持更多数字
    english_nums = {
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
        'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
        'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
        'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
        'eighteen': '18', 'nineteen': '19', 'twenty': '20'
    }

    words = text.split()
    normalized_words = []
    for word in words:
        # 去除标点
        clean_word = re.sub(r'[^\w]', '', word.lower())
        if clean_word in english_nums:
            normalized_words.append(english_nums[clean_word])
        else:
            normalized_words.append(word)
    return ' '.join(normalized_words)


def normalize_numbers(text: str, language: str) -> str:
    """
    将各种形式的数字统一转换为阿拉伯数字
    - 阿拉伯数字: 10, 100 (保持不变)
    - 中文数字: 十, 一百, 一千零五, 二十一
    - 英文数字: ten, one hundred

    无论原始语言是什么，都会尝试转换中文和英文数字
    这样 "10"、"十"、"ten" 都会被统一为 "10"
    """
    result = text

    # 先处理中文数字（适用于所有语言，因为文本中可能包含中文数字）
    result = chinese_to_number(result)

    # 再处理英文数字（适用于所有语言）
    result = english_to_number(result)

    return result


def preprocess_text(text: str, language: str) -> str:
    """
    预处理文本
    - 去除多余空格
    - 英文转小写
    - 数字归一化（中文/英文数字转阿拉伯数字）
    - 去除特殊符号（保留字母、数字、中日文）
    """
    # 首先去除多余空格，合并成一个空格
    text = re.sub(r'\s+', ' ', text).strip()

    # 英文转小写
    if language == 'en':
        text = text.lower()
        # 数字归一化（英文数字转阿拉伯数字）
        text = normalize_numbers(text, language)
        # 英文：先将标点符号替换为空格，避免单词粘连（如 "hello,world" -> "hello world"）
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        # 清理多余空格
        text = re.sub(r'\s+', ' ', text).strip()
    elif language == 'zh':
        # 数字归一化（中文数字转阿拉伯数字）
        text = normalize_numbers(text, language)
        # 中文：只保留中文字符和数字
        text = re.sub(r'[^\u4e00-\u9fff0-9]', '', text)
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
