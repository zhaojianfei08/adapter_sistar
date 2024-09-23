from flask import render_template, request, jsonify
from sqlalchemy import asc, desc

from web_template.rbac import login_required, check_permission
from . import user_role_permisson_app
from .config import MANY_SIDE_A_API_NAME, MANY_SIDE_B_MODEL_NAME, A_TO_B_DISPLAY, MANY_SIDE_A_MODEL_NAME, \
    A_LINK_B_PROGRAM_ID, A_LINK_B_COLUMN, MANY_SIDE_A_SEARCH_BY, MANY_SIDE_A_TEMPLATE_NAME, MANY_SIDE_A_FORM_INFO, \
    MANY_SIDE_A_FORM_INFO_VALIDATE, A_LINK_B_DISPLAY_NAME, MANY_SIDE_B_API_NAME, B_TO_A_DISPLAY, MANY_SIDE_B_SEARCH_BY, \
    MANY_SIDE_B_TEMPLATE_NAME, MANY_SIDE_B_FORM_INFO, MANY_SIDE_B_FORM_INFO_VALIDATE, B_LINK_A_DISPLAY_NAME, \
    B_LINK_A_COLUMN, MANY_SIDE_C_API_NAME, B_TO_C_DISPLAY, MANY_SIDE_C_MODEL_NAME, C_LINK_B_COLUMN, C_LINK_B_PROGRAM_ID, \
    MANY_SIDE_C_SEARCH_BY, B_LINK_C_COLUMN, B_LINK_C_DISPLAY_NAME, MANY_SIDE_C_TEMPLATE_NAME, MANY_SIDE_C_FORM_INFO, \
    MANY_SIDE_C_FORM_INFO_VALIDATE, C_TO_B_DISPLAY


