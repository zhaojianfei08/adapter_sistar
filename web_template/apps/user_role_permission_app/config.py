from .models import User, Role, Permission

# 一方的api名称, 一般是模型名小写后，加一个复数s
MANY_SIDE_A_API_NAME = 'users'
# 多方的api名称
MANY_SIDE_B_API_NAME = 'roles'
MANY_SIDE_C_API_NAME = 'permissions'

# "一"方对应的Model, 一方对应的模型
MANY_SIDE_A_MODEL_NAME = User
# “多”方对应的Model，多方对应的模型
MANY_SIDE_B_MODEL_NAME = Role
MANY_SIDE_C_MODEL_NAME = Permission
# 基于哪个字段筛选
MANY_SIDE_A_SEARCH_BY = 'name'
MANY_SIDE_B_SEARCH_BY = 'name'
MANY_SIDE_C_SEARCH_BY = 'name'
# 模板的名字
MANY_SIDE_A_TEMPLATE_NAME = 'user_index'
MANY_SIDE_B_TEMPLATE_NAME = 'role_index'
MANY_SIDE_C_TEMPLATE_NAME = 'permission_index'

# 表单的配置
MANY_SIDE_A_FORM_INFO = {
    "name": "User",  # 模型名
    "api_name": "rbac/api/user",  # 对应的API 增加  修改  删除要用，需要考虑 蓝图前缀,还有ONE_SIDE_API_NAME后面的s去掉
    "columns": {  # 需要渲染的列
        'name': {  # name列
            "list_title": "Name",  # 在列表展示的名称
            "id": "name",  # 添加的id， 修改的id
            "type": "text"  # 字段的类型
        },
        'email': {  # name列
            "list_title": "Email",  # 在列表展示的名称
            "id": "email",  # 添加的id， 修改的id
            "type": "text"  # 字段的类型
        },
        'password_hash': {  # books列
            "list_title": "Password Hash",
            "id": "password_hash",
            "type": "text"  # 下列选择框
        },
        'roles': {  # 下拉选择框
            "list_title": "Roles",
            "id": "roles",
            "type": "form-select",
            # 'list_id': "author"  # 如果是外键通过这个数值表示外键关联关系，而不是使用外键的id
        }
    }
}

MANY_SIDE_B_FORM_INFO = {  #
    "name": "Role",  # 模型类
    "api_name": "rbac/api/role",
    "columns": {
        'name': {
            "list_title": "Name",
            "id": "name",
            "type": "text",
        },
        'permissions': {  # 下拉选择框
            "list_title": "Permissions",
            "id": "permissions",
            "type": "form-select",
            # 'list_id': "author"  # 如果是外键通过这个数值表示外键关联关系，而不是使用外键的id
        }
    }
}

MANY_SIDE_C_FORM_INFO = {  #
    "name": "Permission",  # 模型类
    "api_name": "rbac/api/permission",
    "columns": {
        'name': {
            "list_title": "Name",
            "id": "name",
            "type": "text",
        },
        'roles': {  # 下拉选择框
            "list_title": "Roles",
            "id": "roles",
            "type": "form-select",
            # 'list_id': "author"  # 如果是外键通过这个数值表示外键关联关系，而不是使用外键的id
        }
    }
}

# 表单返回后端的校验
MANY_SIDE_A_FORM_INFO_VALIDATE = {
    "column_list": ['name', 'email', 'password_hash', 'roles'],  # 校验，模型类必传项目中，必须列入到column_list中
    "name": {  # 只要在上面的list中，必须增加校验的条件
        'type': str,  # 类型校验
        'length': 128  # 长度角度
        # 可以扩展其他校验
    },
    "email": {  # 只要在上面的list中，必须增加校验的条件
        'type': str,  # 类型校验
        'length': 128  # 长度角度
        # 可以扩展其他校验
    },
    "password_hash": {  # 只要在上面的list中，必须增加校验的条件
        'type': str,  # 类型校验
        'length': 128  # 长度角度
        # 可以扩展其他校验
    },
    "roles": {
        'type': list,
        'length': 256
    }
}

MANY_SIDE_B_FORM_INFO_VALIDATE = {
    "column_list": ['name', 'permissions'],
    "name": {
        'type': str,
        'length': 128
    },
    "permissions": {
        'type': list,
        'length': 256
    }
}

MANY_SIDE_C_FORM_INFO_VALIDATE = {
    "column_list": ['name', 'roles'],
    "name": {
        'type': str,
        'length': 128
    },
    "roles": {
        'type': list,
        'length': 256
    }
}

"""
A : User 
B : Role
C ：Permission 
"""
# 一方中显示多方的所有数据组合
A_TO_B_DISPLAY = ['id', 'name']  # 添加一方的时候，需要通过下拉列表显示需要关联的多方对象，这时候下拉列表的value为id。内容为title
# 比如，创建作者时候，要给作者同时绑定书籍
B_TO_C_DISPLAY = ['id', 'name']
# 多方中显示一方的所有数据组合
B_TO_A_DISPLAY = ['id', 'name']  # 添加多方对象时候，给多方对象一个唯一的外键ID

C_TO_B_DISPLAY = ['id', 'name']
# 一方中可以关联到多方的关联字段
# Author : one   Book： Many
# Author 对象，关系到books的字段： books

A_LINK_B_COLUMN = 'roles'  # 一方对象通过这个字段关联多方对象
A_LINK_B_DISPLAY_NAME = 'name'  # ['十万个为什么', '卖火柴的小女孩']  多方对象展示在一方中展示的字段，该字段必须在多方对象的属性空间内
A_LINK_B_PROGRAM_ID = 'id'  # 多方对象在一方对象中被修改或者创建，使用id

B_LINK_A_COLUMN = 'users'  # 一方对象通过这个字段关联多方对象
B_LINK_A_DISPLAY_NAME = 'name'  # ['十万个为什么', '卖火柴的小女孩']  多方对象展示在一方中展示的字段，该字段必须在多方对象的属性空间内
B_LINK_A_PROGRAM_ID = 'id'  # 多方对象在一方对象中被修改或者创建，使用id

B_LINK_C_COLUMN = 'permissions'  # 一方对象通过这个字段关联多方对象
B_LINK_C_DISPLAY_NAME = 'name'  # ['十万个为什么', '卖火柴的小女孩']  多方对象展示在一方中展示的字段，该字段必须在多方对象的属性空间内
B_LINK_C_PROGRAM_ID = 'id'  # 多方对象在一方对象中被修改或者创建，使用id

C_LINK_B_COLUMN = 'roles'
C_LINK_B_DISPLAY_NAME = 'name'
C_LINK_B_PROGRAM_ID = 'id'
# 多方对象列表，显示一方对象的字段
# ONE_SIDE_DISPLAY_NAME = 'author'  # 多方对象关联到一方的反向字段，  比如一本书，要知道他的作者，Book.author
# ONE_SIDE_DISPLAY_NAME_IN_LIST = 'name'  # Book.author.name  所以这个必须是在一方对象的地址空间内
