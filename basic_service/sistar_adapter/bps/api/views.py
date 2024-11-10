from flask import request

from helpers import success_response, error_response
from . import api_bp
from marshmallow import Schema, fields
from .adapter import create_batch, sistar_batch_params_instance, create_batch_ex, delete_batch, get_last_error, \
    get_last_full_error_string, set_batch_parameters, set_batch_size, set_batch_start_data, set_batch_status, \
    set_timeout, add_parameter, get_number_at, get_size, get_value_at


# 定义输入参数模式


class HelloSchema(Schema):
    name = fields.String(required=True, description='Name of the person')  #
    # 判断输入的元素是数组中的某一个 validate=validate.OneOf(['active', 'inactive', 'pending'])
    #  status = fields.String(required=True, validate=validate.OneOf(['active', 'inactive', 'pending']))


# class CreateBatchSchema(Schema):
#     site = fields.Int(required=True, description='The number of the site.')
#     area = fields.Int(required=True, description='The number of the area.')
#     year = fields.Int(required=True, description='The 2-digit year of the batch, 0..99.')
#     order = fields.Int(required=True, description='The number of the order, 1..65535.')
#     batch = fields.Int(required=True, description='The number of the batch, 1..65535.')
#     recipeCategory = fields.Int(required=True, description='The number of the recipe category.')
#     recipe = fields.Int(required=True, description='The number of the batch, 1..65535.')
#     line = fields.Int(required=True, description='The number of the batch, 1..65535.')
#     productId = fields.Int(required=True, description='The number of the batch, 1..65535.')
#     size = fields.Float(required=True, description='The number of the batch, 1..65535.')
#     useDefaultSize = fields.Boolean(required=True, description='The number of the batch, 1..65535.')
#     startMode = fields.String(required=True, description='The number of the batch, 1..65535.')
#     plannedStartTimeYear = fields.Int(required=True, description='The number of the batch, 1..65535.')
#     plannedStartTimeMonth = fields.Int(required=True, description='The number of the batch, 1..65535.')
#     plannedStartTimeDay = fields.Int(required=True, description='The number of the batch, 1..65535.')
#     status = fields.String(required=True, description='The number of the batch, 1..65535.')
#     parameterList = fields.Raw(required=True)
#     useDefaultParameterValues = fields.Boolean(required=True, description='The number of the batch, 1..65535.')
#     errorMessage = fields.String(required=True, description='The number of the batch, 1..65535.')
#     doRepeat = fields.Boolean(required=True, description='The number of the batch, 1..65535.')


@api_bp.route('/create_batch', methods=['POST'])
def create_batch_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = create_batch(res.get('site'),
                              res.get('area'),
                              res.get('year'),
                              res.get('order'),
                              res.get('batch'),
                              res.get('recipeCategory'),
                              res.get('recipe'),
                              res.get('line'),
                              res.get('productId'),
                              res.get('size'),
                              res.get('useDefaultSize'),
                              res.get('startMode'),
                              res.get('plannedStartTimeYear'),
                              res.get('plannedStartTimeMonth'),
                              res.get('plannedStartTimeDay'),
                              res.get('plannedStartTimeHour'),
                              res.get('plannedStartTimeMin'),
                              res.get('plannedStartTimeSec'),
                              'Locked',
                              parameterList,
                              res.get('useDefaultParameterValues'),
                              res.get('errorMessage'),
                              res.get('doRepeat'))

        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/create_batch_ex', methods=['POST'])
