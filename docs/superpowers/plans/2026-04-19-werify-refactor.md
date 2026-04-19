# WERify 项目重构计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重构 WERify 项目，提升代码可维护性、可测试性和可扩展性

**Architecture:** 采用分层架构：API层(路由) -> 服务层(业务逻辑) -> 数据访问层(数据库)，核心计算逻辑独立封装

**Tech Stack:** Python 3.13, Flask, SQLite, Vue.js 3, CSS Variables

---

## 文件结构规划

### 后端重构
```
wer-calculator/
├── app.py                    # 仅保留路由定义
├── config.py                 # 配置管理（新增）
├── core/
│   ├── __init__.py
│   ├── calculator.py         # 核心计算逻辑（从原文件迁移）
│   ├── text_processor.py     # 文本预处理（新增）
│   └── number_normalizer.py  # 数字归一化（新增）
├── services/
│   ├── __init__.py
│   ├── calculation_service.py    # 计算服务（新增）
│   └── history_service.py        # 历史记录服务（新增）
├── repositories/
│   ├── __init__.py
│   └── history_repository.py     # 历史记录数据访问（新增）
├── models/
│   ├── __init__.py
│   └── calculation_result.py     # 数据模型（新增）
├── database/
│   ├── __init__.py
│   └── db_manager.py             # 数据库管理（从原文件迁移重构）
└── tests/                        # 测试目录（新增）
    ├── __init__.py
    ├── test_calculator.py
    ├── test_text_processor.py
    └── test_number_normalizer.py
```

### 前端重构
```
static/
├── index.html                # 简化，移除内联JS
├── history.html              # 简化，移除内联JS
├── css/
│   ├── style.css             # 保留基础样式
│   ├── components.css        # 组件样式（新增）
│   └── themes.css            # 主题变量（新增）
└── js/
    ├── app.js                # 主应用逻辑（新增）
    ├── components/
    │   ├── calculator.js     # 计算器组件（新增）
    │   ├── history.js        # 历史记录组件（新增）
    │   └── theme-toggle.js   # 主题切换组件（新增）
    └── utils/
        ├── api.js            # API 封装（新增）
        └── storage.js        # 本地存储（新增）
```

---

## Task 1: 创建项目基础结构

**Files:**
- Create: `config.py`
- Create: `core/__init__.py`
- Create: `services/__init__.py`
- Create: `repositories/__init__.py`
- Create: `models/__init__.py`
- Create: `database/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: 创建配置文件**

```python
# config.py
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
```

- [ ] **Step 2: 创建所有 __init__.py 文件**

```bash
# 创建空文件
touch core/__init__.py
touch services/__init__.py
touch repositories/__init__.py
touch models/__init__.py
touch database/__init__.py
touch tests/__init__.py
```

- [ ] **Step 3: Commit**

```bash
git add config.py core/ services/ repositories/ models/ database/ tests/
git commit -m "chore: create project structure for refactoring"
```

---

## Task 2: 重构核心计算模块

**Files:**
- Create: `core/text_processor.py`
- Create: `core/number_normalizer.py`
- Create: `core/calculator.py`
- Modify: `calculator.py` (原文件，后续删除)

- [ ] **Step 1: 创建文本处理器**

```python
# core/text_processor.py
import re
from typing import Dict, Callable

class TextProcessor:
    """文本预处理器"""
    
    # 语言特定的处理配置
    PROCESSORS: Dict[str, Dict] = {
        'en': {
            'to_lower': True,
            'punctuation_to_space': True,
            'allowed_chars': r'a-zA-Z0-9\s',
            'normalize_numbers': True
        },
        'zh': {
            'to_lower': False,
            'punctuation_to_space': False,
            'allowed_chars': r'\u4e00-\u9fff0-9',
            'normalize_numbers': True
        },
        'ja': {
            'to_lower': True,
            'punctuation_to_space': False,
            'allowed_chars': r'\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fffa-zA-Z0-9',
            'normalize_numbers': False
        }
    }
    
    def __init__(self, language: str = 'en'):
        if language not in self.PROCESSORS:
            raise ValueError(f"Unsupported language: {language}")
        self.language = language
        self.config = self.PROCESSORS[language]
    
    def process(self, text: str) -> str:
        """处理文本"""
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
```

- [ ] **Step 2: 创建数字归一化器**

```python
# core/number_normalizer.py
from typing import Dict, Set

