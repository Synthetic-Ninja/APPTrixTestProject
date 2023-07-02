from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from services.image_service import WatermarkImage


class ClientSex(models.Model):
    """Модель пола пользователей"""
    sex_name = models.TextField(null=False)


class Client(AbstractUser):
    """Модель пользователя"""

    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    sex = models.ForeignKey(to=ClientSex, on_delete=models.CASCADE)
    email = models.EmailField(null=False, unique=True)
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True,
                               default='default/default_avatar.png')

    position_latitude = models.FloatField(validators=(MaxValueValidator(90), MinValueValidator(-90)))
    position_longitude = models.FloatField(validators=(MaxValueValidator(180), MinValueValidator(-180)))

    def save(self, *args, **kwargs):
        if self.avatar:
            self.avatar.file = WatermarkImage(self.avatar.file).get()

        return super().save(*args, **kwargs)


class ClientMatch(models.Model):
    """Модель для хранения симпатий пользователей"""

    from_client_id = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name='from_user')
    to_client_id = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('from_client_id', 'to_client_id')
