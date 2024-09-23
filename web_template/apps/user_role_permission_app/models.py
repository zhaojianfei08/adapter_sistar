from werkzeug.security import generate_password_hash, check_password_hash

from web_template.extensions import BaseModel, db

user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                      db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
                      extend_existing=True  # 解决重复定义问题
                      )

role_permissions = db.Table('role_permissions',
                            db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True),
                            extend_existing=True  # 解决重复定义问题
                            )


class User(BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String(80), nullable=False)
    # 多对多关系：通过 user_roles 表关联
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(200))  # 存储加密的密码

    # 设置密码时，自动将其加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码是否正确
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))


    def __repr__(self):
        return f'<User {self.name}>'


"""
roles 是 User 中的关系字段，它与 Role 模型关联，secondary=user_roles 表示多对多关系是通过 user_roles 表实现的。
backref='users' 在 Role 模型中自动生成了一个反向引用字段 users，使得我们可以通过一个 Role 实例来访问与其相关的 User 实例。
lazy='dynamic' 表示关系的查询是延迟加载的，这在处理大数据集时有助于提高性能。

使用 db.Table() 创建关联表，用于存储多对多关系。
使用 relationship() 和 secondary 参数来定义多对多关系。
backref 参数允许反向引用关系，便于从另一方访问关联的对象。
"""


class Role(BaseModel):
    __tablename__ = 'roles'

    name = db.Column(db.String(80), unique=True, nullable=False)

    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(BaseModel):
    __tablename__ = 'permissions'

    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Permission {self.name}>'
