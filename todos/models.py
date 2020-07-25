
import django
import mongoengine


class Todo(mongoengine.Document):
    title = mongoengine.StringField(blank=False, default='')
    description = mongoengine.StringField(blank=False, default='')
    deadline = mongoengine.DateTimeField(default=django.utils.timezone.now)