@user_role_permisson_app.route(f'/api/{MANY_SIDE_A_API_NAME}/', defaults={'id': None}, methods=['GET', 'POST'])
@user_role_permisson_app.route(f'/api/{MANY_SIDE_A_API_NAME}/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required()
@check_permission()
def get_side_A_items(id):
    if request.method == 'GET':
        many_side_B_info = MANY_SIDE_B_MODEL_NAME.query.filter_by(is_deleted=False).all()
        _x, _y = A_TO_B_DISPLAY
        many_side_B_info_display = [[info.to_dict().get(_x), info.to_dict().get(_y)] for info in many_side_B_info]
        if id:
            # 查询单条记录
            item = MANY_SIDE_A_MODEL_NAME.query.filter_by(id=id, is_deleted=False).first()
            # 查询单条记录的所有的多对多字段
            many_side_program_id_list = [many_side_obj.to_dict()[A_LINK_B_PROGRAM_ID] for many_side_obj in
                                         getattr(item, A_LINK_B_COLUMN)]

            result = {}
            result.update(item.to_dict())
            result.update({A_LINK_B_COLUMN: many_side_program_id_list})
            if item:
                return jsonify(result)
            else:
                return jsonify({'error': f'{MANY_SIDE_A_API_NAME} not found'}), 404
        else:
            # 查询所有记录
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            sort_by = request.args.get('sort_by', 'id')
            order = request.args.get('order', 'asc')
            search = request.args.get('search', '')

            query = MANY_SIDE_A_MODEL_NAME.query.filter_by(is_deleted=False)

            if search:
                query = query.filter(getattr(MANY_SIDE_A_MODEL_NAME, MANY_SIDE_A_SEARCH_BY).contains(search))

            if order == 'asc':
                query = query.order_by(asc(getattr(MANY_SIDE_A_MODEL_NAME, sort_by)))
            else:
                query = query.order_by(desc(getattr(MANY_SIDE_A_MODEL_NAME, sort_by)))

            items = query.paginate(page=page, per_page=per_page, count=True)

            result = []
            # 需要将一方关联的多方按照其名称展示成列表
            for item in items:
                _d = {}
                many_side_display_list = [many_side_obj.to_dict()[A_LINK_B_DISPLAY_NAME] for many_side_obj in
                                          getattr(item, A_LINK_B_COLUMN)]
                _d.update(item.to_dict())
                _d.update({A_LINK_B_COLUMN: many_side_display_list})
                result.append(_d)

            total_page = items.total // items.per_page
            total_page += 1
            return render_template(f'{MANY_SIDE_A_TEMPLATE_NAME}.html', form_info=MANY_SIDE_A_FORM_INFO,
                                   total=items.total,
                                   page=items.page,
                                   total_page=total_page,
                                   per_page=items.per_page,
                                   items=result,
                                   page_obj=items,
                                   many_side_B_info_display=many_side_B_info_display
                                   )
    elif request.method == 'POST':
        data = request.json
        # 传递过来的数据，只能多于等于column_list, 不能column_list有这个数据，但是传递过来的data没有这个数据
        if _ := data.keys() - set(MANY_SIDE_A_FORM_INFO_VALIDATE['column_list']):
            if not len(_) > 0:
                return jsonify({
                    'message': f'required {list(set(MANY_SIDE_A_FORM_INFO_VALIDATE["column_list"]) - data.keys())}, but not give!'}), 500
        new_data = {}
        for column in MANY_SIDE_A_FORM_INFO_VALIDATE['column_list']:
            if isinstance(data[column], MANY_SIDE_A_FORM_INFO_VALIDATE[column]['type']):
                # 判断传递过来的数据类型是否满足要求
                new_data[column] = data[column]
            else:
                return jsonify({
                    'message': f'{column} should be type {MANY_SIDE_A_FORM_INFO_VALIDATE[column]["type"]},but got type {type(data[column])}'}), 500
        # 创建对象
        new_data_copy = new_data.copy()
        new_data.pop(A_LINK_B_COLUMN)
        new_item = MANY_SIDE_A_MODEL_NAME(**new_data)
        # 获取多有的多方对象
        for many_side_id in new_data_copy[A_LINK_B_COLUMN]:
            # 获取多方对象
            many_side_obj = MANY_SIDE_B_MODEL_NAME.query.get(many_side_id)
            if many_side_obj:
                # 将多方对象中append进来
                getattr(new_item, A_LINK_B_COLUMN).append(many_side_obj)
        # 将这个对象完成的保存
        new_item.save()

        return jsonify({'message': f'{MANY_SIDE_A_API_NAME}'.replace('s', '') + 'created!'}), 201

    elif request.method == 'PUT':
        item = MANY_SIDE_A_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_A_MODEL_NAME} not found'}), 404
        data = request.json
        new_data = data.copy()
        new_data.pop(A_LINK_B_COLUMN)
        # print(data[ONE_LINK_MANY_COLUMN])  # ['1', '2', '3']
        # 对多方对象进行处理
        new_obj = set()
        for id in data[A_LINK_B_COLUMN]:
            _item = MANY_SIDE_B_MODEL_NAME.query.get(id)
            if _item:
                new_obj.add(_item)
        raw_obj = set(getattr(item, A_LINK_B_COLUMN))
        # 第一种方式：传递过来的对象id，比原来的对象增加
        if _add_obj := new_obj - raw_obj:
            for _item in _add_obj:
                getattr(item, A_LINK_B_COLUMN).append(_item)
        # 第二种方式：传递过来的对象id,比原来的对象减少
        elif _sub_obj := raw_obj - new_obj:
            for _item in _sub_obj:
                getattr(item, A_LINK_B_COLUMN).remove(_item)
        item.update_fields(**new_data)
        return jsonify({'message': f'{MANY_SIDE_A_API_NAME}'.replace('s', '') + 'updated!'})
    elif request.method == 'DELETE':
        item = MANY_SIDE_A_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_A_API_NAME}'.replace('s', '') + 'not found'}), 404
        item.soft_delete()
        return jsonify({'message': f'{MANY_SIDE_A_API_NAME}'.replace('s', '') + 'deleted!'})


