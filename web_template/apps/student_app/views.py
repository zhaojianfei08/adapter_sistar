from flask import render_template, request, jsonify
from sqlalchemy import asc, desc

from . import student_app
from .config import API_NAME, MODEL_NAME, SEARCH_BY, FORM_INFO_TASK, TEMPLATE_NAME, FORM_INFO_VALIDATE


@student_app.route(f'/api/{API_NAME}/', defaults={'id': None}, methods=['GET', 'POST'])
@student_app.route(f'/api/{API_NAME}/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_items(id):
    if request.method == 'GET':
        if id:
            # 查询单条记录
            item = MODEL_NAME.query.filter_by(id=id, is_deleted=False).first()
            if item:
                return jsonify(item.to_dict())
            else:
                return jsonify({'error': f'{API_NAME} not found'}), 404
        else:
            # 查询所有记录
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            sort_by = request.args.get('sort_by', 'id')
            order = request.args.get('order', 'asc')
            search = request.args.get('search', '')

            query = MODEL_NAME.query.filter_by(is_deleted=False)

            if search:
                query = query.filter(getattr(MODEL_NAME, SEARCH_BY).contains(search))

            if order == 'asc':
                query = query.order_by(asc(getattr(MODEL_NAME, sort_by)))
            else:
                query = query.order_by(desc(getattr(MODEL_NAME, sort_by)))

            items = query.paginate(page=page, per_page=per_page, count=True)

            total_page = items.total // items.per_page
            total_page += 1

            return render_template(f'{TEMPLATE_NAME}.html', form_info=FORM_INFO_TASK, total=items.total,
                                   page=items.page,
                                   total_page=total_page,
                                   per_page=items.per_page,
                                   items=[item.to_dict() for item in items.items],
                                   page_obj=items)
    elif request.method == 'POST':
        data = request.json
        if _ := data.keys() - set(FORM_INFO_VALIDATE['column_list']):
            if not len(_) > 0:
                return jsonify({
                    'message': f'required {list(set(FORM_INFO_VALIDATE["column_list"]) - data.keys())}, but not give!'}), 500
        new_data = {}
        for column in FORM_INFO_VALIDATE['column_list']:
            if isinstance(data[column], FORM_INFO_VALIDATE[column]['type']):
                new_data[column] = data[column]
            else:
                return jsonify({
                    'message': f'{column} should be type {FORM_INFO_VALIDATE[column]["type"]},but got type {type(data[column])}'}), 500
        new_item = MODEL_NAME(**new_data)
        new_item.save()
        return jsonify({'message': f'{API_NAME}'.replace('s', '') + 'created!'}), 201
    elif request.method == 'PUT':
        item = MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{MODEL_NAME} not found'}), 404
        data = request.json

        item.update_fields(**data)
        return jsonify({'message': 'User updated!'})
    elif request.method == 'DELETE':
        item = MODEL_NAME.query.get(id)
        if not item:
            return jsonify({'message': f'{API_NAME}'.replace('s', '') + 'not found'}), 404
        item.soft_delete()
        return jsonify({'message': f'{API_NAME}'.replace('s', '') + 'deleted!'})
