from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    user_image_url = serializers.SerializerMethodField('get_user_image_url')

    def get_user_image_url(self, message):
        if message.sender.profile.image:
            return message.sender.profile.image.url
        return ''

    class Meta:
        model = Message
        fields = ('message_id', 'sender', 'date_time', 'message', 'user_image_url')
