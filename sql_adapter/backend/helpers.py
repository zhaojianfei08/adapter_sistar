from flask import jsonify


def success_response(data=None, message="success", code=200):
    """
    成功返回的格式
    :param data: 返回的实际数据
    :param message: 提示信息
    :param code: 自定义状态码，默认为 200
    """
    return {
        "status": "success",
        "code": code,
        "message": message,
        "data": data
    }


def error_response(message="error", code=400, data=None):
    """
    错误返回的格式
    :param message: 错误信息
    :param code: HTTP 状态码，默认为 400
    :param data: 附加数据（可选）
    """
    return {
        "status": "error",
        "code": code,
        "message": message,
        "data": data
    }