@user_role_permisson_app.route(f'/api/{MANY_SIDE_B_API_NAME}/', defaults={'id': None}, methods=['GET', 'POST'])
@user_role_permisson_app.route(f'/api/{MANY_SIDE_B_API_NAME}/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required()
@check_permission()
def get_side_B_items(id):
    if request.method == 'GET':
        many_side_C_info = MANY_SIDE_C_MODEL_NAME.query.filter_by(is_deleted=False).all()
        _x, _y = C_TO_B_DISPLAY
        many_side_C_info_display = [[info.to_dict().get(_x), info.to_dict().get(_y)] for info in many_side_C_info]
        if id:
            # 查询单条记录
            item = MANY_SIDE_B_MODEL_NAME.query.filter_by(id=id, is_deleted=False).first()
            # 查询单条记录的所有的多对多字段
            many_side_program_id_list = [many_side_obj.to_dict()[A_LINK_B_PROGRAM_ID] for many_side_obj in
                                         getattr(item, B_LINK_C_COLUMN)]

            result = {}
            result.update(item.to_dict())
            result.update({B_LINK_A_COLUMN: many_side_program_id_list})
            if item:
                return jsonify(result)
            else:
                return jsonify({'error': f'{MANY_SIDE_B_API_NAME} not found'}), 404

        else:
            # 查询所有记录
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            sort_by = request.args.get('sort_by', 'id')
            order = request.args.get('order', 'asc')
            search = request.args.get('search', '')

            query = MANY_SIDE_B_MODEL_NAME.query.filter_by(is_deleted=False)

            if search:
                query = query.filter(getattr(MANY_SIDE_B_MODEL_NAME, MANY_SIDE_B_SEARCH_BY).contains(search))

            if order == 'asc':
                query = query.order_by(asc(getattr(MANY_SIDE_B_MODEL_NAME, sort_by)))
            else:
                query = query.order_by(desc(getattr(MANY_SIDE_B_MODEL_NAME, sort_by)))

            items = query.paginate(page=page, per_page=per_page, count=True)

            total_page = items.total // items.per_page
            total_page += 1

            result = []
            # 需要将一方关联的多方按照其名称展示成列表
            for item in items:
                _d = {}
                many_side_C_display_list = [many_side_obj.to_dict()[B_LINK_C_DISPLAY_NAME] for many_side_obj in
                                            getattr(item, B_LINK_C_COLUMN)]
                _d.update(item.to_dict())
                _d.update({B_LINK_C_COLUMN: many_side_C_display_list})
                result.append(_d)

            return render_template(f'{MANY_SIDE_B_TEMPLATE_NAME}.html', form_info=MANY_SIDE_B_FORM_INFO,
                                   total=items.total,
                                   page=items.page,
                                   total_page=total_page,
                                   per_page=items.per_page,
                                   items=result,
                                   page_obj=items, many_side_C_info_display=many_side_C_info_display)
    elif request.method == 'POST':
        data = request.json
        if _ := data.keys() - set(MANY_SIDE_B_FORM_INFO_VALIDATE['column_list']):
            if not len(_) > 0:
                return jsonify({
                    'message': f'required {list(set(MANY_SIDE_B_FORM_INFO_VALIDATE["column_list"]) - data.keys())}, but not give!'}), 500
        new_data = {}

        for column in MANY_SIDE_B_FORM_INFO_VALIDATE['column_list']:
            if isinstance(data[column], MANY_SIDE_B_FORM_INFO_VALIDATE[column]['type']):
                new_data[column] = data[column]
            else:
                return jsonify({
                    'message': f'{column} should be type {MANY_SIDE_B_FORM_INFO_VALIDATE[column]["type"]},but got type {type(data[column])}'}), 500

                # 获取多有的多方对象
        new_data_copy = new_data.copy()
        new_data.pop(B_LINK_C_COLUMN)
        new_item = MANY_SIDE_B_MODEL_NAME(**new_data)

        for many_side_id in new_data_copy[B_LINK_C_COLUMN]:
            # 获取多方对象

            many_side_obj = MANY_SIDE_C_MODEL_NAME.query.get(many_side_id)
            print(many_side_obj)
            if many_side_obj:
                # 将多方对象中append进来
                getattr(new_item, B_LINK_C_COLUMN).append(many_side_obj)
        new_item.save()
        return jsonify({'message': f'{MANY_SIDE_B_API_NAME}'.replace('s', '') + 'created!'}), 201
    elif request.method == 'PUT':

        item = MANY_SIDE_B_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_B_MODEL_NAME} not found'}), 404
        data = request.json
        new_data = data.copy()
        new_data.pop(B_LINK_A_COLUMN)
        # print(data[ONE_LINK_MANY_COLUMN])  # ['1', '2', '3']
        # 对多方对象进行处理
        new_obj = set()
        for id in data[B_LINK_A_COLUMN]:
            _item = MANY_SIDE_A_MODEL_NAME.query.get(id)
            if _item:
                new_obj.add(_item)
        raw_obj = set(getattr(item, B_LINK_A_COLUMN))
        # 第一种方式：传递过来的对象id，比原来的对象增加
        if _add_obj := new_obj - raw_obj:
            for _item in _add_obj:
                getattr(item, B_LINK_A_COLUMN).append(_item)
        # 第二种方式：传递过来的对象id,比原来的对象减少
        elif _sub_obj := raw_obj - new_obj:
            for _item in _sub_obj:
                getattr(item, B_LINK_A_COLUMN).remove(_item)
        item.update_fields(**new_data)
        return jsonify({'message': f'{MANY_SIDE_A_API_NAME}'.replace('s', '') + 'updated!'})

    elif request.method == 'DELETE':
        item = MANY_SIDE_B_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_B_API_NAME}'.replace('s', '') + 'not found'}), 404
        item.soft_delete()
        return jsonify({'message': f'{MANY_SIDE_B_API_NAME}'.replace('s', '') + 'deleted!'})


