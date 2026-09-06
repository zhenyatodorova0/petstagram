from django.contrib import admin
from unfold.admin import ModelAdmin
from photos.models import Photo


# Register your models here.
@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = ['id', 'description', 'date_of_publication', 'tagged_pets_list']

    @staticmethod
    def tagged_pets_list(obj):
        return ', '.join(pet.name for pet in obj.tagged_pets.all())