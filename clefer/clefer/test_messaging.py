import pytest

from messaging.models import Message
from accounts.models import User

@pytest.mark.django_db
def test_should_add_a_new_message():
    # Given
    user1 = User(username="pe@pe.com", password="pw")
    user1.save()
    msg = "Test message"
    user1_id = user1.id

    # When
    message = Message(message_text=msg, receiver=user1, sender=user1)
    message.save()

    # Then
    assert Message.objects.count() == 1
    assert Message.objects.first().message_text == msg
    assert Message.objects.first().receiver.id == user1_id
    assert Message.objects.first().sender.id == user1_id
    assert Message.objects.first().is_read == False

@pytest.mark.django_db
def test_should_normalize_message_text():
    # Given
    user1 = User(username="pe@pe.com", password="pw")
    user1.save()
    msg = "Test mEssaGE"

    # When
    message = Message(message_text=msg, receiver=user1, sender=user1)
    message.save()

    # Then
    assert Message.objects.first().normalized_msg_text == "test message"

@pytest.mark.django_db
def test_should_set_send_date():
    # Given
    user1 = User(username="pe@pe.com", password="pw")
    user1.save()
    msg = "Test mEssaGE"

    # When
    message = Message(message_text=msg, receiver=user1, sender=user1)
    message.save()

    # Then
    assert Message.objects.first().send_date is not None

@pytest.mark.django_db
def test_should_set_received_date():
    # Given
    user1 = User(username="pe@pe.com", password="pw")
    user1.save()
    msg = "Test mEssaGE"

    # When
    message = Message(message_text=msg, receiver=user1, sender=user1)
    message.save()

    # Then
    assert Message.objects.first().received_date is not None
