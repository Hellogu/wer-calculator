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
        # 快速检查：如果没有数字字符，直接返回
        if not any(c in self.all_cn_chars for c in text):
            return text
        
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
                try:
                    num = self._parse_chinese_number(num_str)
                    result.append(str(num))
                except Exception:
                    result.append(num_str)
                i = j
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    def _parse_chinese_number(self, s: str) -> int:
        """解析中文数字字符串"""
        if not s:
            return 0
        
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
