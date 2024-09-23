from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from flask_restful import Resource, Api
from flask_session import Session

db = SQLAlchemy()
api = Api()
session = Session()


class BaseModel(db.Model):
    __abstract__ = True  # 声明为抽象类，这样不会在数据库中创建表

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        """保存对象到数据库"""
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """从数据库中删除对象"""
        db.session.delete(self)
        db.session.commit()

    def update_fields(self, **kwargs):
        """根据传入的字段更新对象"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def soft_delete(self):
        """标记对象为已删除，但不从数据库中物理删除"""
        self.is_deleted = True
        db.session.commit()

    @classmethod
    def get_all(cls):
        """获取所有未被软删除的对象"""
        return cls.query.filter_by(is_deleted=False).all()

    @classmethod
    def get_by_id(cls, id):
        """根据ID获取对象"""
        return cls.query.filter_by(id=id, is_deleted=False).first()

    @classmethod
    def filter(cls, **kwargs):
        """根据过滤条件获取对象"""
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def paginate(cls, page=1, per_page=10, filters=None, sort_by=None, order='asc'):
        """获取分页对象，支持过滤和排序"""
        query = cls.query

        if filters:
            query = query.filter_by(**filters)

        if sort_by:
            order_by_clause = asc(sort_by) if order == 'asc' else desc(sort_by)
            query = query.order_by(order_by_clause)

        return query.paginate(page, per_page, False)

    def to_dict(self):
        new_dict = {}
        for column in self.__table__.columns:
            if isinstance(getattr(self, column.name), datetime):
                value = getattr(self, column.name).strftime('%Y-%m-%d %H:%M:%S')
                new_dict[column.name] = value
            else:
                new_dict[column.name] = getattr(self, column.name)
        return new_dict
