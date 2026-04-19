"""
Flask 主应用
"""
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import os
import json
import csv
import io

from calculator import calculate_wer_cer as calculate_metric
from database import init_db, save_record, get_all_records, get_records_by_language, get_record_by_id, delete_record, clear_all_records, migrate_add_alignment, update_record_title, search_records_by_title

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


@app.route('/api/history/<int:record_id>/title', methods=['PUT'])
def update_history_title(record_id):
    """更新历史记录标题"""
    try:
        data = request.get_json()
        title = data.get('title', '')

        success = update_record_title(record_id, title)
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


@app.route('/api/history/search', methods=['GET'])
def search_history():
    """搜索历史记录（按标题）"""
    try:
        keyword = request.args.get('keyword', '')
        language = request.args.get('language')

        if not keyword:
            return jsonify({
                'success': False,
                'error': '请提供搜索关键词'
            }), 400

        records = search_records_by_title(keyword, language)
        return jsonify({
            'success': True,
            'data': records
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/export', methods=['GET'])
def export_history():
    """导出历史记录为CSV"""
    try:
        # 获取导出范围参数
        export_scope = request.args.get('scope', 'all')  # 'all' 或 'filtered'
        language = request.args.get('language')
        keyword = request.args.get('keyword')

        # 获取记录数据
        if export_scope == 'filtered':
            # 导出筛选结果
            if keyword:
                records = search_records_by_title(keyword, language)
            elif language:
                records = get_records_by_language(language)
            else:
                records = get_all_records()
        else:
            # 导出全部
            records = get_all_records()

        if not records:
            return jsonify({
                'success': False,
                'error': '没有可导出的记录'
            }), 400

        # 创建CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # 写入表头（中文）
        headers = ['ID', '标题', '时间', '语言', '参考文本', '识别文本', '指标', '错误率', '替换数', '删除数', '插入数', '总数']
        writer.writerow(headers)

        # 语言映射
        lang_map = {'en': '英文', 'zh': '中文', 'ja': '日文'}

        # 写入数据
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

        # 获取CSV内容
        csv_content = output.getvalue()
        output.close()

        # 添加BOM以支持Excel中文显示
        csv_content = '\ufeff' + csv_content

        # 生成文件名
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"wer_history_{timestamp}.csv"

        # 返回CSV文件
        response = Response(
            csv_content.encode('utf-8'),
            mimetype='text/csv; charset=utf-8',
            headers={
                'Content-Disposition': f'attachment; filename={filename}',
                'Content-Type': 'text/csv; charset=utf-8'
            }
        )
        return response

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
