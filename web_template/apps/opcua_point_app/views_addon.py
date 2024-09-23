import json
import os
import numpy as np
import pandas as pd
import redis
from flask import request, flash, redirect, render_template, session, jsonify, url_for, g

from web_template.extensions import db
from .models import OPCUAPoint

from . import opcua_app


@opcua_app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # 检查是否有上传文件
    if not session.get('device_name'):
        return jsonify({'status': False, 'message': "please set device name first!"})
    if 'file' not in request.files:
        return jsonify({'status': False, 'message': "No file part"})

    file = request.files['file']

    # 如果没有选择文件，返回错误
    if file.filename == '':
        return jsonify({'status': False, 'message': "No selected file"})

    if file and allowed_file(file.filename):
        # 保存上传的文件到服务器的临时目录
        file_path = os.path.join(r'E:\TH\core\web_template\apps\opcua_point_app\uploads', file.filename)
        file.save(file_path)

        # 解析Excel文件并将数据存入数据库
        try:
            parse_excel(file_path, session.get('device_name'), session.get('device_id'))
            return jsonify({'status': False, 'message': "File uploaded and data inserted successfully!"})
        except Exception as e:
            return jsonify({'status': False, 'message': f"{str(e)}"})
    else:
        return jsonify({'status': False, 'message': "Invalid file type"})


def allowed_file(filename):
    # 检查文件后缀名
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']


def parse_excel(file_path, device_name, device_id):
    # 使用pandas读取Excel文件
    df = pd.read_excel(file_path, sheet_name=device_name)

    tag_id_to_node_id_map = {}

    tag_id_to_detail_map = {}

    # 增加之前先删除
    p_list = OPCUAPoint.query.filter(OPCUAPoint.device_id == device_id).all()
    for p in p_list:
        p.delete()

    # 遍历每一行并将数据插入到数据库
    for index, row in df.iterrows():
        tag_id_to_node_id_map[row['node_id']] = row['tag_uuid']
        row.pop('No')
        data = OPCUAPoint(**row)
        data.device_id = int(session.get('device_id'))
        tag_id_to_detail_map[row['tag_uuid']] = data.to_dict()
        data.save()

    # 将需要的数据放到内存中，供adapter引擎调用
    session['tag_id_to_node_id_map'] = json.dumps(tag_id_to_node_id_map)
    session['tag_id_to_detail_map'] = json.dumps(tag_id_to_detail_map)

    # 删除文件，避免占用服务器存储
    os.remove(file_path)


@opcua_app.route('/index')
def index():
    device_id = session.get('device_id')
    device_name = session.get('device_name')
    return render_template('opcua_main.html', device_id=device_id, device_name=device_name)


@opcua_app.route('/set_device', methods=['GET', 'POST'])
def set_device():
    device_id = request.json.get('deviceId')
    device_name = request.json.get('deviceName')
    device_url = request.json.get('deviceUrl')
    session['device_id'] = device_id
    session['device_name'] = device_name
    session['device_url'] = device_url
    return jsonify({'status': True, 'message': 'ok', 'code': 0})


@opcua_app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    device_id = session.get('device_id')
    device_name = session.get('device_name')
    device_url = session.get('device_url')

    if device_id and device_name and device_url:

        device_info = {'device_id': device_id, 'device_name': device_name, 'device_url': device_url}

        opcua_point_list = OPCUAPoint.query.filter(OPCUAPoint.device_id == int(device_id),
                                                   OPCUAPoint.is_deleted == False).all()

        opcua_point_dict_list = [opcua_point.to_dict() for opcua_point in opcua_point_list]

        tag_id_to_node_id_map = {opcua_point['node_id']: opcua_point['tag_uuid'] for opcua_point in opcua_point_dict_list}
        tag_id_to_detail_map = {opcua_point['tag_uuid']: opcua_point for opcua_point in opcua_point_dict_list}

        redis_client = g.redis_client
        # 操作 Redis
        redis_client.set('device_info', json.dumps(device_info))
        redis_client.set('tag_id_to_node_id_map', json.dumps(tag_id_to_node_id_map))
        redis_client.set('tag_id_to_detail_map', json.dumps(tag_id_to_detail_map))
        return jsonify({'status': True, 'message': 'ok', 'code': 0})

    else:
        return jsonify({'status': False, 'message': '请先选择需要deploy的设备', 'code': 0})


@opcua_app.route('/performance', methods=['GET'])
def performance():
    redis_client = g.redis_client
    performance = redis_client.hgetall('performance')
    try:
        thread_status = performance.pop('threads')
    except KeyError:
        thread_status = []
    return render_template('performance_index.html', performance=performance, thread_status=json.loads(thread_status))
