from mongoengine import Document, fields
import datetime
# Create your models here.
class Admin(Document):
    admin_id = fields.StringField(required = True, unique = True)
    email = fields.EmailField(required = True)
    
class Subscribtion(Document):
    is_active = fields.BooleanField(default=True)
    admin_id = fields.StringField(required = True)
    plan_id = fields.StringField(required = True)
    plan_name = fields.StringField(required = True)
    duration_date = fields.IntField(required = True)
    create_date = fields.DateField(required = True)
    expiry_date = fields.DateField(required = True)

class Notification(Document):
    admin_id = fields.StringField(required = True)
    plan_type = fields.StringField(required=True)
    message = fields.StringField(required=True)
    sent_time = fields.DateTimeField(required=True, default=datetime.datetime.utcnow)