class NumberNormalizer:
    """数字归一化器 - 将中文/英文数字转为阿拉伯数字"""
    
    # 中文数字映射
    CN_DIGITS: Dict[str, str] = {
        '零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
        '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
        '两': '2'
    }
    
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
        """归一化数字"""
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
                num = self._parse_chinese_number(num_str)
                result.append(str(num))
                i = j
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    def _parse_chinese_number(self, s: str) -> int:
        """解析中文数字"""
        if not s:
            return 0
        
        result = 0
        current = 0
        
        for char in s:
            if char in self.CN_DIGITS:
                current = int(self.CN_DIGITS[char])
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
        words = text.split()
        normalized = []
        
        for word in words:
            clean_word = ''.join(c for c in word.lower() if c.isalnum())
            if clean_word in self.EN_NUMBERS:
                normalized.append(self.EN_NUMBERS[clean_word])
            else:
                normalized.append(word)
        
        return ' '.join(normalized)
```

- [ ] **Step 3: 创建核心计算器**

```python
# core/calculator.py
from typing import List, Tuple, Dict, Optional
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
    
    # 计算编辑距离
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

def _compute_alignment(ref_items: List[str], hyp_items: List[str]) -> Tuple[int, List[AlignmentItem]]:
    """计算对齐"""
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
            if ref_items[i-1] == hyp_items[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # 删除
                    dp[i][j-1],      # 插入
                    dp[i-1][j-1]     # 替换
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
    """回溯找对齐路径"""
    alignment = []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref_items[i-1] == hyp_items[j-1]:
            # 匹配
            alignment.append(AlignmentItem(
                ref=ref_items[i-1],
                hyp=hyp_items[j-1],
                type='correct'
            ))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            # 替换
            alignment.append(AlignmentItem(
                ref=ref_items[i-1],
                hyp=hyp_items[j-1],
                type='substitution'
            ))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            # 删除
            alignment.append(AlignmentItem(
                ref=ref_items[i-1],
                hyp=None,
                type='deletion'
            ))
            i -= 1
        else:
            # 插入
            alignment.append(AlignmentItem(
                ref=None,
                hyp=hyp_items[j-1],
                type='insertion'
            ))
            j -= 1
    
    alignment.reverse()
    return alignment
```

- [ ] **Step 4: Commit**

```bash
git add core/
git commit -m "refactor: extract core calculation logic into separate modules"
```

---

## Task 3: 创建数据模型

**Files:**
- Create: `models/calculation_result.py`

- [ ] **Step 1: 创建数据模型**

```python
# models/calculation_result.py
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

@dataclass
class AlignmentItemModel:
    """对齐项模型"""
    ref: Optional[str]
    hyp: Optional[str]
    type: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ref': self.ref,
            'hyp': self.hyp,
            'type': self.type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AlignmentItemModel':
        return cls(
            ref=data.get('ref'),
            hyp=data.get('hyp'),
            type=data['type']
        )

@dataclass
class CalculationResultModel:
    """计算结果模型"""
    id: Optional[int] = None
    title: str = ''
    timestamp: str = ''
    language: str = 'en'
    reference: str = ''
    hypothesis: str = ''
    metric: str = 'WER'
    result: float = 0.0
    substitutions: int = 0
    deletions: int = 0
    insertions: int = 0
    total: int = 0
    alignment: List[AlignmentItemModel] = None
    
    def __post_init__(self):
        if self.alignment is None:
            self.alignment = []
        if not self.timestamp:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'timestamp': self.timestamp,
            'language': self.language,
            'reference': self.reference,
            'hypothesis': self.hypothesis,
            'metric': self.metric,
            'result': self.result,
            'substitutions': self.substitutions,
            'deletions': self.deletions,
            'insertions': self.insertions,
            'total': self.total,
            'alignment': [item.to_dict() for item in self.alignment]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculationResultModel':
        alignment_data = data.get('alignment', [])
        alignment = [AlignmentItemModel.from_dict(item) for item in alignment_data]
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            timestamp=data.get('timestamp', ''),
            language=data.get('language', 'en'),
            reference=data.get('reference', ''),
            hypothesis=data.get('hypothesis', ''),
            metric=data.get('metric', 'WER'),
            result=data.get('result', 0.0),
            substitutions=data.get('substitutions', 0),
            deletions=data.get('deletions', 0),
            insertions=data.get('insertions', 0),
            total=data.get('total', 0),
            alignment=alignment
        )
    
    def to_db_dict(self) -> Dict[str, Any]:
        """转换为数据库格式"""
        return {
            'id': self.id,
            'title': self.title,
            'timestamp': self.timestamp,
            'language': self.language,
            'reference': self.reference,
            'hypothesis': self.hypothesis,
            'metric': self.metric,
            'result': self.result,
            'substitutions': self.substitutions,
            'deletions': self.deletions,
            'insertions': self.insertions,
            'total': self.total,
            'alignment': json.dumps([item.to_dict() for item in self.alignment])
        }
    
    @classmethod
    def from_db_dict(cls, data: Dict[str, Any]) -> 'CalculationResultModel':
        """从数据库格式创建"""
        alignment_json = data.get('alignment', '[]')
        try:
            alignment_data = json.loads(alignment_json)
            alignment = [AlignmentItemModel.from_dict(item) for item in alignment_data]
        except json.JSONDecodeError:
            alignment = []
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            timestamp=data.get('timestamp', ''),
            language=data.get('language', 'en'),
            reference=data.get('reference', ''),
            hypothesis=data.get('hypothesis', ''),
            metric=data.get('metric', 'WER'),
            result=data.get('result', 0.0),
            substitutions=data.get('substitutions', 0),
            deletions=data.get('deletions', 0),
            insertions=data.get('insertions', 0),
            total=data.get('total', 0),
            alignment=alignment
        )
