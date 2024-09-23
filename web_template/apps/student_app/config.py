from .models import Student

# 在API中如何表示
API_NAME = 'students'
# 对应的Model
MODEL_NAME = Student
# 基于哪个字段筛选
SEARCH_BY = 'name'
# 模板的名字
TEMPLATE_NAME = 'index'
# 字段列表
COLUMN_LIST = ['id', 'name', 'grade']
# 表单的配置
FORM_INFO_TASK = {
    "name": "STUDENT",
    "api_name": "student/api/student",
    "columns": {
        'name': {
            "list_title": "Name",
            "id": "name",
            "type": "text"
        },
        'grade': {
            "list_title": "Grade",
            "id": "grade",
            "type": "text"
        }
    }
}
# 表单返回后端的校验
FORM_INFO_VALIDATE = {
    "column_list" : ['name', 'grade'],
    "name" : {
        'type': str,
        'length': 128
    },
    "grade" : {
        'type': str,
        'length': 8
    }
}

