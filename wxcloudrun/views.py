from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import searchspider
import vidspider
import kepuspider
import pricespider
import zhaoyaospider
import json
import yyw_spider
import xywy_spider
import yywspider_v2
import jdspider_v2

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/api/search', methods=['POST'])
def get_search():
    
    s = searchspider.spider()

    params = request.get_json()

    if 'word' not in params:
        return make_err_response('缺少word参数')

    word = params['word']
    
    result_json = json.dumps(s.run(word))

    return result_json


@app.route('/api/vidsearch', methods=['POST'])
def get_vidsearch():
    
    s = vidspider.vidspider()

    params = request.get_json()

    if 'word' not in params:
        return make_err_response('缺少word参数')

    word = params['word']
    
    result_json = json.dumps(s.run(word))

    return result_json


@app.route('/api/kepusearch', methods=['POST'])
def get_kepusearch():
    
    s = kepuspider.kepuspider()
    
    result_json = json.dumps(s.run())

    return result_json


@app.route('/api/pricesearch', methods=['POST'])
def get_pricesearch():
    
    s = pricespider.pricespider()

    params = request.get_json()

    if 'word' not in params:
        return make_err_response('缺少word参数')

    word = params['word']
    
    result_json = json.dumps(s.run(word))

    return result_json



@app.route('/api/zhaoyaosearch', methods=['POST'])
def get_zhaoyaosearch():
    
    s = zhaoyaospider.zhaoyaospider()
    
    result_json = json.dumps(s.run())

    return result_json


@app.route('/api/xywysearch', methods=['POST'])
def get_xywysearch():
    
    s = xywy_spider.xywy_spider()

    params = request.get_json()

    if 'word' not in params:
        return make_err_response('缺少word参数')

    word = params['word']
    
    result_json = json.dumps(s.run(word))

    return result_json


@app.route('/api/yywsearch', methods=['POST'])
def get_yywsearch():
    
    s = yyw_spider.yyw_spider()

    params = request.get_json()

    if 'word' not in params:
        return make_err_response('缺少word参数')

    word = params['word']
    
    result_json = json.dumps(s.run(word))

    return result_json


@app.route('/api/yywsearch_v2', methods=['POST'])
def get_yywsearch_v2():
    
    s = yywspider_v2.yywspider_v2

    params = request.get_json()

    if 'word' not in params:
        return make_err_response('缺少word参数')

    word = params['word']
    
    result_json = json.dumps(s.get_html(word))

    return result_json

@app.route('/api/jdsearch_v2', methods=['POST'])
def get_jdsearch_v2():
    
    s = jdspider_v2.jdspider_v2

    params = request.get_json()

    if 'word' not in params:
        return make_err_response('缺少word参数')

    word = params['word']
    
    result_json = json.dumps(s.get_html(word))

    return result_json