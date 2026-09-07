from django.db import migrations
from django.template.defaultfilters import slugify


def fix_pet_slugs(apps, schema_editor):
    Pet = apps.get_model('pets', 'Pet')

    for pet in Pet.objects.all():
        expected_slug = slugify(f"{pet.name}-{pet.pk}")
        if not pet.slug or pet.slug.endswith('-none'):
            pet.slug = expected_slug
            pet.save(update_fields=['slug'])


def reverse_fix_pet_slugs(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_pet_user'),
    ]

    operations = [
        migrations.RunPython(fix_pet_slugs, reverse_fix_pet_slugs),
    ]
