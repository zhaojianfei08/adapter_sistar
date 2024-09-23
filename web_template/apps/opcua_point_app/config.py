from .models import OPCUADevice, OPCUAPoint

"""
ONE_SIDE is 一方

MANY_SIDE is 多方 
"""

# 一方的api名称, 一般是模型名小写后，加一个复数s
ONE_SIDE_API_NAME = 'opcuadevices'
# 多方的api名称
MANY_SIDE_API_NAME = 'opcuapoints'
# "一"方对应的Model, 一方对应的模型
ONE_SIDE_MODEL_NAME = OPCUADevice
# “多”方对应的Model，多方对应的模型
MANY_SIDE_MODEL_NAME = OPCUAPoint
# 基于哪个字段筛选
ONE_SIDE_SEARCH_BY = 'device_name'
MANY_SIDE_SEARCH_BY = 'comments'
# 模板的名字
ONE_SIDE_TEMPLATE_NAME = 'opcua_device_index'
MANY_SIDE_TEMPLATE_NAME = 'opcua_point_index'

# 表单的配置
ONE_SIDE_FORM_INFO = {
    "name": "OPCUADevice",  # 模型名
    "api_name": "opcua/api/opcuadevice",  # 对应的API 增加  修改  删除要用，需要考虑 蓝图前缀,还有ONE_SIDE_API_NAME后面的s去掉
    "columns": {  # 需要渲染的列
        'device_name': {  # name列
            "list_title": "Device Name",  # 在列表展示的名称
            "id": "device_name",  # 添加的id， 修改的id
            "type": "text"  # 字段的类型
        },
        'url': {  # name列
            "list_title": "URL",  # 在列表展示的名称
            "id": "url",  # 添加的id， 修改的id
            "type": "text"  # 字段的类型
        },
        'opcuapoints': {  # books列
            "list_title": "OPCUA Points",
            "id": "opcuapoints",
            "type": "form-select"  # 下列选择框
        }
    }
}

MANY_SIDE_FORM_INFO = {  #
    "name": "OPCUAPoint",  # 模型类
    "api_name": "opcua/api/opcuapoint",
    "columns": {
        'tag_uuid': {
            "list_title": "tag_uuid",
            "id": "tag_uuid",
            "type": "text",
        },
        'node_id': {
            "list_title": "node_id",
            "id": "node_id",
            "type": "text",
        },
        'interval': {
            "list_title": "interval",
            "id": "interval",
            "type": "text",
        },
        'active': {
            "list_title": "active",
            "id": "active",
            "type": "text",
        }, 'active_alarm': {
            "list_title": "active_alarm",
            "id": "active_alarm",
            "type": "text",
        }, 'alarm_up': {
            "list_title": "alarm_up",
            "id": "alarm_up",
            "type": "text",
        }, 'alarm_down': {
            "list_title": "alarm_down",
            "id": "alarm_down",
            "type": "text",
        }, 'alarm_up_info': {
            "list_title": "alarm_up_info",
            "id": "alarm_up_info",
            "type": "text",
        }, 'alarm_down_info': {
            "list_title": "alarm_down_info",
            "id": "alarm_down_info",
            "type": "text",
        }, 'alarm_up_change': {
            "list_title": "alarm_up_change",
            "id": "alarm_up_change",
            "type": "text",
        }, 'alarm_down_change': {
            "list_title": "alarm_down_change",
            "id": "alarm_down_change",
            "type": "text",
        }, 'active_archive': {
            "list_title": "active_archive",
            "id": "active_archive",
            "type": "text",
        }, 'archive_onchange': {
            "list_title": "archive_onchange",
            "id": "archive_onchange",
            "type": "text",
        }, 'archive_interval': {
            "list_title": "archive_interval",
            "id": "archive_interval",
            "type": "text",
        }, 'active_scale': {
            "list_title": "active_scale",
            "id": "active_scale",
            "type": "text",
        }, 'scale_sign': {
            "list_title": "scale_sign",
            "id": "scale_sign",
            "type": "text",
        }, 'scale_factor': {
            "list_title": "scale_factor",
            "id": "scale_factor",
            "type": "text",
        }, 'mqtt_topic_name': {
            "list_title": "mqtt_topic_name",
            "id": "mqtt_topic_name",
            "type": "text",
        }, 'unit': {
            "list_title": "unit",
            "id": "unit",
            "type": "text",
        }, 'comments': {
            "list_title": "comments",
            "id": "comments",
            "type": "text",
        },
        'device_id': {  # 下拉选择框
            "list_title": "Device ID",
            "id": "device_id",
            "type": "form-select",
            'list_id': "device"  # 如果是外键通过这个数值表示外键关联关系，而不是使用外键的id
        }
    }
}
# 表单返回后端的校验
ONE_SIDE_FORM_INFO_VALIDATE = {
    "column_list": ['device_name', 'url', 'opcuapoints'],  # 校验，模型类必传项目中，必须列入到column_list中
    "device_name": {  # 只要在上面的list中，必须增加校验的条件
        'type': str,  # 类型校验
        'length': 128  # 长度角度
        # 可以扩展其他校验
    },
    "url": {  # 只要在上面的list中，必须增加校验的条件
        'type': str,  # 类型校验
        'length': 128  # 长度角度
        # 可以扩展其他校验
    },
    "opcuapoints": {
        'type': list,
        'length': 256
    }
}

