"""
文本处理器测试
"""
import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.text_processor import TextProcessor


class TestTextProcessor(unittest.TestCase):
    """文本处理器测试"""
    
    def test_english_processing(self):
        """测试英文处理"""
        processor = TextProcessor('en')
        
        # 测试标点符号转空格
        result = processor.process("hello,world")
        self.assertEqual(result, "hello world")
        
        # 测试转小写
        result = processor.process("Hello World")
        self.assertEqual(result, "hello world")
        
        # 测试多余空格
        result = processor.process("hello    world")
        self.assertEqual(result, "hello world")
        
        # 测试混合标点
        result = processor.process("Hello, world! How are you?")
        self.assertEqual(result, "hello world how are you")
    
    def test_chinese_processing(self):
        """测试中文处理"""
        processor = TextProcessor('zh')
        
        # 测试保留中文和数字
        result = processor.process("你好123")
        self.assertEqual(result, "你好123")
        
        # 测试去除英文标点
        result = processor.process("你好，世界！")
        self.assertEqual(result, "你好世界")
        
        # 测试去除英文字母
        result = processor.process("你好abc")
        self.assertEqual(result, "你好")
    
    def test_japanese_processing(self):
        """测试日文处理"""
        processor = TextProcessor('ja')
        
        # 测试保留日文、英文和数字
        result = processor.process("こんにちはhello123")
        self.assertEqual(result, "こんにちはhello123")
        
        # 测试英文转小写
        result = processor.process("Hello")
        self.assertEqual(result, "hello")
        
        # 测试去除标点
        result = processor.process("こんにちは、世界！")
        self.assertEqual(result, "こんにちは世界")
    
    def test_empty_input(self):
        """测试空输入"""
        processor = TextProcessor('en')
        result = processor.process("")
        self.assertEqual(result, "")
    
    def test_whitespace_only(self):
        """测试仅空格输入"""
        processor = TextProcessor('en')
        result = processor.process("   ")
        self.assertEqual(result, "")
    
    def test_invalid_language(self):
        """测试无效语言"""
        with self.assertRaises(ValueError) as context:
            TextProcessor('invalid')
        self.assertIn('不支持的语言', str(context.exception))


if __name__ == '__main__':
    unittest.main()
