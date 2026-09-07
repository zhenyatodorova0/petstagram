from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from photos.validators import FileSizeValidator

UserModel = get_user_model()
# Create your models here.
class Photo(models.Model):
    # photo = models.ImageField(
    #     upload_to='meadia',
    #     validators=[
    #         FileSizeValidator(5)
    #     ]
    # )
    photo = CloudinaryField('image')
    description = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(10)
        ],
        null = True,
        blank = True,
    )
    location = models.CharField(
        max_length=30
    )
    tagged_pets = models.ManyToManyField(
        to="pets.Pet",
    )
    date_of_publication = models.DateField(
        auto_now=True
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

