"""
Run via: python manage.py shell < seed_data.py
"""

from datetime import date
from pets.models import Pet
from photos.models import Photo
from common.models import Comment, Like

# ── Pets ──────────────────────────────────────────────────────────────────────

pets_data = [
    {
        "name": "Buddy",
        "personal_photo": "https://images.dog.ceo/breeds/labrador/n02099712_3853.jpg",
        "date_of_birth": date(2019, 4, 10),
    },
    {
        "name": "Whiskers",
        "personal_photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg",
        "date_of_birth": date(2020, 8, 22),
    },
    {
        "name": "Daisy",
        "personal_photo": "https://images.dog.ceo/breeds/beagle/n02088364_11136.jpg",
        "date_of_birth": date(2018, 1, 5),
    },
    {
        "name": "Mittens",
        "personal_photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Kittyply_edit1.jpg/1200px-Kittyply_edit1.jpg",
        "date_of_birth": date(2021, 11, 30),
    },
    {
        "name": "Max",
        "personal_photo": "https://images.dog.ceo/breeds/golden-retriever/n02099601_7742.jpg",
        "date_of_birth": date(2017, 6, 15),
    },
]

created_pets = []
for data in pets_data:
    pet, created = Pet.objects.get_or_create(name=data["name"], defaults=data)
    # slug is set on first save with pk=None, so we need a second save to embed pk
    if created:
        pet.save()
    created_pets.append(pet)
    print(f"{'Created' if created else 'Found'} pet: {pet.name} (slug={pet.slug})")

buddy, whiskers, daisy, mittens, max_ = created_pets

# ── Photos ────────────────────────────────────────────────────────────────────
# Photo.photo is an ImageField — we store a relative path string directly to
# avoid needing real files in a seed script.

photos_data = [
    {
        "photo": "photos/buddy_park.jpg",
        "description": "Buddy chasing frisbees at the local park",
        "location": "Central Park, NYC",
        "tagged": [buddy, max_],
    },
    {
        "photo": "photos/whiskers_window.jpg",
        "description": "Whiskers judging the world from the windowsill",
        "location": "Home - Living Room",
        "tagged": [whiskers],
    },
    {
        "photo": "photos/daisy_beach.jpg",
        "description": "Daisy splashing in the waves on a sunny afternoon",
        "location": "Malibu Beach, CA",
        "tagged": [daisy],
    },
    {
        "photo": "photos/mittens_nap.jpg",
        "description": "Mittens doing what cats do best — sleeping everywhere",
        "location": "Home - Bedroom",
        "tagged": [mittens, whiskers],
    },
    {
        "photo": "photos/max_hike.jpg",
        "description": "Max conquering the mountain trail like a true adventurer",
        "location": "Rocky Mountain National Park",
        "tagged": [max_, buddy, daisy],
    },
    {
        "photo": "photos/buddy_whiskers.jpg",
        "description": "Unlikely best friends sharing a sunny afternoon nap",
        "location": "Backyard Garden",
        "tagged": [buddy, whiskers],
    },
]

created_photos = []
for data in photos_data:
    tagged = data.pop("tagged")
    photo, created = Photo.objects.get_or_create(
        photo=data["photo"], defaults=data
    )
    if created:
        photo.tagged_pets.set(tagged)
    created_photos.append(photo)
    print(f"{'Created' if created else 'Found'} photo: {photo.location} — {photo.photo}")

# ── Comments ──────────────────────────────────────────────────────────────────

comments_data = [
    (created_photos[0], "Buddy looks so happy! What a good boy!"),
    (created_photos[0], "I love how energetic he is, wish my dog ran that fast."),
    (created_photos[1], "Classic cat move. Whiskers owns that windowsill."),
    (created_photos[2], "Daisy at the beach is the cutest thing I've seen all week!"),
    (created_photos[2], "She looks like she was born for the ocean!"),
    (created_photos[3], "Mittens and Whiskers napping together — my heart is full."),
    (created_photos[4], "Max on a hike?! He looks like a poster dog for the outdoors."),
    (created_photos[4], "Amazing shot, the lighting is perfect!"),
    (created_photos[4], "I want to take MY dog on this trail now."),
    (created_photos[5], "A dog and a cat as best friends — this is everything."),
    (created_photos[5], "The way Buddy is watching over Whiskers is adorable."),
]

for photo, text in comments_data:
    comment, created = Comment.objects.get_or_create(text=text, to_photo=photo)
    print(f"{'Created' if created else 'Found'} comment on photo {photo.pk}: \"{text[:50]}...\"")

# ── Likes ─────────────────────────────────────────────────────────────────────

likes_distribution = {
    0: 12,  # buddy park
    1: 7,   # whiskers window
    2: 15,  # daisy beach
    3: 9,   # mittens nap
    4: 20,  # max hike
    5: 18,  # buddy + whiskers
}

for photo_idx, count in likes_distribution.items():
    photo = created_photos[photo_idx]
    existing = Like.objects.filter(to_photo=photo).count()
    to_create = max(0, count - existing)
    Like.objects.bulk_create([Like(to_photo=photo) for _ in range(to_create)])
    print(f"Photo {photo.pk} ({photo.location}): {Like.objects.filter(to_photo=photo).count()} likes")

print("\nSeed complete.")
print(f"  Pets:     {Pet.objects.count()}")
print(f"  Photos:   {Photo.objects.count()}")
print(f"  Comments: {Comment.objects.count()}")
print(f"  Likes:    {Like.objects.count()}")
