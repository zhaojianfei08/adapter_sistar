from web_template.extensions import BaseModel, db


class Author(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)
    """
    backref
    描述: 为另一个模型定义反向引用。使用 backref 可以在定义关系的一方，自动生成反向引用。通过反向引用，可以从关联的对象中访问到原始对象。
    back_populates
    描述: 用于显式指定关系的反向属性。如果两个模型的关系非常复杂，back_populates 允许更精细的控制，必须在两个模型中都设置。
    lazy
    描述: 控制关系属性的加载方式。它可以用来优化查询性能，避免不必要的数据库访问。
    选项:
    'select': 默认方式，按需加载，访问关系时发出查询。
    'joined': 在执行父查询时通过 JOIN 一起加载关联数据。
    'subquery': 通过子查询一起加载关联数据。
    'noload': 从不加载关联数据。
    'dynamic': 返回一个查询对象，而不是对象列表，允许你使用过滤、排序等操作。
    cascade
    描述: 定义级联操作，控制当父对象被修改或删除时，如何处理关联的子对象。常见的级联选项有：
    'save-update': 在保存或更新父对象时，也保存或更新子对象。
    'delete': 删除父对象时，删除关联的子对象。
    'delete-orphan': 当子对象不再与任何父对象关联时，自动删除子对象。
    'all': 包含所有级联操作。
    uselist
    描述: 指定是否返回一个列表。通常用于一对多关系中，默认为 True（返回列表）。如果设置为 False，则期望一对一关系，返回单个对象。
    foreign_keys
    描述: 明确指定哪一个字段用作外键，适用于在一个模型中有多个外键指向同一个表的情况。
    primaryjoin
    描述: 用来定义两个表之间关系的自定义连接条件。这个选项在复杂的关系中很有用，尤其是多对多或自关联的表。
    secondary
    描述: 用于定义多对多关系。secondary 参数指定了关联表，通过该表来关联两个模型。
    order_by
    描述: 指定返回关联对象的默认排序顺序。
    remote_side
    描述: 在自关联（即一个表与自身关联）的情况下，定义哪个字段在关联表的 "另一侧" 被用作外键。这对于实现自引用关系（如树状结构）非常有用。
    post_update
    描述: 如果设置为 True，会导致关系更新为 "post-update" 操作。主要在循环外键的情况下使用，用于避免死锁。
    single_parent
    描述: 设置为 True 时，SQLAlchemy 将强制每个子对象仅属于一个父对象，适用于某些层次结构。
    viewonly
    描述: 设为 True 时，关系变为只读，不能通过关系来添加、更新或删除关联对象。
    sync_backref
    描述: 默认为 True，用于控制反向引用属性的同步。如果设置为 False，则不会自动更新反向属性。
    """

    def add_book(self, book):
        pass


class Book(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', ondelete='SET NULL'), nullable=True)


    """
    'CASCADE': 删除父行时，子行也会被自动删除。
    'SET NULL': 删除父行时，外键值会被设置为 NULL。
    'RESTRICT': 阻止删除父行，直到相关的子行被删除。
    'NO ACTION': 与 'RESTRICT' 类似，但行为可能会因数据库的不同而异。
    'SET DEFAULT': 删除父行时，将外键列设置为默认值。
    """
