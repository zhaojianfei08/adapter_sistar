from web_template.extensions import BaseModel, db


class OPCUADevice(BaseModel):
    __tablename__ = 'opcuadevices'

    device_name = db.Column(db.String(128), nullable=False, unique=True)
    url = db.Column(db.String(128), nullable=False)

    opcuapoints = db.relationship('OPCUAPoint', backref='opcuadevice', lazy=True)


class OPCUAPoint(BaseModel):
    __tablename__ = 'opcuapoints'

    tag_uuid = db.Column(db.String(128), nullable=False, unique=True)
    node_id = db.Column(db.String(128), nullable=False)
    interval = db.Column(db.String(128), nullable=False)
    active = db.Column(db.String(128), nullable=False)
    active_alarm = db.Column(db.String(128), nullable=False)
    alarm_up = db.Column(db.String(128), nullable=False)
    alarm_down = db.Column(db.String(128), nullable=False)
    alarm_up_info = db.Column(db.String(128), nullable=False)
    alarm_down_info = db.Column(db.String(128), nullable=False)
    alarm_up_change = db.Column(db.String(128), nullable=False)
    alarm_down_change = db.Column(db.String(128), nullable=False)
    active_archive = db.Column(db.String(128), nullable=False)
    archive_onchange = db.Column(db.String(128), nullable=False)
    archive_interval = db.Column(db.String(128), nullable=False)
    active_scale = db.Column(db.String(128), nullable=False)
    scale_sign = db.Column(db.String(128), nullable=False)
    scale_factor = db.Column(db.String(128), nullable=False)
    mqtt_topic_name = db.Column(db.String(128), nullable=False)
    unit = db.Column(db.String(128), nullable=False)
    comments = db.Column(db.String(128), nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey('opcuadevices.id', ondelete='SET NULL'), nullable=True)

    def __repr__(self):
        return f'<OPCUAPoint {self.comments}>'




