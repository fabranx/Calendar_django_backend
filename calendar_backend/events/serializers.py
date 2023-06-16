from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()  # chiama il methodo get_<field_name>

    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = Event
        fields = ('id', 'author', 'author_name', 'date', 'description', 'created_at', 'updated_at')