from web_template.extensions import BaseModel, db

A_B_s = db.Table('a_bs',
    db.Column('a_id', db.Integer, db.ForeignKey('as.id'), primary_key=True),
    db.Column('b_id', db.Integer, db.ForeignKey('bs.id'), primary_key=True)
)


class A(BaseModel):

    __tablename__ = 'as'

    name = db.Column(db.String(80), nullable=False)

    # 多对多关系：通过 user_roles 表关联
    bs = db.relationship('B', secondary=A_B_s, backref=db.backref('as', lazy='dynamic'))

"""
roles 是 User 中的关系字段，它与 Role 模型关联，secondary=user_roles 表示多对多关系是通过 user_roles 表实现的。
backref='users' 在 Role 模型中自动生成了一个反向引用字段 users，使得我们可以通过一个 Role 实例来访问与其相关的 User 实例。
lazy='dynamic' 表示关系的查询是延迟加载的，这在处理大数据集时有助于提高性能。

使用 db.Table() 创建关联表，用于存储多对多关系。
使用 relationship() 和 secondary 参数来定义多对多关系。
backref 参数允许反向引用关系，便于从另一方访问关联的对象。
"""

class B(BaseModel):

    __tablename__ = 'bs'

    name = db.Column(db.String(80), unique=True, nullable=False)