MANY_SIDE_FORM_INFO_VALIDATE = {
    "column_list": ['tag_uuid', 'node_id', 'interval',
                    'active', 'active_alarm', 'alarm_up',
                    'alarm_down',
                    'alarm_up_info',
                    'alarm_down_info',
                    'alarm_up_change',
                    'alarm_down_change',
                    'active_archive',
                    'archive_onchange',
                    'archive_interval',
                    'active_scale',
                    'scale_sign',
                    'scale_factor',
                    'mqtt_topic_name',
                    'unit',
                    'comments','device_id'],
    "tag_uuid": {
        'type': str,
        'length': 128
    },
    "node_id": {
        'type': str,
        'length': 128
    },
    "interval": {
        'type': str,
        'length': 128
    },
    "active": {
        'type': str,
        'length': 128
    },
    "active_alarm": {
        'type': str,
        'length': 128
    },
    "alarm_up": {
        'type': str,
        'length': 128
    },
    "alarm_down": {
        'type': str,
        'length': 128
    },
    "alarm_up_info": {
        'type': str,
        'length': 128
    },
    "alarm_down_info": {
        'type': str,
        'length': 128
    },
    "active_archive": {
        'type': str,
        'length': 128
    },
    "archive_onchange": {
        'type': str,
        'length': 128
    },
    "archive_interval": {
        'type': str,
        'length': 128
    },
    "active_scale": {
        'type': str,
        'length': 128
    },
    "scale_sign": {
        'type': str,
        'length': 128
    },
    "scale_factor": {
        'type': str,
        'length': 128
    },
    "mqtt_topic_name": {
        'type': str,
        'length': 128
    },
    "unit": {
        'type': str,
        'length': 128
    },
    "comments": {
        'type': str,
        'length': 128
    },
    "device_id": {
        'type': str
    }
}

# 一方中显示多方的所有数据组合
ONE_TO_MANY_DISPLAY = ['id', 'comments']  # 添加一方的时候，需要通过下拉列表显示需要关联的多方对象，这时候下拉列表的value为id。内容为title
# 比如，创建作者时候，要给作者同时绑定书籍

# 多方中显示一方的所有数据组合
MANY_TO_ONE_DISPLAY = ['id', 'device_name']  # 添加多方对象时候，给多方对象一个唯一的外键ID

# 一方中可以关联到多方的关联字段
# Author : one   Book： Many
# Author 对象，关系到books的字段： books

ONE_LINK_MANY_COLUMN = 'opcuapoints'  # 一方对象通过这个字段关联多方对象
MANY_SIDE_DISPLAY_NAME = 'comments'  # ['十万个为什么', '卖火柴的小女孩']  多方对象展示在一方中展示的字段，该字段必须在多方对象的属性空间内
MANY_SIDE_PROGRAM_ID = 'id'  # 多方对象在一方对象中被修改或者创建，使用id

# 多方对象列表，显示一方对象的字段
ONE_SIDE_DISPLAY_NAME = 'opcuadevice'  # 多方对象关联到一方的反向字段，  比如一本书，要知道他的作者，Book.author
ONE_SIDE_DISPLAY_NAME_IN_LIST = 'device_name'  # Book.author.name  所以这个必须是在一方对象的地址空间内
