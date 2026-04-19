import os

class Config:
    """应用配置"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'wer_calculator.db')
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
    
    # 语言配置
    SUPPORTED_LANGUAGES = ['en', 'zh', 'ja']
    DEFAULT_LANGUAGE = 'en'
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
