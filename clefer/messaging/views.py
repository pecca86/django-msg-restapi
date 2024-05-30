from rest_framework.parsers import JSONParser
from .models import Message
from .serializers import MessageSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db.utils import IntegrityError
from django.db.models import Q

# This route can also the the following query parameters: qstring
@api_view(['GET', 'POST'])
def get_messages(request, format='json'):

    if request.method == 'GET':
        """
        Get all user's messages
        """
        qstring = request.GET.get('qstring', '')
        messages = Message.objects.filter(Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)).filter(normalized_msg_text__contains=qstring)

        for message in messages:
            message.received_date = timezone.now()
            message.save()

        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
            """
            Create a new message
            """
            try:
                data = JSONParser().parse(request)
                serializer = MessageSerializer(data=data)

                if serializer.is_valid():
                    serializer.save(sender=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response({'message': 'No receiver with that id found.'}, status=status.HTTP_404_NOT_FOUND)
            
@api_view(['GET'])
def get_unread_messages(request, format='json'):
    """
    Get all user's unread messages
    """
    messages = Message.objects.all().filter(receiver_id=request.user.id).filter(is_read=False)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_send_messages(request, format='json'):
    """
    Get all user's sent messages
    """
    messages = Message.objects.all().filter(sender_id=request.user.id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_received_messages(request, format='json'):
    """
    Get all user's received messages
    """
    messages = Message.objects.all().filter(receiver_id=request.user.id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def get_messages_by_user(request, user_id, format='json'):
    """
    Get all messages by a specific user
    """
    messages = Message.objects.all().filter(sender_id=user_id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_message(request, message_id, format='json'):
    """
    Get a specific message by ID
    """
    try:
        # only get the message if the user is the sender or receiver
        user_id = request.user.id
        message = Message.objects.get(pk=message_id)
        if message.sender_id != user_id and message.receiver_id != user_id:
            return Response({'message': 'No message with that id found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if message.receiver_id == user_id:
            message.is_read = True
            message.save()

    except Message.DoesNotExist:
        return Response({'message': f'message with id {message_id} not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MessageSerializer(message)
    return Response(serializer.data)