import pytest

from accounts.models import User

@pytest.mark.django_db
def test_should_create_user():
    # Given
    username = "u@u.com"
    password = "pw"
    # When
    user = User.objects.create(username=username, password=password)
    # Then
    assert user.username == username
    assert user.password == password
    assert user.is_superuser == False
    assert user.is_staff == False
    assert user.is_active == True
    assert user.is_authenticated == True
    assert user.is_anonymous == False
    assert user.groups.count() == 0
    assert user.user_permissions.count() == 0
    assert user.messages.count() == 0
    assert user.__str__() == username