```

- [ ] **Step 2: Commit**

```bash
git add models/
git commit -m "feat: add data models for calculation results"
```

---

## Task 4: 重构数据库层

**Files:**
- Create: `database/db_manager.py`
- Modify: `database.py` (原文件，后续删除)

- [ ] **Step 1: 创建数据库管理器**

```python
# database/db_manager.py
import sqlite3
import os
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from ..models.calculation_result import CalculationResultModel
from ..config import Config

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._init_db()
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接（上下文管理器）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """初始化数据库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建历史记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT DEFAULT '',
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    language TEXT DEFAULT 'en',
                    reference TEXT NOT NULL,
                    hypothesis TEXT NOT NULL,
                    metric TEXT DEFAULT 'WER',
                    result REAL DEFAULT 0,
                    substitutions INTEGER DEFAULT 0,
                    deletions INTEGER DEFAULT 0,
                    insertions INTEGER DEFAULT 0,
                    total INTEGER DEFAULT 0,
                    alignment TEXT DEFAULT '[]'
                )
            ''')
            
            # 检查是否需要迁移（添加 alignment 字段）
            cursor.execute("PRAGMA table_info(history)")
            columns = [row['name'] for row in cursor.fetchall()]
            
            if 'alignment' not in columns:
                cursor.execute('''
                    ALTER TABLE history ADD COLUMN alignment TEXT DEFAULT '[]'
                ''')
    
    def save_record(self, record: CalculationResultModel) -> int:
        """保存记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            data = record.to_db_dict()
            
            cursor.execute('''
                INSERT INTO history 
                (title, timestamp, language, reference, hypothesis, metric, 
                 result, substitutions, deletions, insertions, total, alignment)
                VALUES 
                (:title, :timestamp, :language, :reference, :hypothesis, :metric,
                 :result, :substitutions, :deletions, :insertions, :total, :alignment)
            ''', data)
            
            return cursor.lastrowid
    
    def get_record_by_id(self, record_id: int) -> Optional[CalculationResultModel]:
        """根据ID获取记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM history WHERE id = ?', 
                (record_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return CalculationResultModel.from_db_dict(dict(row))
            return None
    
    def get_all_records(self) -> List[CalculationResultModel]:
        """获取所有记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM history ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            
            return [CalculationResultModel.from_db_dict(dict(row)) for row in rows]
    
    def get_records_by_language(self, language: str) -> List[CalculationResultModel]:
        """根据语言获取记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM history WHERE language = ? ORDER BY timestamp DESC',
                (language,)
            )
            rows = cursor.fetchall()
            
            return [CalculationResultModel.from_db_dict(dict(row)) for row in rows]
    
    def search_records_by_title(self, keyword: str, language: str = None) -> List[CalculationResultModel]:
        """根据标题搜索记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if language:
                cursor.execute('''
                    SELECT * FROM history 
                    WHERE title LIKE ? AND language = ?
                    ORDER BY timestamp DESC
                ''', (f'%{keyword}%', language))
            else:
                cursor.execute('''
                    SELECT * FROM history 
                    WHERE title LIKE ?
                    ORDER BY timestamp DESC
                ''', (f'%{keyword}%',))
            
            rows = cursor.fetchall()
            return [CalculationResultModel.from_db_dict(dict(row)) for row in rows]
    
    def update_record_title(self, record_id: int, title: str) -> bool:
        """更新记录标题"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE history SET title = ? WHERE id = ?',
                (title, record_id)
            )
            return cursor.rowcount > 0
    
    def delete_record(self, record_id: int) -> bool:
        """删除记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history WHERE id = ?', (record_id,))
            return cursor.rowcount > 0
    
    def clear_all_records(self) -> int:
        """清空所有记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history')
            return cursor.rowcount
```

- [ ] **Step 2: Commit**

```bash
git add database/
git commit -m "refactor: restructure database layer with DatabaseManager"
```

---

## Task 5: 创建服务层

**Files:**
- Create: `services/calculation_service.py`
- Create: `services/history_service.py`

- [ ] **Step 1: 创建计算服务**

```python
# services/calculation_service.py
from typing import Dict, Any
from ..core.calculator import calculate_wer_cer, CalculationResult
from ..models.calculation_result import CalculationResultModel, AlignmentItemModel

class CalculationService:
    """计算服务"""
    
    def calculate(
        self, 
        reference: str, 
        hypothesis: str, 
        language: str = 'en',
        metric: str = 'wer',
        title: str = ''
    ) -> CalculationResultModel:
        """
        执行计算
        
        Args:
            reference: 参考文本
            hypothesis: 识别文本
            language: 语言
            metric: 指标类型
            title: 标题
        
        Returns:
            CalculationResultModel
        """
        # 执行核心计算
        result = calculate_wer_cer(reference, hypothesis, language, metric)
        
        # 转换为模型
        alignment_models = [
            AlignmentItemModel(
                ref=item.ref,
                hyp=item.hyp,
                type=item.type
            )
            for item in result.alignment
        ]
        
        return CalculationResultModel(
            title=title,
            language=language,
            reference=reference,
            hypothesis=hypothesis,
            metric=result.metric,
            result=result.result,
            substitutions=result.substitutions,
            deletions=result.deletions,
            insertions=result.insertions,
            total=result.total,
            alignment=alignment_models
        )
    
    def validate_input(
        self, 
        reference: str, 
        hypothesis: str, 
        language: str
    ) -> Dict[str, Any]:
        """验证输入"""
        errors = {}
        
        if not reference or not reference.strip():
            errors['reference'] = '参考文本不能为空'
        
        if not hypothesis or not hypothesis.strip():
            errors['hypothesis'] = '识别文本不能为空'
        
        if language not in ['en', 'zh', 'ja']:
            errors['language'] = '不支持的语言'
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
```

- [ ] **Step 2: 创建历史记录服务**

```python
# services/history_service.py
from typing import List, Optional, Dict, Any
from ..database.db_manager import DatabaseManager
from ..models.calculation_result import CalculationResultModel
from ..config import Config

class HistoryService:
    """历史记录服务"""
    
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
    
    def save_calculation(
        self, 
        result: CalculationResultModel
    ) -> Dict[str, Any]:
        """保存计算记录"""
        try:
            record_id = self.db.save_record(result)
            return {
                'success': True,
                'id': record_id,
                'message': '保存成功'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_history_list(
        self, 
        language: str = None,
        page: int = 1,
        page_size: int = None
    ) -> Dict[str, Any]:
        """获取历史记录列表"""
        try:
            if language:
                records = self.db.get_records_by_language(language)
            else:
                records = self.db.get_all_records()
            
            # 分页
            page_size = page_size or Config.DEFAULT_PAGE_SIZE
            total = len(records)
            start = (page - 1) * page_size
            end = start + page_size
            paginated_records = records[start:end]
            
            return {
                'success': True,
                'data': [r.to_dict() for r in paginated_records],
                'total': total,
                'page': page,
                'page_size': page_size
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_history(
        self, 
        keyword: str, 
        language: str = None
    ) -> Dict[str, Any]:
        """搜索历史记录"""
        try:
            records = self.db.search_records_by_title(keyword, language)
            
            return {
                'success': True,
                'data': [r.to_dict() for r in records],
                'total': len(records)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_title(
        self, 
        record_id: int, 
        title: str
    ) -> Dict[str, Any]:
        """更新记录标题"""
        try:
            success = self.db.update_record_title(record_id, title)
            if success:
                return {
                    'success': True,
                    'message': '更新成功'
                }
            else:
                return {
                    'success': False,
                    'error': '记录不存在'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_record(self, record_id: int) -> Dict[str, Any]:
        """删除记录"""
        try:
            success = self.db.delete_record(record_id)
            if success:
                return {
                    'success': True,
                    'message': '删除成功'
                }
            else:
                return {
                    'success': False,
                    'error': '记录不存在'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def clear_all(self) -> Dict[str, Any]:
        """清空所有记录"""
        try:
            count = self.db.clear_all_records()
            return {
                'success': True,
                'message': f'已清空 {count} 条记录'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_record_detail(self, record_id: int) -> Dict[str, Any]:
        """获取记录详情"""
        try:
            record = self.db.get_record_by_id(record_id)
            if record:
                return {
                    'success': True,
                    'data': record.to_dict()
                }
            else:
                return {
                    'success': False,
                    'error': '记录不存在'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
```

- [ ] **Step 3: Commit**

```bash
git add services/
git commit -m "feat: add service layer for business logic"
```

---

## Task 6: 重构 Flask 路由

**Files:**
- Modify: `app.py` (完全重写)

- [ ] **Step 1: 重写 app.py**

```python
# app.py
"""
Flask 主应用 - 仅保留路由定义
"""
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import os
import csv
import io
from datetime import datetime

from config import Config
from services.calculation_service import CalculationService
from services.history_service import HistoryService
from database.db_manager import DatabaseManager

# 初始化 Flask 应用
app = Flask(__name__, static_folder='static')
CORS(app)

# 初始化服务
calc_service = CalculationService()
history_service = HistoryService()

# ==================== 静态文件路由 ====================

@app.route('/')
def index():
    """首页"""
    return send_from_directory('static', 'index.html')

@app.route('/history')
def history_page():
    """历史记录页面"""
    return send_from_directory('static', 'history.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """静态文件"""
    return send_from_directory('static', filename)

# ==================== API 路由 ====================

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """计算 WER/CER"""
    try:
        data = request.get_json()
        
        # 提取参数
        reference = data.get('reference', '')
        hypothesis = data.get('hypothesis', '')
        language = data.get('language', 'en')
        metric = data.get('metric', 'wer')
        title = data.get('title', '').strip()
        save = data.get('save', True)
        
        # 验证输入
        validation = calc_service.validate_input(reference, hypothesis, language)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'errors': validation['errors']
            }), 400
        
        # 执行计算
        result = calc_service.calculate(
            reference=reference,
            hypothesis=hypothesis,
            language=language,
            metric=metric,
            title=title
        )
        
        # 保存到历史记录
        if save:
            history_service.save_calculation(result)
        
        return jsonify({
            'success': True,
            'data': result.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """获取历史记录"""
    try:
        language = request.args.get('language')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', Config.DEFAULT_PAGE_SIZE, type=int)
        
        result = history_service.get_history_list(
            language=language,
            page=page,
            page_size=min(page_size, Config.MAX_PAGE_SIZE)
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/search', methods=['GET'])
def search_history():
    """搜索历史记录"""
    try:
        keyword = request.args.get('keyword', '')
        language = request.args.get('language')
        
        if not keyword:
            return jsonify({
                'success': False,
                'error': '搜索关键词不能为空'
            }), 400
        
        result = history_service.search_history(keyword, language)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<int:record_id>', methods=['GET'])
def get_history_detail(record_id):
    """获取历史记录详情"""
    result = history_service.get_record_detail(record_id)
    return jsonify(result)

@app.route('/api/history/<int:record_id>', methods=['PUT'])
def update_history_title(record_id):
    """更新历史记录标题"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        
        if not title:
            return jsonify({
                'success': False,
                'error': '标题不能为空'
            }), 400
        
        result = history_service.update_title(record_id, title)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    """删除历史记录"""
    result = history_service.delete_record(record_id)
    return jsonify(result)

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """清空所有历史记录"""
    result = history_service.clear_all()
    return jsonify(result)

