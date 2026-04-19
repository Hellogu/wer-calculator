"""
数字归一化器测试
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.number_normalizer import NumberNormalizer


class TestNumberNormalizer(unittest.TestCase):
    """数字归一化器测试"""
    
    def setUp(self):
        self.normalizer = NumberNormalizer()
    
    def test_chinese_single_digits(self):
        """测试中文个位数"""
        result = self.normalizer.normalize("一二三", 'zh')
        self.assertEqual(result, "123")
    
    def test_chinese_ten(self):
        """测试中文十"""
        result = self.normalizer.normalize("十", 'zh')
        self.assertEqual(result, "10")
    
    def test_chinese_eleven(self):
        """测试中文十一"""
        result = self.normalizer.normalize("十一", 'zh')
        self.assertEqual(result, "11")
    
    def test_chinese_twenty(self):
        """测试中文二十"""
        result = self.normalizer.normalize("二十", 'zh')
        self.assertEqual(result, "20")
    
    def test_chinese_twenty_one(self):
        """测试中文二十一"""
        result = self.normalizer.normalize("二十一", 'zh')
        self.assertEqual(result, "21")
    
    def test_chinese_hundred(self):
        """测试中文一百"""
        result = self.normalizer.normalize("一百", 'zh')
        self.assertEqual(result, "100")
    
    def test_chinese_hundred_five(self):
        """测试中文一百零五"""
        result = self.normalizer.normalize("一百零五", 'zh')
        self.assertEqual(result, "105")
    
    def test_chinese_thousand(self):
        """测试中文一千"""
        result = self.normalizer.normalize("一千", 'zh')
        self.assertEqual(result, "1000")
    
    def test_chinese_ten_thousand(self):
        """测试中文一万"""
        result = self.normalizer.normalize("一万", 'zh')
        self.assertEqual(result, "10000")
    
    def test_chinese_mixed_text(self):
        """测试中文混合文本"""
        result = self.normalizer.normalize("第 twenty 一页", 'zh')
        self.assertEqual(result, "第20一页")
    
    def test_chinese_no_numbers(self):
        """测试中文无数字"""
        result = self.normalizer.normalize("你好世界", 'zh')
        self.assertEqual(result, "你好世界")
    
    def test_english_zero_to_nine(self):
        """测试英文0-9"""
        for word, num in [('zero', '0'), ('one', '1'), ('two', '2'), 
                          ('three', '3'), ('four', '4'), ('five', '5'),
                          ('six', '6'), ('seven', '7'), ('eight', '8'), ('nine', '9')]:
            result = self.normalizer.normalize(word, 'en')
            self.assertEqual(result, num)
    
    def test_english_ten_to_twenty(self):
        """测试英文10-20"""
        for word, num in [('ten', '10'), ('eleven', '11'), ('twelve', '12'),
                          ('thirteen', '13'), ('fourteen', '14'), ('fifteen', '15'),
                          ('sixteen', '16'), ('seventeen', '17'), ('eighteen', '18'),
                          ('nineteen', '19'), ('twenty', '20')]:
            result = self.normalizer.normalize(word, 'en')
            self.assertEqual(result, num)
    
    def test_english_mixed_text(self):
        """测试英文混合文本"""
        result = self.normalizer.normalize("I have ten apples", 'en')
        self.assertEqual(result, "I have 10 apples")
    
    def test_english_no_numbers(self):
        """测试英文无数字"""
        result = self.normalizer.normalize("hello world", 'en')
        self.assertEqual(result, "hello world")
    
    def test_special_chinese_numbers(self):
        """测试特殊中文数字"""
        # 两
        result = self.normalizer.normalize("两", 'zh')
        self.assertEqual(result, "2")
        
        # 廿
        result = self.normalizer.normalize("廿", 'zh')
        self.assertEqual(result, "20")
        
        # 卅
        result = self.normalizer.normalize("卅", 'zh')
        self.assertEqual(result, "30")


if __name__ == '__main__':
    unittest.main()