def create_batch_ex_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """

    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = create_batch_ex(res.get('site'),
                                 res.get('area'),
                                 res.get('year'),
                                 res.get('order'),
                                 res.get('batch'),
                                 res.get('recipeCategory'),
                                 res.get('recipe'),
                                 res.get('line'),
                                 res.get('productId'),
                                 res.get('useDefaultProductId'),
                                 res.get('size'),
                                 res.get('useDefaultSize'),
                                 res.get('startMode'),
                                 res.get('plannedStartTimeYear'),
                                 res.get('plannedStartTimeMonth'),
                                 res.get('plannedStartTimeDay'),
                                 res.get('plannedStartTimeHour'),
                                 res.get('plannedStartTimeMin'),
                                 res.get('plannedStartTimeSec'),
                                 'Locked',
                                 parameterList,
                                 res.get('useDefaultParameterValues'),
                                 res.get('batcName'),
                                 res.get('errorMessage'),
                                 res.get('doRepeat'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/delete_batch', methods=['POST'])
def delete_batch_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """

    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = delete_batch(res.get('site'),
                              res.get('area'),
                              res.get('year'),
                              res.get('order'),
                              res.get('batch'),
                              res.get('recipeCategory'),
                              res.get('errorMessage'),
                              res.get('doRepeat'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/get_last_error', methods=['POST'])
def get_last_error_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    try:
        # 设置超时时间为 5 秒
        result = get_last_error()
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/get_last_full_error_string', methods=['POST'])
def get_last_full_error_string_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    try:
        # 设置超时时间为 5 秒
        result = get_last_full_error_string()
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/set_batch_parameters', methods=['POST'])
def set_batch_parameters_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = set_batch_parameters(res.get('site'),
                                      res.get('area'),
                                      res.get('year'),
                                      res.get('order'),
                                      res.get('batch'),
                                      res.get('recipeCategory'),
                                      parameterList,
                                      res.get('errorMessage'),
                                      res.get('doRepeat'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/set_batch_size', methods=['POST'])
def set_batch_size_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = set_batch_size(res.get('site'),
                                res.get('area'),
                                res.get('year'),
                                res.get('order'),
                                res.get('batch'),
                                res.get('recipeCategory'),
                                res.get('size'),
                                res.get('errorMessage'),
                                res.get('doRepeat'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/set_batch_start_data', methods=['POST'])
def set_batch_start_data_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = set_batch_start_data(res.get('site'),
                                      res.get('area'),
                                      res.get('year'),
                                      res.get('order'),
                                      res.get('batch'),
                                      res.get('recipeCategory'),
                                      res.get('startMode'),
                                      res.get('plannedStartTimeYear'),
                                      res.get('plannedStartTimeMonth'),
                                      res.get('plannedStartTimeDay'),
                                      res.get('plannedStartTimeHour'),
                                      res.get('plannedStartTimeMin'),
                                      res.get('plannedStartTimeSec'),
                                      res.get('errorMessage'),
                                      res.get('doRepeat'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/set_batch_status', methods=['POST'])
def set_batch_status_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = set_batch_status(res.get('site'),
                                  res.get('area'),
                                  res.get('year'),
                                  res.get('order'),
                                  res.get('batch'),
                                  res.get('recipeCategory'),
                                  res.get('status'),
                                  res.get('errorMessage'),
                                  res.get('doRepeat'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/set_timeout', methods=['POST'])
def set_timeout_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = set_timeout(res.get('timeout'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/add_parameter', methods=['POST'])
def add_parameter_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = add_parameter(res.get('paramNumber'),res.get('paramValue')
                               )
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/get_number_at', methods=['POST'])
def get_number_at_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = get_number_at(res.get('index'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/get_size', methods=['POST'])
def get_size_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = get_size()
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_bp.route('/get_value_at', methods=['POST'])
def get_value_at_func():
    """
    site, area, year, order, batch, recipeCategory, recipe, line, productId, size, useDefaultSize,
                      startMode, plannedStartTimeYear, plannedStartTimeMonth, plannedStartTimeDay, status,
                      parameterList, useDefaultParameterValues, errorMessage,
                      doRepeat
    :return:
    """
    res = request.json
    parameterList = sistar_batch_params_instance
    try:
        # 设置超时时间为 5 秒
        result = get_value_at(res.get('index'))
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))