from .models import Author, Book

"""
ONE_SIDE is 一方

MANY_SIDE is 多方 
"""

# 一方的api名称, 一般是模型名小写后，加一个复数s
ONE_SIDE_API_NAME = 'authors'
# 多方的api名称
MANY_SIDE_API_NAME = 'books'
# "一"方对应的Model, 一方对应的模型
ONE_SIDE_MODEL_NAME = Author
# “多”方对应的Model，多方对应的模型
MANY_SIDE_MODEL_NAME = Book
# 基于哪个字段筛选
ONE_SIDE_SEARCH_BY = 'name'
MANY_SIDE_SEARCH_BY = 'title'
# 模板的名字
ONE_SIDE_TEMPLATE_NAME = 'one_side_index'
MANY_SIDE_TEMPLATE_NAME = 'many_side_index'

# 表单的配置
ONE_SIDE_FORM_INFO = {
    "name": "Author",  # 模型名
    "api_name": "ab/api/author",  # 对应的API 增加  修改  删除要用，需要考虑 蓝图前缀,还有ONE_SIDE_API_NAME后面的s去掉
    "columns": {  # 需要渲染的列
        'name': {  # name列
            "list_title": "Name",  # 在列表展示的名称
            "id": "name",  # 添加的id， 修改的id
            "type": "text"  # 字段的类型
        },
        'books': {  # books列
            "list_title": "Books",
            "id": "books",
            "type": "form-select"  # 下列选择框
        }
    }
}

MANY_SIDE_FORM_INFO = {  #
    "name": "Book",  # 模型类
    "api_name": "ab/api/book",
    "columns": {
        'title': {
            "list_title": "Title",
            "id": "title",
            "type": "text",
        },
        'author_id': {  # 下拉选择框
            "list_title": "Author",
            "id": "author_id",
            "type": "form-select",
            'list_id': "author"  # 如果是外键通过这个数值表示外键关联关系，而不是使用外键的id
        }
    }
}
# 表单返回后端的校验
ONE_SIDE_FORM_INFO_VALIDATE = {
    "column_list": ['name', 'books'],  # 校验，模型类必传项目中，必须列入到column_list中
    "name": {  # 只要在上面的list中，必须增加校验的条件
        'type': str,  # 类型校验
        'length': 128  # 长度角度
        # 可以扩展其他校验
    },
    "books": {
        'type': list,
        'length': 256
    }
}

MANY_SIDE_FORM_INFO_VALIDATE = {
    "column_list": ['title', 'author_id'],
    "title": {
        'type': str,
        'length': 128
    },
    "author_id": {
        'type': str
    }
}

# 一方中显示多方的所有数据组合
ONE_TO_MANY_DISPLAY = ['id', 'title']  # 添加一方的时候，需要通过下拉列表显示需要关联的多方对象，这时候下拉列表的value为id。内容为title
# 比如，创建作者时候，要给作者同时绑定书籍

# 多方中显示一方的所有数据组合
MANY_TO_ONE_DISPLAY = ['id', 'name']  # 添加多方对象时候，给多方对象一个唯一的外键ID

# 一方中可以关联到多方的关联字段
# Author : one   Book： Many
# Author 对象，关系到books的字段： books

ONE_LINK_MANY_COLUMN = 'books'  # 一方对象通过这个字段关联多方对象
MANY_SIDE_DISPLAY_NAME = 'title'  # ['十万个为什么', '卖火柴的小女孩']  多方对象展示在一方中展示的字段，该字段必须在多方对象的属性空间内
MANY_SIDE_PROGRAM_ID = 'id'  # 多方对象在一方对象中被修改或者创建，使用id

# 多方对象列表，显示一方对象的字段
ONE_SIDE_DISPLAY_NAME = 'author'  # 多方对象关联到一方的反向字段，  比如一本书，要知道他的作者，Book.author
ONE_SIDE_DISPLAY_NAME_IN_LIST = 'name'  # Book.author.name  所以这个必须是在一方对象的地址空间内
