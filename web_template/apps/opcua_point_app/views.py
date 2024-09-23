from flask import render_template, request, jsonify, session
from sqlalchemy import asc, desc

from . import opcua_app
from .config import ONE_SIDE_API_NAME, ONE_SIDE_MODEL_NAME, ONE_SIDE_SEARCH_BY, ONE_SIDE_FORM_INFO, \
    ONE_SIDE_FORM_INFO_VALIDATE, MANY_SIDE_API_NAME, MANY_SIDE_MODEL_NAME, MANY_SIDE_FORM_INFO_VALIDATE, \
    ONE_SIDE_TEMPLATE_NAME, MANY_SIDE_TEMPLATE_NAME, MANY_SIDE_FORM_INFO, ONE_TO_MANY_DISPLAY, ONE_LINK_MANY_COLUMN, \
    MANY_SIDE_DISPLAY_NAME, MANY_SIDE_PROGRAM_ID, MANY_TO_ONE_DISPLAY, ONE_SIDE_DISPLAY_NAME, \
    ONE_SIDE_DISPLAY_NAME_IN_LIST


@opcua_app.route(f'/api/{ONE_SIDE_API_NAME}/', defaults={'id': None}, methods=['GET', 'POST'])
@opcua_app.route(f'/api/{ONE_SIDE_API_NAME}/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_one_side_items(id):
    device_id = session.get('device_id')
    device_name = session.get('device_name')
    if request.method == 'GET':
        many_info = MANY_SIDE_MODEL_NAME.query.filter_by(is_deleted=False).all()
        _x, _y = ONE_TO_MANY_DISPLAY
        many_info_display = [[info.to_dict().get(_x), info.to_dict().get(_y)] for info in many_info]
        if id:
            # 查询单条记录
            item = ONE_SIDE_MODEL_NAME.query.filter_by(id=id, is_deleted=False).first()
            # 查询单条记录的所有的多对多字段
            many_side_program_id_list = [many_side_obj.to_dict()[MANY_SIDE_PROGRAM_ID] for many_side_obj in
                                         getattr(item, ONE_LINK_MANY_COLUMN)]

            result = {}
            result.update(item.to_dict())
            result.update({ONE_LINK_MANY_COLUMN: many_side_program_id_list})
            if item:
                return jsonify(result)
            else:
                return jsonify({'error': f'{ONE_SIDE_API_NAME} not found'}), 404
        else:
            # 查询所有记录
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            sort_by = request.args.get('sort_by', 'id')
            order = request.args.get('order', 'asc')
            search = request.args.get('search', '')

            query = ONE_SIDE_MODEL_NAME.query.filter_by(is_deleted=False)

            if search:
                query = query.filter(getattr(ONE_SIDE_MODEL_NAME, ONE_SIDE_SEARCH_BY).contains(search))

            if order == 'asc':
                query = query.order_by(asc(getattr(ONE_SIDE_MODEL_NAME, sort_by)))
            else:
                query = query.order_by(desc(getattr(ONE_SIDE_MODEL_NAME, sort_by)))

            items = query.paginate(page=page, per_page=per_page, count=True)

            result = []
            # 需要将一方关联的多方按照其名称展示成列表
            for item in items:
                _d = {}
                many_side_display_list = [many_side_obj.to_dict()[MANY_SIDE_DISPLAY_NAME] for many_side_obj in
                                          getattr(item, ONE_LINK_MANY_COLUMN)]
                _d.update(item.to_dict())
                _d.update({ONE_LINK_MANY_COLUMN: many_side_display_list})
                result.append(_d)

            total_page = items.total // items.per_page
            total_page += 1
            return render_template(f'{ONE_SIDE_TEMPLATE_NAME}.html', form_info=ONE_SIDE_FORM_INFO, total=items.total,
                                   page=items.page,
                                   total_page=total_page,
                                   per_page=items.per_page,
                                   items=result,
                                   page_obj=items,
                                   many_info_display=many_info_display,
                                   device_id=device_id,
                                   device_name=device_name
                                   )
    elif request.method == 'POST':
        data = request.json
        # 传递过来的数据，只能多于等于column_list, 不能column_list有这个数据，但是传递过来的data没有这个数据
        if _ := data.keys() - set(ONE_SIDE_FORM_INFO_VALIDATE['column_list']):
            if not len(_) > 0:
                return jsonify({
                    'message': f'required {list(set(ONE_SIDE_FORM_INFO_VALIDATE["column_list"]) - data.keys())}, but not give!'}), 500
        new_data = {}
        for column in ONE_SIDE_FORM_INFO_VALIDATE['column_list']:
            if isinstance(data[column], ONE_SIDE_FORM_INFO_VALIDATE[column]['type']):
                # 判断传递过来的数据类型是否满足要求
                new_data[column] = data[column]
            else:
                return jsonify({
                    'message': f'{column} should be type {ONE_SIDE_FORM_INFO_VALIDATE[column]["type"]},but got type {type(data[column])}'}), 500
        # 创建对象
        new_data_copy = new_data.copy()
        new_data.pop(ONE_LINK_MANY_COLUMN)
        new_item = ONE_SIDE_MODEL_NAME(**new_data)
        # 获取多有的多方对象
        for many_side_id in new_data_copy[ONE_LINK_MANY_COLUMN]:
            # 获取多方对象
            many_side_obj = MANY_SIDE_MODEL_NAME.query.get(many_side_id)
            if many_side_obj:
                # 将多方对象中append进来
                getattr(new_item, ONE_LINK_MANY_COLUMN).append(many_side_obj)
        # 将这个对象完成的保存
        new_item.save()

        return jsonify({'message': f'{ONE_SIDE_API_NAME}'.replace('s', '') + 'created!'}), 201

    elif request.method == 'PUT':
        item = ONE_SIDE_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{ONE_SIDE_MODEL_NAME} not found'}), 404
        data = request.json
        new_data = data.copy()
        new_data.pop(ONE_LINK_MANY_COLUMN)
        # print(data[ONE_LINK_MANY_COLUMN])  # ['1', '2', '3']
        # 对多方对象进行处理
        new_obj = set()
        for id in data[ONE_LINK_MANY_COLUMN]:
            _item = MANY_SIDE_MODEL_NAME.query.get(id)
            if _item:
                new_obj.add(_item)
        raw_obj = set(getattr(item, ONE_LINK_MANY_COLUMN))
        # 第一种方式：传递过来的对象id，比原来的对象增加
        if _add_obj := new_obj - raw_obj:
            for _item in _add_obj:
                getattr(item, ONE_LINK_MANY_COLUMN).append(_item)
        # 第二种方式：传递过来的对象id,比原来的对象减少
        elif _sub_obj := raw_obj - new_obj:
            for _item in _sub_obj:
                getattr(item, ONE_LINK_MANY_COLUMN).remove(_item)
        item.update_fields(**new_data)
        return jsonify({'message': f'{ONE_SIDE_API_NAME}'.replace('s', '') + 'updated!'})
    elif request.method == 'DELETE':
        item = ONE_SIDE_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{ONE_SIDE_API_NAME}'.replace('s', '') + 'not found'}), 404
        item.soft_delete()
        return jsonify({'message': f'{ONE_SIDE_API_NAME}'.replace('s', '') + 'deleted!'})


@opcua_app.route(f'/api/{MANY_SIDE_API_NAME}/', defaults={'id': None}, methods=['GET', 'POST'])
@opcua_app.route(f'/api/{MANY_SIDE_API_NAME}/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_many_side_items(id):
    device_id = session.get('device_id') or 1
    device_name = session.get('device_name')
    if request.method == 'GET':
        one_info = ONE_SIDE_MODEL_NAME.query.filter_by(is_deleted=False).all()
        _x, _y = MANY_TO_ONE_DISPLAY
        one_info_display = [[info.to_dict().get(_x), info.to_dict().get(_y)] for info in one_info]
        if id:
            # 查询单条记录
            item = MANY_SIDE_MODEL_NAME.query.filter_by(id=id, is_deleted=False).first()
            if item:
                _item = item.to_dict()
                _item[f'{ONE_SIDE_DISPLAY_NAME}_id'] = getattr(item, f'{ONE_SIDE_DISPLAY_NAME}_id')
                return jsonify(_item)
            else:
                return jsonify({'error': f'{MANY_SIDE_API_NAME} not found'}), 404
        else:
            # 查询所有记录
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            sort_by = request.args.get('sort_by', 'id')
            order = request.args.get('order', 'asc')
            search = request.args.get('search', '')

            query = MANY_SIDE_MODEL_NAME.query.filter(MANY_SIDE_MODEL_NAME.is_deleted==False, MANY_SIDE_MODEL_NAME.device_id==int(device_id))

            if search:
                query = query.filter(getattr(MANY_SIDE_MODEL_NAME, ONE_SIDE_SEARCH_BY).contains(search))

            if order == 'asc':
                query = query.order_by(asc(getattr(MANY_SIDE_MODEL_NAME, sort_by)))
            else:
                query = query.order_by(desc(getattr(MANY_SIDE_MODEL_NAME, sort_by)))

            items = query.paginate(page=page, per_page=per_page, count=True)

            total_page = items.total // items.per_page
            total_page += 1
            result = []
            for item in items.items:
                if item:
                    _item = item.to_dict()
                    if getattr(item, ONE_SIDE_DISPLAY_NAME):
                        _item[ONE_SIDE_DISPLAY_NAME] = getattr(getattr(item, ONE_SIDE_DISPLAY_NAME),
                                                               ONE_SIDE_DISPLAY_NAME_IN_LIST)
                    result.append(_item)
            return render_template(f'{MANY_SIDE_TEMPLATE_NAME}.html', form_info=MANY_SIDE_FORM_INFO, total=items.total,
                                   page=items.page,
                                   total_page=total_page,
                                   per_page=items.per_page,
                                   items=result,
                                   page_obj=items, one_info_display=one_info_display, device_id=device_id,
                                   device_name=device_name)
    elif request.method == 'POST':
        data = request.json
        if _ := data.keys() - set(MANY_SIDE_FORM_INFO_VALIDATE['column_list']):
            if not len(_) > 0:
                return jsonify({
                    'message': f'required {list(set(MANY_SIDE_FORM_INFO_VALIDATE["column_list"]) - data.keys())}, but not give!'}), 500
        new_data = {}
        print(data)
        for column in MANY_SIDE_FORM_INFO_VALIDATE['column_list']:
            if isinstance(data[column], MANY_SIDE_FORM_INFO_VALIDATE[column]['type']):
                new_data[column] = data[column]
            else:
                return jsonify({
                    'message': f'{column} should be type {MANY_SIDE_FORM_INFO_VALIDATE[column]["type"]},but got type {type(data[column])}'}), 500
        print(new_data)
        new_item = MANY_SIDE_MODEL_NAME(**new_data)
        new_item.save()
        return jsonify({'message': f'{MANY_SIDE_API_NAME}'.replace('s', '') + 'created!'}), 201
    elif request.method == 'PUT':
        item = MANY_SIDE_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_MODEL_NAME} not found'}), 404
        data = request.json
        item.update_fields(**data)
        return jsonify({'message': 'User updated!'})
    elif request.method == 'DELETE':
        item = MANY_SIDE_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_API_NAME}'.replace('s', '') + 'not found'}), 404
        item.soft_delete()
        return jsonify({'message': f'{MANY_SIDE_API_NAME}'.replace('s', '') + 'deleted!'})
