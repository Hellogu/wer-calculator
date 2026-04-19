"""
数字归一化模块
将中文/英文数字转换为阿拉伯数字
"""
from typing import Dict, Set


class NumberNormalizer:
    """数字归一化器"""
    
    # 中文数字到数值的映射
    CN_DIGITS: Dict[str, int] = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '两': 2, '廿': 20, '卅': 30, '卌': 40
    }
    
    # 中文单位映射
    CN_UNITS: Dict[str, int] = {
        '十': 10, '百': 100, '千': 1000, '万': 10000
    }
    
    # 英文数字映射
    EN_NUMBERS: Dict[str, str] = {
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
        'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
        'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
        'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
        'eighteen': '18', 'nineteen': '19', 'twenty': '20'
    }
    
    def __init__(self):
        self.all_cn_chars: Set[str] = set(self.CN_DIGITS.keys()) | set(self.CN_UNITS.keys())
    
    def normalize(self, text: str, language: str = 'zh') -> str:
        """
        归一化数字
        
        Args:
            text: 输入文本
            language: 语言类型 ('zh', 'en')
        
        Returns:
            归一化后的文本
        """
        if language == 'zh':
            return self._normalize_chinese(text)
        elif language == 'en':
            return self._normalize_english(text)
        return text
    
    def _normalize_chinese(self, text: str) -> str:
        """中文数字归一化"""
        import re
        
        # 先处理英文数字（在中文模式下也处理英文数字）
        # 使用特殊模式，保留空格以便后续处理
        text = self._normalize_english_in_chinese(text)
        
        # 快速检查：如果没有中文数字字符，直接返回
        if not any(c in self.all_cn_chars for c in text):
            return text
        
        # 判断是否为纯数字文本（只包含数字字符和空格）
        # 纯数字文本中的单字也应该被转换
        is_pure_number_text = all(c in self.all_cn_chars or c.isspace() for c in text)
        
        result = []
        i = 0
        n = len(text)
        
        while i < n:
            if text[i] in self.all_cn_chars:
                # 找到连续的数字字符
                j = i
                while j < n and text[j] in self.all_cn_chars:
                    j += 1
                
                num_str = text[i:j]
                # 转换条件：
                # 1. 连续数字字符长度>1，或
                # 2. 是纯数字文本，或
                # 3. 该字符是单位数字（十百千万）或特殊数字（廿卅）
                should_convert = (len(num_str) > 1 or 
                                 is_pure_number_text or 
                                 num_str in self.CN_UNITS or
                                 num_str in ('廿', '卅', '卌'))
                
                if should_convert:
                    try:
                        num = self._parse_chinese_number(num_str)
                        result.append(str(num))
                    except Exception:
                        result.append(num_str)
                else:
                    # 不转换（混合文本中的单个个位数）
                    result.append(num_str)
                i = j
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    def _normalize_english_in_chinese(self, text: str) -> str:
        """在中文文本中归一化英文数字，移除英文数字周围的空格"""
        import re
        
        # 快速检查：如果没有英文数字，直接返回原文本
        text_lower = text.lower()
        has_english_number = any(num in text_lower for num in self.EN_NUMBERS.keys())
        if not has_english_number:
            return text
        
        # 使用正则表达式替换英文数字，保留周围文本结构
        result = text
        
        # 处理独立的英文数字词（前后有空格或边界）
        for en_num, digits in sorted(self.EN_NUMBERS.items(), key=lambda x: -len(x[0])):
            # 匹配作为独立词的英文数字
            pattern = r'(?<![a-zA-Z])' + re.escape(en_num) + r'(?![a-zA-Z])'
            result = re.sub(pattern, digits, result, flags=re.IGNORECASE)
        
        # 清理数字周围的多余空格
        # 将 "中文 数字 中文" 中的数字周围空格移除
        result = re.sub(r'(\d+)\s+(?=[\u4e00-\u9fff])', r'\1', result)  # 数字后接中文，移除空格
        result = re.sub(r'(?<=[\u4e00-\u9fff])\s+(\d+)', r'\1', result)  # 中文后接数字，移除空格
        
        return result
    
    def _parse_chinese_number(self, s: str) -> int:
        """解析中文数字字符串"""
        if not s:
            return 0
        
        # 处理纯个位数连续的情况（如"一二三" -> 123）
        if all(c in self.CN_DIGITS and self.CN_DIGITS[c] < 10 for c in s):
            # 将所有个位数连接成数字
            digits = [str(self.CN_DIGITS[c]) for c in s]
            return int(''.join(digits))
        
        result = 0
        current = 0
        
        for char in s:
            if char in self.CN_DIGITS:
                current = self.CN_DIGITS[char]
            elif char in self.CN_UNITS:
                unit = self.CN_UNITS[char]
                if current == 0:
                    current = 1
                if unit >= 10000:
                    result = (result + current) * unit
                else:
                    result += current * unit
                current = 0
        
        result += current
        return result
    
    def _normalize_english(self, text: str) -> str:
        """英文数字归一化"""
        import re
        
        words = text.split()
        normalized = []
        
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word in self.EN_NUMBERS:
                normalized.append(self.EN_NUMBERS[clean_word])
            else:
                normalized.append(word)
        
        return ' '.join(normalized)