@user_role_permisson_app.route(f'/api/{MANY_SIDE_C_API_NAME}/', defaults={'id': None}, methods=['GET', 'POST'])
@user_role_permisson_app.route(f'/api/{MANY_SIDE_C_API_NAME}/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required()
@check_permission()
def get_side_C_items(id):
    if request.method == 'GET':
        many_side_B_info = MANY_SIDE_B_MODEL_NAME.query.filter_by(is_deleted=False).all()
        _x, _y = B_TO_C_DISPLAY
        many_side_B_info_display = [[info.to_dict().get(_x), info.to_dict().get(_y)] for info in many_side_B_info]
        if id:
            # 查询单条记录
            item = MANY_SIDE_C_MODEL_NAME.query.filter_by(id=id, is_deleted=False).first()
            # 查询单条记录的所有的多对多字段
            many_side_program_id_list = [many_side_obj.to_dict()[C_LINK_B_PROGRAM_ID] for many_side_obj in
                                         getattr(item, C_LINK_B_COLUMN)]

            result = {}
            result.update(item.to_dict())
            result.update({C_LINK_B_COLUMN: many_side_program_id_list})
            if item:
                return jsonify(result)
            else:
                return jsonify({'error': f'{MANY_SIDE_C_API_NAME} not found'}), 404

        else:
            # 查询所有记录
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            sort_by = request.args.get('sort_by', 'id')
            order = request.args.get('order', 'asc')
            search = request.args.get('search', '')

            query = MANY_SIDE_C_MODEL_NAME.query.filter_by(is_deleted=False)

            if search:
                query = query.filter(getattr(MANY_SIDE_C_MODEL_NAME, MANY_SIDE_C_SEARCH_BY).contains(search))

            if order == 'asc':
                query = query.order_by(asc(getattr(MANY_SIDE_C_MODEL_NAME, sort_by)))
            else:
                query = query.order_by(desc(getattr(MANY_SIDE_C_MODEL_NAME, sort_by)))

            items = query.paginate(page=page, per_page=per_page, count=True)

            total_page = items.total // items.per_page
            total_page += 1

            result = []
            # 需要将一方关联的多方按照其名称展示成列表
            for item in items:
                _d = {}
                many_side_B_display_list = [many_side_obj.to_dict()[B_LINK_C_DISPLAY_NAME] for many_side_obj in
                                            getattr(item, C_LINK_B_COLUMN).all()]
                _d.update(item.to_dict())
                _d.update({C_LINK_B_COLUMN: many_side_B_display_list})
                result.append(_d)

            return render_template(f'{MANY_SIDE_C_TEMPLATE_NAME}.html', form_info=MANY_SIDE_C_FORM_INFO,
                                   total=items.total,
                                   page=items.page,
                                   total_page=total_page,
                                   per_page=items.per_page,
                                   items=result,
                                   page_obj=items, many_side_B_info_display=many_side_B_info_display)
    elif request.method == 'POST':
        data = request.json
        if _ := data.keys() - set(MANY_SIDE_C_FORM_INFO_VALIDATE['column_list']):
            if not len(_) > 0:
                return jsonify({
                    'message': f'required {list(set(MANY_SIDE_C_FORM_INFO_VALIDATE["column_list"]) - data.keys())}, but not give!'}), 500
        new_data = {}

        for column in MANY_SIDE_C_FORM_INFO_VALIDATE['column_list']:
            if isinstance(data[column], MANY_SIDE_C_FORM_INFO_VALIDATE[column]['type']):
                new_data[column] = data[column]
            else:
                return jsonify({
                    'message': f'{column} should be type {MANY_SIDE_C_FORM_INFO_VALIDATE[column]["type"]},but got type {type(data[column])}'}), 500

                # 获取多有的多方对象
        new_data_copy = new_data.copy()
        new_data.pop(C_LINK_B_COLUMN)
        new_item = MANY_SIDE_C_MODEL_NAME(**new_data)

        for many_side_id in new_data_copy[C_LINK_B_COLUMN]:
            # 获取多方对象

            many_side_obj = MANY_SIDE_B_MODEL_NAME.query.get(many_side_id)
            print(many_side_obj)
            if many_side_obj:
                # 将多方对象中append进来
                getattr(new_item, C_LINK_B_COLUMN).append(many_side_obj)
        new_item.save()
        return jsonify({'message': f'{MANY_SIDE_C_API_NAME}'.replace('s', '') + 'created!'}), 201
    elif request.method == 'PUT':

        item = MANY_SIDE_C_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_C_MODEL_NAME} not found'}), 404
        data = request.json
        new_data = data.copy()
        new_data.pop(B_LINK_C_COLUMN)
        # print(data[ONE_LINK_MANY_COLUMN])  # ['1', '2', '3']
        # 对多方对象进行处理
        new_obj = set()
        for id in data[B_LINK_C_COLUMN]:
            _item = MANY_SIDE_B_MODEL_NAME.query.get(id)
            if _item:
                new_obj.add(_item)
        raw_obj = set(getattr(item, B_LINK_C_COLUMN))
        # 第一种方式：传递过来的对象id，比原来的对象增加
        if _add_obj := new_obj - raw_obj:
            for _item in _add_obj:
                getattr(item, B_LINK_C_COLUMN).append(_item)
        # 第二种方式：传递过来的对象id,比原来的对象减少
        elif _sub_obj := raw_obj - new_obj:
            for _item in _sub_obj:
                getattr(item, B_LINK_C_COLUMN).remove(_item)
        item.update_fields(**new_data)
        return jsonify({'message': f'{MANY_SIDE_C_API_NAME}'.replace('s', '') + 'updated!'})

    elif request.method == 'DELETE':
        item = MANY_SIDE_C_MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MANY_SIDE_C_API_NAME}'.replace('s', '') + 'not found'}), 404
        item.soft_delete()
        return jsonify({'message': f'{MANY_SIDE_C_API_NAME}'.replace('s', '') + 'deleted!'})
