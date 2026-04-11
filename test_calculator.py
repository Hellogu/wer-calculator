"""
WER/CER 计算器全面测试
覆盖基准测试、单错误类型、混合错误、边界条件、语言特性、长文本场景
"""
from calculator import calculate_metric, preprocess_text
from database import init_db, save_record


def save_test_record(title: str, language: str, reference: str, hypothesis: str):
    """保存测试记录到历史记录"""
    result = calculate_metric(reference, hypothesis, language)
    save_record(
        title=title,
        language=language,
        metric=result['metric'],
        result=result['result'],
        total=result['total'],
        substitutions=result['substitutions'],
        deletions=result['deletions'],
        insertions=result['insertions'],
        reference=reference,
        hypothesis=hypothesis
    )
    return result


def test_baseline():
    """基准测试：验证完美匹配和全错场景"""
    print("=" * 60)
    print("【基准测试】完美匹配和全错场景")
    print("=" * 60)
    
    # 英文 - 0% 错误率
    print("\n1. 英文 - 完美匹配 (0% 错误率)")
    ref = "the quick brown fox jumps over the lazy dog"
    hyp = "the quick brown fox jumps over the lazy dog"
    result = save_test_record("[测试]英文完美匹配", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    print(f"[PASS]" if result['result'] == 0.0 else "[FAIL]")
    
    # 英文 - 100% 错误率（完全不同的文本）
    print("\n2. 英文 - 完全不同 (100% 错误率)")
    ref = "hello world"
    hyp = "goodbye moon"
    result = save_test_record("[测试]英文完全不同", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 中文 - 0% 错误率
    print("\n3. 中文 - 完美匹配 (0% 错误率)")
    ref = "今天天气很好"
    hyp = "今天天气很好"
    result = save_test_record("[测试]中文完美匹配", "zh", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    print(f"[PASS]" if result['result'] == 0.0 else "[FAIL]")
    
    # 日文 - 0% 错误率
    print("\n4. 日文 - 完美匹配 (0% 错误率)")
    ref = "こんにちは"
    hyp = "こんにちは"
    result = save_test_record("[测试]日文完美匹配", "ja", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    print(f"[PASS]" if result['result'] == 0.0 else "[FAIL]")


def test_single_error_types():
    """单错误类型测试：隔离验证 S/D/I 计算"""
    print("\n" + "=" * 60)
    print("【单错误类型测试】隔离验证 S/D/I 计算")
    print("=" * 60)
    
    # 纯替换 (Substitution)
    print("\n1. 纯替换 - 英文")
    ref = "cat dog bird"
    hyp = "cat fish bird"
    result = save_test_record("[测试]纯替换-英文", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    print(f"期望: 33.33% (1替换/3词) | [PASS]" if result['substitutions'] == 1 and result['deletions'] == 0 and result['insertions'] == 0 else "[FAIL]")
    
    print("\n2. 纯替换 - 中文")
    ref = "我爱北京天安门"
    hyp = "我爱上海天安门"
    result = save_test_record("[测试]纯替换-中文", "zh", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 纯删除 (Deletion)
    print("\n3. 纯删除 - 英文")
    ref = "the quick brown fox"
    hyp = "the brown fox"
    result = save_test_record("[测试]纯删除-英文", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    print(f"期望: 50% (2删除/4词) | [PASS]" if result['deletions'] == 2 and result['substitutions'] == 0 and result['insertions'] == 0 else "[FAIL]")
    
    print("\n4. 纯删除 - 日文")
    ref = "さくらが咲いています"
    hyp = "さくら咲いています"
    result = save_test_record("[测试]纯删除-日文", "ja", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 纯插入 (Insertion)
    print("\n5. 纯插入 - 英文")
    ref = "hello world"
    hyp = "hello beautiful world"
    result = save_test_record("[测试]纯插入-英文", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    print(f"期望: 50% (1插入/2词) | [PASS]" if result['insertions'] == 1 and result['substitutions'] == 0 and result['deletions'] == 0 else "[FAIL]")
    
    print("\n6. 纯插入 - 中文")
    ref = "你好世界"
    hyp = "你好美丽的世界"
    result = save_test_record("[测试]纯插入-中文", "zh", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")


def test_mixed_errors():
    """混合错误测试：验证 S+D+I 组合场景"""
    print("\n" + "=" * 60)
    print("【混合错误测试】S+D+I 组合场景")
    print("=" * 60)
    
    # S + D
    print("\n1. 替换 + 删除 - 英文")
    ref = "I love programming"
    hyp = "I like coding"
    result = save_test_record("[测试]替换+删除-英文", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # S + I
    print("\n2. 替换 + 插入 - 中文")
    ref = "今天天气不错"
    hyp = "今天天气真的很好"
    result = save_test_record("[测试]替换+插入-中文", "zh", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # D + I
    print("\n3. 删除 + 插入 - 日文")
    ref = "東京タワーが見えます"
    hyp = "東京スカイツリー見えます"
    result = save_test_record("[测试]删除+插入-日文", "ja", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # S + D + I
    print("\n4. 替换 + 删除 + 插入 - 英文")
    ref = "the cat sat on the mat"
    hyp = "a dog sat on mat"
    result = save_test_record("[测试]替换+删除+插入-英文", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 复杂混合
    print("\n5. 复杂混合 - 中文")
    ref = "中华人民共和国成立于一九四九年"
    hyp = "中国成立于一九四九年十月一日"
    result = save_test_record("[测试]复杂混合-中文", "zh", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")


def test_boundary_conditions():
    """边界条件测试：验证鲁棒性"""
    print("\n" + "=" * 60)
    print("【边界条件测试】验证鲁棒性")
    print("=" * 60)
    
    # 空字符串
    print("\n1. 空字符串 vs 空字符串")
    ref = ""
    hyp = ""
    result = save_test_record("[测试]空字符串", "en", ref, hyp)
    print(f"参考: '{ref}'")
    print(f"识别: '{hyp}'")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 空 vs 有内容
    print("\n2. 空字符串 vs 有内容")
    ref = ""
    hyp = "hello world"
    result = save_test_record("[测试]空vs有内容", "en", ref, hyp)
    print(f"参考: '{ref}'")
    print(f"识别: '{hyp}'")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 有内容 vs 空
    print("\n3. 有内容 vs 空字符串")
    ref = "hello world"
    hyp = ""
    result = save_test_record("[测试]有内容vs空", "en", ref, hyp)
    print(f"参考: '{ref}'")
    print(f"识别: '{hyp}'")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 特殊字符
    print("\n4. 特殊字符 - 英文标点")
    ref = "Hello, world! How are you?"
    hyp = "Hello world how are you"
    result = save_test_record("[测试]特殊字符-英文标点", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 中文标点
    print("\n5. 特殊字符 - 中文标点")
    ref = "你好，世界！今天天气真好。"
    hyp = "你好世界今天天气真好"
    result = save_test_record("[测试]特殊字符-中文标点", "zh", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 单字符
    print("\n6. 单字符")
    ref = "a"
    hyp = "b"
    result = save_test_record("[测试]单字符", "en", ref, hyp)
    print(f"参考: '{ref}'")
    print(f"识别: '{hyp}'")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")


def test_language_specific():
    """语言特性测试：验证语言特定处理"""
    print("\n" + "=" * 60)
    print("【语言特性测试】验证语言特定处理")
    print("=" * 60)
    
    # 英文大小写
    print("\n1. 英文大小写不敏感")
    ref = "HELLO WORLD"
    hyp = "hello world"
    result = save_test_record("[测试]英文大小写", "en", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    print(f"[PASS]" if result['result'] == 0.0 else "[FAIL]")
    
    # 英文多空格
    print("\n2. 英文多空格处理")
    ref = "hello   world"
    hyp = "hello world"
    result = save_test_record("[测试]英文多空格", "en", ref, hyp)
    print(f"参考: '{ref}'")
    print(f"识别: '{hyp}'")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 中文空格
    print("\n3. 中文空格处理")
    ref = "你好 世界"
    hyp = "你好世界"
    result = save_test_record("[测试]中文空格", "zh", ref, hyp)
    print(f"参考: '{ref}'")
    print(f"识别: '{hyp}'")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 日文平假名片假名
    print("\n4. 日文平假名片假名")
    ref = "カタカナとひらがな"
    hyp = "かたかなとヒラガナ"
    result = save_test_record("[测试]日文平片假名", "ja", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 混合语言
    print("\n5. 中英混合")
    ref = "Hello你好World世界"
    hyp = "Hello你好Word世界"
    result = save_test_record("[测试]中英混合", "zh", ref, hyp)
    print(f"参考: {ref}")
    print(f"识别: {hyp}")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")


def test_long_text():
    """长文本测试：验证长段文本计算性能"""
    print("\n" + "=" * 60)
    print("【长文本测试】长段文本计算场景")
    print("=" * 60)
    
    # 英文长文本 - 新闻段落
    print("\n1. 英文长文本 - 新闻段落 (约100词)")
    ref = """Artificial intelligence has become one of the most transformative technologies of the 21st century. 
    From healthcare to finance, education to transportation, AI is reshaping industries and creating new 
    opportunities for innovation. Machine learning algorithms can now process vast amounts of data to 
    identify patterns and make predictions with unprecedented accuracy."""
    hyp = """Artificial intelligence has become one of the most transformative technologies of the 21st century. 
    From healthcare to finance, education to transportation, AI is reshaping industries and creating new 
    opportunities for innovation. Machine learning algorithms can now process vast amounts of data to 
    identify patterns and make predictions with unprecedented accuracy."""
    result = save_test_record("[测试]英文长文本-新闻", "en", ref, hyp)
    print(f"参考长度: {len(ref)} 字符, 约 {len(ref.split())} 词")
    print(f"识别长度: {len(hyp)} 字符, 约 {len(hyp.split())} 词")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 英文长文本 - 带错误
    print("\n2. 英文长文本 - 带多个错误 (约100词)")
    ref = """The rapid advancement of technology has fundamentally changed how we communicate, work, and live. 
    Smartphones have become essential tools for daily life, connecting billions of people across the globe. 
    Social media platforms have transformed the way we share information and maintain relationships."""
    hyp = """The rapid advancement of technology has fundamentally changed how we communicate, work, and live. 
    Smartphones have become essential tools for daily life, connecting millions of people around the globe. 
    Social networks have transformed the way we share information and maintain relationships with others."""
    result = save_test_record("[测试]英文长文本-带错误", "en", ref, hyp)
    print(f"参考长度: {len(ref)} 字符, 约 {len(ref.split())} 词")
    print(f"识别长度: {len(hyp)} 字符, 约 {len(hyp.split())} 词")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 中文长文本 - 文章段落
    print("\n3. 中文长文本 - 文章段落 (约200字)")
    ref = """人工智能技术的发展正在深刻改变我们的生活方式。从智能手机到自动驾驶汽车，
    从语音助手到推荐系统，AI技术已经渗透到我们日常生活的方方面面。
    这些技术不仅提高了效率，还为解决复杂问题提供了新的思路和方法。
    未来，随着技术的不断进步，人工智能将在更多领域发挥重要作用。"""
    hyp = """人工智能技术的发展正在深刻改变我们的生活方式。从智能手机到自动驾驶汽车，
    从语音助手到推荐系统，AI技术已经渗透到我们日常生活的方方面面。
    这些技术不仅提高了效率，还为解决复杂问题提供了新的思路和方法。
    未来，随着技术的不断进步，人工智能将在更多领域发挥重要作用。"""
    result = save_test_record("[测试]中文长文本-文章", "zh", ref, hyp)
    print(f"参考长度: {len(ref)} 字符")
    print(f"识别长度: {len(hyp)} 字符")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 中文长文本 - 带错误
    print("\n4. 中文长文本 - 带多个错误 (约200字)")
    ref = """北京故宫博物院是中国最大的古代文化艺术博物馆，建立于1925年10月10日。
    它位于北京紫禁城内，是在明朝、清朝两代皇宫及其收藏的基础上建立起来的综合性博物馆。
    故宫博物院占地面积约72万平方米，建筑面积约15万平方米，有大小宫殿七十多座，房屋九千余间。"""
    hyp = """北京故宫是中国最大的古代文化艺术博物馆，建立于1925年10月。
    它位于北京紫禁城内，是在明朝、清朝两代皇宫及其收藏的基础上建立起来的综合性博物馆。
    故宫博物院占地面积约72万平方米，建筑面积约15万平方米，有大小宫殿七十多座，房屋八千多间。"""
    result = save_test_record("[测试]中文长文本-带错误", "zh", ref, hyp)
    print(f"参考长度: {len(ref)} 字符")
    print(f"识别长度: {len(hyp)} 字符")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 日文长文本
    print("\n5. 日文长文本 - 文章段落")
    ref = """日本の四季はとても美しいです。春には桜が咲き、夏には花火大会があります。
    秋には紅葉が美しく、冬には雪景色が楽しめます。
    どの季節も魅力的で、観光客を魅了しています。"""
    hyp = """日本の四季はとても美しいです。春には桜が咲き、夏には花火大会があります。
    秋には紅葉が美しく、冬には雪景色が楽しめます。
    どの季節も魅力的で、観光客を魅了しています。"""
    result = save_test_record("[测试]日文长文本-文章", "ja", ref, hyp)
    print(f"参考长度: {len(ref)} 字符")
    print(f"识别长度: {len(hyp)} 字符")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 超长文本 - 模拟ASR长语音
    print("\n6. 超长文本 - 模拟ASR长语音 (约500字)")
    ref = """各位听众朋友们，大家好。欢迎收听今天的科技新闻栏目。
    今天我们要讨论的话题是人工智能在医疗领域的应用。
    近年来，随着深度学习技术的突破，AI在医学影像诊断、药物研发、个性化治疗等方面取得了显著进展。
    例如，在肺癌早期筛查中，AI系统已经可以辅助医生识别CT影像中的微小结节，准确率甚至超过了经验丰富的放射科医生。
    在药物研发方面，传统的药物开发周期通常需要10到15年，成本高达数十亿美元。
    而借助人工智能技术，研究人员可以更快地筛选候选化合物，预测药物与靶点的相互作用，从而大幅缩短研发周期。
    当然，AI在医疗领域的应用也面临着数据隐私、算法偏见、监管审批等挑战。
    我们需要在推动技术创新的同时，确保患者的权益得到充分保护。
    感谢大家的收听，我们下期节目再见。"""
    hyp = """各位听众朋友们，大家好。欢迎收听今天的科技新闻栏目。
    今天我们要讨论的话题是人工智能在医疗领域的应用。
    近年来，随着深度学习技术的突破，AI在医学影像诊断、药物研发、个性化治疗等方面取得了显著进展。
    例如，在肺癌早期筛查中，人工智能系统已经可以辅助医生识别CT影像中的微小结节，准确率甚至超过了经验丰富的放射科医生。
    在药物研发方面，传统的药物开发周期通常需要10到15年，成本高达数十亿美元。
    而借助AI技术，研究人员可以更快地筛选候选化合物，预测药物与靶点的相互作用，从而大幅缩短研发周期。
    当然，人工智能在医疗领域的应用也面临着数据隐私、算法偏见、监管审批等挑战。
    我们需要在推动技术创新的同时，确保患者的权益得到充分保护。
    感谢大家的收听，我们下期节目再见。"""
    result = save_test_record("[测试]超长文本-ASR模拟", "zh", ref, hyp)
    print(f"参考长度: {len(ref)} 字符")
    print(f"识别长度: {len(hyp)} 字符")
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")


def test_real_world_scenarios():
    """真实场景测试：模拟实际ASR使用场景"""
    print("\n" + "=" * 60)
    print("【真实场景测试】模拟实际ASR使用场景")
    print("=" * 60)
    
    # 会议转录场景
    print("\n1. 会议转录场景 - 中文")
    ref = """首先，我们来回顾一下上季度的销售业绩。总体上来说，我们的营收增长了百分之十五，
    这主要得益于新产品的成功推出。但是，我们也注意到客户流失率有所上升，
    这需要我们在下个季度重点关注。接下来，请各部门负责人汇报一下具体的情况。"""
    hyp = """首先，我们来回顾一下上季度的销售业绩。总体上来说，我们的营收增长了百分之十五，
    这主要得益于新产品的成功推出。但是，我们也注意到客户流失率有所上升，
    这需要我们在下个季度重点关注。接下来，请各部门负责人汇报一下具体的情况。"""
    result = save_test_record("[场景]会议转录-中文", "zh", ref, hyp)
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 客服对话场景
    print("\n2. 客服对话场景 - 中文")
    ref = "您好，请问有什么可以帮您？好的，我帮您查询一下订单状态。请提供您的订单号。"
    hyp = "你好，请问有什么可以帮您？好的，我帮您查一下订单状态。请提供您的订单号。"
    result = save_test_record("[场景]客服对话-中文", "zh", ref, hyp)
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 英文播客场景
    print("\n3. 英文播客场景")
    ref = "Welcome to our podcast. Today we're going to talk about the future of renewable energy."
    hyp = "Welcome to our podcast. Today we're gonna talk about the future of renewable energy."
    result = save_test_record("[场景]英文播客", "en", ref, hyp)
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")
    
    # 日文动漫台词场景
    print("\n4. 日文动漫台词场景")
    ref = "お前はもう死んでいる。何！？そんなバカな！"
    hyp = "お前はもう死んでいる。なに！？そんな馬鹿な！"
    result = save_test_record("[场景]日文动漫台词", "ja", ref, hyp)
    print(f"结果: {result['metric']} {result['result']}% | S:{result['substitutions']} D:{result['deletions']} I:{result['insertions']} 总:{result['total']}")


if __name__ == '__main__':
    # 初始化数据库
    init_db()
    
    print("\n")
    print("*" * 60)
    print("WER/CER 计算器全面测试")
    print("*" * 60)
    print("\n所有测试结果将保存到历史记录中")
    print("-" * 60)
    
    # 执行所有测试
    test_baseline()
    test_single_error_types()
    test_mixed_errors()
    test_boundary_conditions()
    test_language_specific()
    test_long_text()
    test_real_world_scenarios()
    
    print("\n" + "*" * 60)
    print("测试完成！所有结果已保存到历史记录")
    print("请在浏览器中访问 http://localhost:5000/history 查看")
    print("*" * 60)
