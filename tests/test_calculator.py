"""
计算器测试
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.calculator import calculate_wer_cer


class TestCalculator(unittest.TestCase):
    """计算器测试"""
    
    def test_perfect_match_wer(self):
        """测试WER完全匹配"""
        result = calculate_wer_cer("hello world", "hello world", 'en', 'wer')
        self.assertEqual(result.result, 0.0)
        self.assertEqual(result.substitutions, 0)
        self.assertEqual(result.deletions, 0)
        self.assertEqual(result.insertions, 0)
    
    def test_perfect_match_cer(self):
        """测试CER完全匹配"""
        result = calculate_wer_cer("hello", "hello", 'en', 'cer')
        self.assertEqual(result.result, 0.0)
    
    def test_substitution_wer(self):
        """测试WER替换错误"""
        result = calculate_wer_cer("hello world", "hello there", 'en', 'wer')
        self.assertEqual(result.substitutions, 1)
        self.assertEqual(result.deletions, 0)
        self.assertEqual(result.insertions, 0)
        self.assertEqual(result.result, 50.0)  # 1/2 * 100
    
    def test_deletion_wer(self):
        """测试WER删除错误"""
        result = calculate_wer_cer("hello world", "hello", 'en', 'wer')
        self.assertEqual(result.substitutions, 0)
        self.assertEqual(result.deletions, 1)
        self.assertEqual(result.insertions, 0)
    
    def test_insertion_wer(self):
        """测试WER插入错误"""
        result = calculate_wer_cer("hello", "hello world", 'en', 'wer')
        self.assertEqual(result.substitutions, 0)
        self.assertEqual(result.deletions, 0)
        self.assertEqual(result.insertions, 1)
    
    def test_chinese_cer(self):
        """测试中文CER"""
        result = calculate_wer_cer("你好世界", "你好", 'zh', 'cer')
        self.assertEqual(result.deletions, 2)
        self.assertEqual(result.total, 4)
    
    def test_chinese_wer(self):
        """测试中文WER"""
        result = calculate_wer_cer("今天 天气 很好", "今天 天气", 'zh', 'wer')
        self.assertEqual(result.deletions, 1)
        self.assertEqual(result.total, 3)
    
    def test_japanese_cer(self):
        """测试日文CER"""
        result = calculate_wer_cer("こんにちは", "こんにち", 'ja', 'cer')
        self.assertEqual(result.deletions, 1)
    
    def test_mixed_language(self):
        """测试混合语言"""
        result = calculate_wer_cer(
            "hello world 你好",
            "hello world 你好",
            'ja',
            'cer'
        )
        self.assertEqual(result.result, 0.0)
    
    def test_empty_reference(self):
        """测试空参考文本"""
        result = calculate_wer_cer("", "hello", 'en', 'wer')
        self.assertEqual(result.total, 0)
        self.assertEqual(result.result, 0.0)
    
    def test_alignment_length(self):
        """测试对齐结果长度"""
        result = calculate_wer_cer("hello world", "hello there", 'en', 'wer')
        # 对齐结果应该包含所有操作
        total_ops = result.substitutions + result.deletions + result.insertions
        # 加上正确匹配的数量
        correct = sum(1 for item in result.alignment if item.type == 'correct')
        self.assertEqual(len(result.alignment), total_ops + correct)
    
    def test_processed_text(self):
        """测试处理后的文本"""
        result = calculate_wer_cer("Hello, World!", "hello world", 'en', 'wer')
        # 检查预处理后的文本
        self.assertEqual(result.reference_processed, "hello world")
        self.assertEqual(result.hypothesis_processed, "hello world")


if __name__ == '__main__':
    unittest.main()
