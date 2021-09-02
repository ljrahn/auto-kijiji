from . import db
from . import ma
from sqlalchemy.sql import func

class Tracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True)
    address_to = db.Column(db.JSON, nullable=False)
    address_from = db.Column(db.JSON, nullable=False)
    tracking_status = db.Column(db.JSON, nullable=False)

    def __init__(self, tracking_number, address_to, address_from, tracking_status):
        self.tracking_number = tracking_number
        self.address_to = address_to
        self.address_from = address_from
        self.tracking_status = tracking_status

class TrackingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tracking_number', 'address_to', 'address_from', 'tracking_status')

tracking_schema = TrackingSchema()
all_trackings_schema = TrackingSchema(many=True)
