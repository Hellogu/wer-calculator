"""
文本预处理模块
处理不同语言的文本预处理
"""
import re
from typing import Dict


class TextProcessor:
    """文本预处理器"""
    
    # 语言特定的处理配置
    PROCESSORS: Dict[str, Dict] = {
        'en': {
            'to_lower': True,
            'punctuation_to_space': True,
            'allowed_chars': r'a-zA-Z0-9\s',
        },
        'zh': {
            'to_lower': False,
            'punctuation_to_space': False,
            'allowed_chars': r'\u4e00-\u9fff0-9',
        },
        'ja': {
            'to_lower': True,
            'punctuation_to_space': False,
            'allowed_chars': r'\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fffa-zA-Z0-9',
        }
    }
    
    def __init__(self, language: str = 'en'):
        """
        初始化文本处理器
        
        Args:
            language: 语言代码 ('en', 'zh', 'ja')
        """
        if language not in self.PROCESSORS:
            raise ValueError(f"不支持的语言: {language}")
        self.language = language
        self.config = self.PROCESSORS[language]
    
    def process(self, text: str) -> str:
        """
        处理文本
        
        Args:
            text: 输入文本
        
        Returns:
            处理后的文本
        """
        if not text:
            return ''
        
        # 标准化空格
        text = self._normalize_whitespace(text)
        
        # 转小写
        if self.config['to_lower']:
            text = text.lower()
        
        # 标点符号处理
        if self.config['punctuation_to_space']:
            text = self._punctuation_to_space(text)
        
        # 过滤字符
        text = self._filter_chars(text)
        
        # 再次标准化空格
        text = self._normalize_whitespace(text)
        
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """标准化空格"""
        return re.sub(r'\s+', ' ', text).strip()
    
    def _punctuation_to_space(self, text: str) -> str:
        """将标点符号替换为空格"""
        return re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    def _filter_chars(self, text: str) -> str:
        """过滤字符"""
        pattern = f'[^{self.config["allowed_chars"]}]'
        return re.sub(pattern, '', text)
