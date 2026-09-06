from django.db.models import BooleanField, Exists, OuterRef, Value
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from common.forms import CommentForm
from common.models import Like
from photos.models import Photo


# Create your views here.
class HomePageView(ListView):
    queryset = Photo.objects.prefetch_related('tagged_pets', 'like_set')
    context_object_name = 'all_photos'
    template_name = 'common/home-page.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            qs = qs.filter(tagged_pets__name__icontains=pet_name)

        if self.request.user.is_authenticated:
            qs = qs.annotate(
                is_liked_by_user=Exists(
                    Like.objects.filter(
                        to_photo_id=OuterRef('pk'),
                        user=self.request.user,
                    )
                )
            )
        else:
            qs = qs.annotate(
                is_liked_by_user=Value(False, output_field=BooleanField())
            )

        return qs

# def home_page(request: HttpRequest) -> HttpResponse:
#     form = SearchForm(request.GET or None)
#     all_photos = Photo.objects.prefetch_related('tagged_pets', 'like_set')
#
#     if request.GET and form.is_valid():
#         searched_name = form.cleaned_data['pet_name']
#         all_photos = all_photos.filter(tagged_pets__name__icontains=searched_name)
#
#     context = {
#         'all_photos': all_photos,
#     }
#     return render(request, 'common/home-page.html', context)

def like_functionality(request: HttpRequest, photo_pk: int) -> HttpResponse:
    like_object = Like.objects.filter(to_photo_id=photo_pk, user=request.user).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(
            to_photo_id=photo_pk,
            user=request.user,
        )
    return redirect(request.META.get('HTTP_REFERER') + f"#{photo_pk}") # load the page of the photo that the user liked

def share_functionality(request: HttpRequest, photo_pk: int) -> HttpResponse:
    # this will work only on localhost as it copies  the value on the server
    copy(request.META['HTTP_HOST'] + resolve_url('photos:details', photo_pk))
    return redirect(request.META['HTTP_REFERER'] + f"#{photo_pk}")
    # copy(request.META.get("HTTP_REFERER")[:-1] + resolve_url('photos:details', photo_pk))
    # return redirect(request.META.get("HTTP_REFERER") + f"#{photo_pk}")

def add_comment(request: HttpRequest, photo_pk: int) -> HttpResponse:
    if request.method == 'POST':
        photo = Photo.objects.get(pk=photo_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()
        return redirect(request.META.get('HTTP_REFERER') + f"#{photo_pk}")
