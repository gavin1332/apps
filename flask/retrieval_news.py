from flask import Flask
from flask import request
from flask import render_template

import json
import urllib2
import urllib


def parse_user(json_str):
    if json_str == '[]':
        return []

    dom = json.loads(json_str)
    primary_category = []
    for k, v in dom['primary_category'].items():
        vstr = k + '(' + str(v[1][0]) + ')'
        primary_category.append(vstr) 
    primary_category.sort(key=lambda x:float(x.split('(')[-1].strip(')')), reverse = True)

    secondary_category = []
    for k, v in dom['secondary_category'].items():
        vstr = k + '(' + str(v[1][0]) + ')'
        secondary_category.append(vstr) 
    secondary_category.sort(key=lambda x:float(x.split('(')[-1].strip(')')), reverse = True)

    general_tag = []
    for k, v in dom['general_tag'].items():
        vstr = k + '(' + str(v[1][0]) + ')'
        general_tag.append(vstr)
    general_tag.sort(key=lambda x:float(x.split('(')[-1].strip(')')), reverse = True)

    attention = []
    for k, v in dom['attention_statics']['click_show'].items():
        vstr = k + '(' + str(v[1][0]) + ')'
        attention.append(vstr)
    attention.sort(key=lambda x:float(x.split('(')[-1].strip(')')), reverse = True)

    pcate = ','.join(primary_category[0:min(10, len(primary_category))])
    scate = ','.join(secondary_category[0:min(10, len(secondary_category))])
    attention = ','.join(attention[0:min(20, len(attention))])
    gtag = ','.join(general_tag[0:min(50, len(general_tag))])
    return [[pcate, scate, attention, gtag]]


def get_user(uid):
    url = 'http://10.128.88.47:8088/topic/api/attention?req_target=usermodel&cuid=' + uid
    post_args = {'req_target':'usermodel', 'cuid':uid}
    post_args_json = json.dumps(post_args)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req, timeout=1000)
    ret = response.read()

    heads = ['primary_cate', 'secondary_cate', 'attention_statics', 'general_tag']
    return heads, parse_user(ret)


def parse_items(json_str):
    if json_str == '[]':
        return []

    dom = json.loads(json_str, encoding='utf-8')
    #dom = json.loads(json_str)
    err_no = dom['err_no']
    err_msg = dom['err_msg']
    data = dom['items']

    outputs = []
    seg_index = 0
    item_index = 0
    for each_seg in data:
        seg_index += 1
        q_ann_sum = str(each_seg['q_ann_sum'])
        score = str(each_seg['score'])
        for i in range(3):
            item_index += 1
            nid = each_seg['nid'][i]
            news_attention = each_seg['nid'][i]
            vertical_type = each_seg['vertical_type'][i]
            display_strategy = each_seg['display_strategy'][i]
            cs = each_seg['cs'][i]
            ext_dict = json.loads(each_seg['ext'][i], encoding='utf-8')

            news_cate = ext_dict['new_cate']
            news_cat = ext_dict['new_cat']
            news_cate = news_cate if news_cate != '' else news_cat

            news_sub_cate = ext_dict['new_sub_cate']
            news_sub_cat = ext_dict['new_sub_cat']
            news_sub_cate = news_sub_cate if news_sub_cate != '' else news_sub_cat

            news_attention = json.loads(each_seg['news_attention'][i], encoding='utf-8')
            news_attention = ','.join([kv[0] + ':' + str(kv[1]) for kv in news_attention])
            outputs.append([nid, str(seg_index), str(item_index), score, news_cate, news_sub_cate,
                    news_attention, vertical_type])

    return outputs


addr_map = {
        'bj':'10.146.140.31:8756',
        'sz':'10.233.16.13:8756',
        'nj':'10.233.16.13:8756',
        'gz':'10.186.102.15:8756',
        'qa':'10.99.70.62:8003',
        }
def get_items(uid, addr):
    url = 'http://%s/SegmentRetrievalService/Retrieve' % addr
    post_args = {'user':{'cuid':uid}, 'retrieval_num':200, 'request_feature':{'product': 1}, 'use_request_feature_cache':False}
    post_args_json = json.dumps(post_args)
    req = urllib2.Request(url, post_args_json)
    req.add_header('log-id', '984523497')
    response = urllib2.urlopen(req)
    ret = response.read()

    heads = ['nid', 'seg_idx', 'item_idx', 'seg_score', 'cate', 'sub_cate', 'news_attention', 'vtype']
    return heads, parse_items(ret)


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/favicon.ico')
def favicon():
    return 'Hello World'

@app.route('/<string:uid>')
def retrieval(uid):
    addr_key = request.args.get('addr', default='bj', type=str)
    addr = addr_map.get(addr_key, addr_map.get('bj'))
    title = 'uid:' + uid
    print uid
    sub_title = ['User Model', 'Retrieval News (%s)' % addr]
    layout = [False, True]
    user_head, user_content = get_user(uid)
    news_head, news_content = get_items(uid, addr)
    head = [user_head, news_head]
    items = [user_content, news_content]
    return render_template('table.html', title=title, sub_title=sub_title, layout=layout, head=head, items=items, addr=addr)
