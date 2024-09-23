from web_template.extensions import BaseModel, db


class Student(BaseModel):
    __tablename__ = 'students'

    name = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(8), nullable=True)

    def __repr__(self):
        return f'<Student {self.name}>'
