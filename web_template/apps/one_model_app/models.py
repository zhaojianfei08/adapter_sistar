from web_template.extensions import BaseModel, db


class Task(BaseModel):
    __tablename__ = 'tasks'

    task_name = db.Column(db.String(80), nullable=False)
    comments = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<Task {self.task_name}>'