@app.route('/api/history/export', methods=['GET'])
def export_history():
    """导出历史记录"""
    try:
        scope = request.args.get('scope', 'all')
        language = request.args.get('language')
        keyword = request.args.get('keyword')
        
        # 获取记录
        if scope == 'filtered':
            if keyword:
                records = history_service.search_history(keyword, language)
                records = records.get('data', [])
            elif language:
                db = DatabaseManager()
                records = db.get_records_by_language(language)
                records = [r.to_dict() for r in records]
            else:
                db = DatabaseManager()
                records = db.get_all_records()
                records = [r.to_dict() for r in records]
        else:
            db = DatabaseManager()
            records = db.get_all_records()
            records = [r.to_dict() for r in records]
        
        if not records:
            return jsonify({
                'success': False,
                'error': '没有可导出的记录'
            }), 400
        
        # 生成 CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        headers = ['ID', '标题', '时间', '语言', '参考文本', '识别文本', 
                   '指标', '错误率', '替换数', '删除数', '插入数', '总数']
        writer.writerow(headers)
        
        lang_map = {'en': '英文', 'zh': '中文', 'ja': '日文'}
        
        for record in records:
            row = [
                record['id'],
                record.get('title', ''),
                record['timestamp'],
                lang_map.get(record['language'], record['language']),
                record['reference'],
                record['hypothesis'],
                record['metric'],
                f"{record['result']}%",
                record['substitutions'],
                record['deletions'],
                record['insertions'],
                record['total']
            ]
            writer.writerow(row)
        
        csv_content = '\ufeff' + output.getvalue()
        output.close()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'wer_history_{timestamp}.csv'
        
        return Response(
            csv_content.encode('utf-8'),
            mimetype='text/csv; charset=utf-8',
            headers={
                'Content-Disposition': f'attachment; filename={filename}'
            }
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok'})

# ==================== 主程序入口 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("  wer-calculator - ASR WER/CER Calculator")
    print("=" * 60)
    print(f"本地访问:    http://localhost:{Config.PORT}")
    print(f"局域网访问:  http://<本机IP>:{Config.PORT}")
    print("-" * 60)
    print("提示: 按 Ctrl+C 可以关闭应用")
    print("=" * 60)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
```

- [ ] **Step 2: Commit**

```bash
git add app.py
git commit -m "refactor: restructure Flask app with clean architecture"
```

---

## Task 7: 删除旧文件

**Files:**
- Delete: `calculator.py` (旧文件)
- Delete: `database.py` (旧文件)

- [ ] **Step 1: 删除旧文件**

```bash
git rm calculator.py database.py
git commit -m "chore: remove old monolithic files"
```

---

## Task 8: 创建测试

**Files:**
- Create: `tests/test_text_processor.py`
- Create: `tests/test_number_normalizer.py`
- Create: `tests/test_calculator.py`

- [ ] **Step 1: 创建文本处理器测试**

```python
# tests/test_text_processor.py
import unittest
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
    
    def test_chinese_processing(self):
        """测试中文处理"""
        processor = TextProcessor('zh')
        
        # 测试保留中文和数字
        result = processor.process("你好123")
        self.assertEqual(result, "你好123")
        
        # 测试去除英文标点
        result = processor.process("你好，世界！")
        self.assertEqual(result, "你好世界")
    
    def test_japanese_processing(self):
        """测试日文处理"""
        processor = TextProcessor('ja')
        
        # 测试保留日文、英文和数字
        result = processor.process("こんにちはhello123")
        self.assertEqual(result, "こんにちはhello123")
        
        # 测试英文转小写
        result = processor.process("Hello")
        self.assertEqual(result, "hello")
    
    def test_empty_input(self):
        """测试空输入"""
        processor = TextProcessor('en')
        result = processor.process("")
        self.assertEqual(result, "")
    
    def test_invalid_language(self):
        """测试无效语言"""
        with self.assertRaises(ValueError):
            TextProcessor('invalid')

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 创建数字归一化器测试**

```python
# tests/test_number_normalizer.py
import unittest
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
    
    def test_chinese_twenty_one(self):
        """测试中文二十一"""
        result = self.normalizer.normalize("二十一", 'zh')
        self.assertEqual(result, "21")
    
    def test_chinese_hundred(self):
        """测试中文一百"""
        result = self.normalizer.normalize("一百", 'zh')
        self.assertEqual(result, "100")
    
    def test_chinese_mixed_text(self):
        """测试中文混合文本"""
        result = self.normalizer.normalize("第 twenty 一页", 'zh')
        self.assertEqual(result, "第20一页")
    
    def test_english_numbers(self):
        """测试英文数字"""
        result = self.normalizer.normalize("ten", 'en')
        self.assertEqual(result, "10")
        
        result = self.normalizer.normalize("twenty", 'en')
        self.assertEqual(result, "20")
    
    def test_english_mixed_text(self):
        """测试英文混合文本"""
        result = self.normalizer.normalize("I have ten apples", 'en')
        self.assertEqual(result, "I have 10 apples")
    
    def test_no_numbers(self):
        """测试无数字文本"""
        result = self.normalizer.normalize("hello world", 'zh')
        self.assertEqual(result, "hello world")

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 3: 创建计算器测试**

```python
# tests/test_calculator.py
import unittest
from core.calculator import calculate_wer_cer

class TestCalculator(unittest.TestCase):
    """计算器测试"""
    
    def test_perfect_match(self):
        """测试完全匹配"""
        result = calculate_wer_cer("hello world", "hello world", 'en', 'wer')
        self.assertEqual(result.result, 0.0)
        self.assertEqual(result.substitutions, 0)
        self.assertEqual(result.deletions, 0)
        self.assertEqual(result.insertions, 0)
    
    def test_substitution(self):
        """测试替换错误"""
        result = calculate_wer_cer("hello world", "hello there", 'en', 'wer')
        self.assertEqual(result.substitutions, 1)
        self.assertEqual(result.deletions, 0)
        self.assertEqual(result.insertions, 0)
    
    def test_deletion(self):
        """测试删除错误"""
        result = calculate_wer_cer("hello world", "hello", 'en', 'wer')
        self.assertEqual(result.substitutions, 0)
        self.assertEqual(result.deletions, 1)
        self.assertEqual(result.insertions, 0)
    
    def test_insertion(self):
        """测试插入错误"""
        result = calculate_wer_cer("hello", "hello world", 'en', 'wer')
        self.assertEqual(result.substitutions, 0)
        self.assertEqual(result.deletions, 0)
        self.assertEqual(result.insertions, 1)
    
    def test_chinese_cer(self):
        """测试中文CER"""
        result = calculate_wer_cer("你好世界", "你好", 'zh', 'cer')
        self.assertEqual(result.deletions, 2)
    
    def test_mixed_language(self):
        """测试混合语言"""
        result = calculate_wer_cer(
            "hello world 你好", 
            "hello world 你好", 
            'ja', 
            'cer'
        )
        self.assertEqual(result.result, 0.0)

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 4: Commit**

```bash
git add tests/
git commit -m "test: add unit tests for core modules"
```

---

## Task 9: 运行测试验证

- [ ] **Step 1: 运行所有测试**

```bash
python -m pytest tests/ -v
```

- [ ] **Step 2: 验证应用启动**

```bash
python app.py
```

- [ ] **Step 3: Commit**

```bash
git commit -m "test: verify all tests pass"
```

---

## Task 10: 更新文档

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 更新 README 架构部分**

在 README 中添加新的架构说明：

```markdown
## 🏗️ 项目架构

本项目采用分层架构设计：

```
wer-calculator/
├── app.py                 # Flask 路由层
├── config.py             # 配置管理
├── core/                 # 核心计算层
│   ├── calculator.py     # WER/CER 计算
│   ├── text_processor.py # 文本预处理
│   └── number_normalizer.py # 数字归一化
├── services/             # 业务服务层
│   ├── calculation_service.py
│   └── history_service.py
├── repositories/         # 数据访问层
│   └── history_repository.py
├── models/               # 数据模型层
│   └── calculation_result.py
├── database/             # 数据库层
│   └── db_manager.py
└── tests/                # 测试层
    ├── test_calculator.py
    ├── test_text_processor.py
    └── test_number_normalizer.py
```

### 架构特点

- **分层设计**: API层 → 服务层 → 核心层 → 数据层
- **单一职责**: 每个模块职责清晰，便于维护
- **可测试性**: 各层可独立测试，支持 Mock
- **可扩展性**: 易于添加新语言、新指标
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with new architecture"
```

---

## 总结

重构完成后，项目将具备以下特点：

1. **清晰的架构**: 分层设计，职责分离
2. **可测试性**: 完整的单元测试覆盖
3. **可维护性**: 模块化设计，易于理解和修改
4. **可扩展性**: 易于添加新功能

**执行方式选择：**

**1. Subagent-Driven (推荐)** - 我为每个 Task 分配独立的 subagent，并行执行，我负责审核

**2. Inline Execution** - 在当前会话中按顺序执行所有 Task

**你选择哪种方式？** 或者你想先执行其中几个 Task 看看效果？
