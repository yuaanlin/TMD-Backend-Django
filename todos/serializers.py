
from rest_framework_mongoengine.serializers import DocumentSerializer

from todos.models import Todo


class TodoSerializer(DocumentSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
