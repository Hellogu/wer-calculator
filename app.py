"""
Flask 主应用
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

from calculator import calculate_metric
from database import init_db, save_record, get_all_records, get_records_by_language, get_record_by_id, delete_record, clear_all_records, migrate_add_alignment

app = Flask(__name__)
CORS(app)

# 初始化数据库
init_db()

# 迁移：添加 alignment 字段（如果旧表没有该字段）
migrate_add_alignment()


@app.route('/')
def index():
    """主页面"""
    return send_from_directory('static', 'index.html')


@app.route('/history')
def history_page():
    """历史记录页面"""
    return send_from_directory('static', 'history.html')


@app.route('/static/<path:path>')
def serve_static(path):
    """静态文件"""
    return send_from_directory('static', path)


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """计算 WER/CER"""
    try:
        data = request.get_json()

        language = data.get('language', 'en')
        reference = data.get('reference', '')
        hypothesis = data.get('hypothesis', '')
        skip_save = data.get('skip_save', False)

        if not reference or not hypothesis:
            return jsonify({
                'success': False,
                'error': '参考文本和识别文本不能为空'
            }), 400

        # 计算指标
        result = calculate_metric(reference, hypothesis, language)

        # 获取标题（可选）
        title = data.get('title', '')

        # 保存到历史记录（包含详细统计），除非 skip_save 为 True
        if not skip_save:
            # 将 alignment 序列化为 JSON 字符串
            alignment_json = json.dumps(result['alignment']) if 'alignment' in result else None
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
                hypothesis=hypothesis,
                alignment=alignment_json
            )

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """获取历史记录，支持按语言过滤"""
    try:
        language = request.args.get('language')
        if language:
            records = get_records_by_language(language)
        else:
            records = get_all_records()
        return jsonify({
            'success': True,
            'data': records
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/<int:record_id>', methods=['GET'])
def get_history_record(record_id):
    """获取单条历史记录详情"""
    try:
        record = get_record_by_id(record_id)
        if record:
            return jsonify({
                'success': True,
                'data': record
            })
        else:
            return jsonify({
                'success': False,
                'error': '记录不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    """删除单条历史记录"""
    try:
        success = delete_record(record_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({
                'success': False,
                'error': '记录不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """清空所有历史记录"""
    try:
        clear_all_records()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    import webbrowser
    import threading
    
    print("=" * 60)
    print("  wer-calculator - ASR WER/CER Calculator v1.0")
    print("=" * 60)
    print("本地访问:    http://localhost:5000")
    print("局域网访问:  http://<本机IP>:5000")
    print("-" * 60)
    print("提示: 按 Ctrl+C 可以关闭应用")
    print("=" * 60)
    
    # 延迟打开浏览器
    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 监听所有网卡，允许局域网访问
    app.run(host='0.0.0.0', port=5000, debug=False)
