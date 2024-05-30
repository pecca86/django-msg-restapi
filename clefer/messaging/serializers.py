from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    message_text = serializers.CharField(max_length=500, allow_blank=True, required=True)
    send_date = serializers.DateTimeField(read_only=True)
    received_date = serializers.DateTimeField(read_only=True)
    # sender_id = serializers.IntegerField(read_only=True)
    sender_id = serializers.ReadOnlyField(source='sender.id')
    receiver_id = serializers.IntegerField(required=True)
    is_read = serializers.BooleanField(read_only=True)


    def create(self, validated_data):
        return Message.objects.create(**validated_data)
    
    def delete(self, instance):
        instance.delete()


    class Meta:
        model = Message
        fields = ['id', 'message_text', 'send_date', 'received_date', 'sender_id', 'receiver_id', 'is_read']

