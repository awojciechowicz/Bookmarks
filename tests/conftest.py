import os
import pytest
from django.contrib.auth.models import User
from account.models import Profile

# Wymagane, bo pytest-playwright uruchamia testy w asyncio event loop,
# co konfliktuje z synchronicznymi operacjami DB w Django.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def test_user(db):
    """Tworzy użytkownika testowego z profilem."""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPassword123'
    )
    Profile.objects.create(user=user)
    return user
