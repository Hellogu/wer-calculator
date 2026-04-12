# wer-calculator - ASR WER/CER Calculator

一个用于评估语音识别（ASR）系统准确率的本地Web工具，支持中文、英文、日文三种语言的 WER/CER 计算。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 特性

- 🌍 **多语言支持**：中文、英文、日文 WER/CER 计算
- 🎨 **可视化对比**：替换（蓝）、删除（红）、插入（绿）高亮显示
- 📊 **详细统计**：S（替换）、D（删除）、I（插入）数量统计
- 📝 **历史记录**：自动保存计算记录，支持语种过滤
- 🏷️ **标题功能**：为每次计算添加可识别标题
- 🌐 **局域网共享**：支持多设备同时访问
- 📱 **响应式设计**：适配不同屏幕尺寸

## 🚀 快速开始

### 方式一：使用可执行文件（推荐）

1. 从 [Releases](https://github.com/yourusername/wer-calculator/releases) 下载对应系统的可执行文件
2. 双击运行 `wer-calculator.exe`（Windows）或 `wer-calculator`（macOS/Linux）
3. 浏览器自动打开 `http://localhost:5000`

### 方式二：源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/wer-calculator.git
cd wer-calculator

# 2. 创建虚拟环境（推荐）
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python app.py

# 5. 浏览器访问
# 本地：http://localhost:5000
# 局域网：http://你的IP:5000
```

## 📖 使用说明

### 基本使用

1. **输入文本**
   - 在左侧「参考文本」输入标准答案
   - 在右侧「识别文本」输入 ASR 识别结果

2. **设置参数**
   - （可选）输入标题，方便历史记录识别
   - 选择语言类型（英文/中文/日文）

3. **计算结果**
   - 点击「计算」按钮
   - 查看 WER/CER 百分比
   - 查看 S/D/I 统计

4. **查看对比**
   - 下方显示逐字/逐词对比
   - 蓝色 = 替换，红色 = 删除，绿色 = 插入

### 历史记录

- 点击顶部「历史记录」查看所有计算记录
- 支持按语种过滤（全部/英文/中文/日文）
- 点击「加载」可重新加载到计算页面
- 支持删除单条或清空全部

## 🧮 算法说明

### WER（Word Error Rate）- 英文
```
WER = (S + D + I) / N × 100%
```
- N = 参考文本词数
- S = 替换数，D = 删除数，I = 插入数
- 按空格分词

### CER（Character Error Rate）- 中文/日文
```
CER = (S + D + I) / N × 100%
```
- N = 参考文本字符数
- 按字符计算
- 使用动态规划进行最优对齐

### 文本预处理
- 去除所有空格
- 英文转小写
- 去除特殊符号

## 🧪 测试

```bash
python test_calculator.py
```

包含 36 个测试用例，覆盖：
- 基准测试（完美匹配、全错）
- 单错误类型（纯替换、纯删除、纯插入）
- 混合错误（S+D+I 组合）
- 边界条件（空字符串、特殊字符）
- 语言特性（大小写、空格、编码）
- 长文本（100-500字符）
- 真实场景（会议、客服、播客）

## 📦 打包发布

### 使用 PyInstaller

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包（使用配置文件）
pyinstaller wer-calculator.spec

# 输出文件
# Windows: dist/wer-calculator.exe
# macOS/Linux: dist/wer-calculator
```

## 🛠 技术栈

- **后端**：Python + Flask
- **前端**：Vue.js 3 (CDN)
- **数据库**：SQLite
- **样式**：原生 CSS

## 📁 项目结构

```
wer-calculator/
├── app.py                 # Flask 主应用
├── calculator.py          # WER/CER 计算核心
├── database.py            # SQLite 数据库操作
├── test_calculator.py     # 测试用例（36个）
├── requirements.txt       # Python 依赖
├── wer-calculator.spec   # PyInstaller 配置
├── static/
│   ├── index.html        # 主页面
│   ├── history.html      # 历史记录页面
│   └── css/
│       └── style.css     # 样式文件
└── wer_calculator.db     # SQLite 数据库（自动创建）
```

## 📝 更新日志

### v1.1 (2026-04-12)
- 🎨 **全新UI设计**：深色科技主题，现代化视觉风格
- ✨ **视觉增强**：动态渐变背景、网格纹理、发光阴影效果
- ⌨️ **键盘快捷键**：`Ctrl + Enter` 快速计算，`ESC` 关闭弹窗
- 📊 **对比可视化增强**：图例显示各类错误数量统计
- 🎯 **交互优化**：按钮悬停动画、结果区域淡入效果
- ♿ **无障碍支持**：ARIA标签、焦点管理、高对比度模式
- 🔤 **字体优化**：JetBrains Mono + Plus Jakarta Sans + Noto Sans
- 🐛 **Bug修复**：移除历史记录加载功能，避免重复记录

### v1.0 (2026-04-11)
- ✅ 支持中英日三语 WER/CER 计算
- ✅ 详细对比视图（蓝/红/绿高亮）
- ✅ 历史记录管理（支持语种过滤）
- ✅ 标题输入功能
- ✅ 响应式界面设计
- ✅ 局域网共享访问
- ✅ 36个测试用例覆盖

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- 开发工具：[Cursor](https://cursor.sh/) / [Trae](https://trae.ai/)
- 算法参考：动态规划编辑距离算法
- 项目开发：本项目由 [Trae](https://trae.ai/) AI 助手协助完成

---

Made with ❤️ for ASR developers
