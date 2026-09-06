from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Prefetch
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from common.mixin import CheckUserIsOwner
from pets.forms import PetForm
from pets.models import Pet
from photos.models import Photo

# Create your views here.

# Class-based view
class PetAddView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-add-page.html' # give it here not to rename the files

    def get_success_url(self) -> str:
        return reverse('accounts:details', kwargs={"pk": self.object.user.pk}) #redirect to the page of the user, that created this animal

    def form_valid(self, form):
        self.object = form.save(commit=False) # self the object without saving it into the DB
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)


# Function-based view - created before creating the function-based view
# def pets_add(request: HttpRequest) -> HttpResponse:
#     form = PetForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#        form.save()
#        return redirect('accounts:details', pk=1)
#     context = {
#         "form": form
#     }
#     return render(request, 'pets/pet-add-page.html', context)

# Class-based view:
class PetEditView(CheckUserIsOwner, UpdateView):
    model = Pet
    form_class = PetForm
    slug_url_kwarg = 'pet_slug'
    template_name = 'pets/pet-edit-page.html'

    def test_func(self) -> bool:
        return self.request.user == self.get_object().user

    def get_success_url(self) -> str:
        return reverse(
            'pets:details',
            kwargs={
                "username": 'username', "pet_slug": self.object.slug
            }
        )

# Function-based view:
# def pets_edit(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)
#     if request.method == 'POST' and form.is_valid():
#         instance = form.save()
#         return redirect('pets:details', username='username', pet_slug=instance.slug)
#     context = {
#         'pet': pet,
#         'form': form
#     }
#     return render(request, 'pets/pet-edit-page.html', context)


# Class-based view:
class PetDeleteView(DeleteView):
    model = Pet
    form_class = PetForm
    slug_url_kwarg = "pet_slug"
    template_name = "pets/pet-delete-page.html"

    def get_success_url(self) -> str:
        return reverse('accounts:details', kwargs={"pk": self.object.user.pk})

    #the delete form will be with populated data
    def get_initial(self):
        return self.object.__dict__

    # same result, but preferred is the upper one
    # def get_context_data(self, **kwargs):
    #     context = super( ).get_context_data(**kwargs)
    #     context['form'] = PetForm(instance=self.object)



# Function-based view:
# def pets_delete(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)
#     if request.method == 'POST' and form.is_valid():
#         pet.delete()
#         return redirect('accounts:details', pk=1)
#     context = {
#         'pet': pet,
#         'form': form
#     }
#     return render(request, 'pets/pet-delete-page.html', context)

# Class-based view:
class PetDetailView(DetailView):
    # we have a customer queryset, so we don't use model
    queryset = Pet.objects.prefetch_related(
         Prefetch(
             'photo_set',
             queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
         )
    )
    slug_url_kwarg = 'pet_slug'
    template_name = 'pets/pet-details-page.html'

# Function-based view:
# def pets_details(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     # take photos of all pets, join all tagget pets and all like sets
#     pet = Pet.objects.prefetch_related(
#          Prefetch(
#              'photo_set',
#              queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
#          )
#     ).get(slug=pet_slug)
#     context = {
#         'pet': pet,
#     }
#     return render(request, 'pets/pet-details-page.html', context)



