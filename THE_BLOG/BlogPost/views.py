from django.shortcuts import render
from django.urls import reverse_lazy
from THE_BLOG.BlogPost.models import DataPost
from .forms import DataPostForm
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import DataPost
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.base import File
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

# Create your views here.
class DataPostView(LoginRequiredMixin, CreateView):
    model = DataPost
    form_class = DataPostForm
    context_object_name = "posts"
    template_name = "postUpload.html"
    login_url = reverse_lazy("signup_login")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

        # if image:
        #     relative_path = image.replace(settings.MEDIA_URL, "")
        #     full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

   



    def form_valid(self, form):
        form.instance.author = self.request.user

        # Generate a slug if missing
        if not form.instance.slug:
            base_slug = slugify(form.instance.Title)
            slug = base_slug
            counter = 1
            while DataPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            form.instance.slug = slug

        form.save()  # ✅ no commit keyword here

        return JsonResponse({'redirect_url': self.get_success_url()})



    def form_invalid(self, form):
        print("⚠️ FORM INVALID")
        print(form.errors)
        return JsonResponse({'errors': form.errors}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get_success_url(self):
    #     return reverse_lazy('PostViews', kwargs={
    #         'author': self.request.user.username,
    #         'category': "Lifestyle"
    #     })

    def get_success_url(self):
        return reverse_lazy('PostView',kwargs={
           'slugs': self.request.user.slugs})

    def upload_post(request):
        if request.method == 'POST':
            form = DataPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Success'})
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        else:
            return render(request, 'BlogPost_form.html')     

class PostView(ListView):
    model = DataPost
    template_name = "author_post.html"
    context_object_name = "posts"
    paginate_by = 8  # 2 for recent_post + 3 for remaining_posts

    def get_queryset(self):
        self.author_slug_name = self.kwargs.get("slugs")
        self.category = self.kwargs.get("category") or "lifestyle"

        user_model = get_user_model()
        self.author = get_object_or_404(user_model, slugs__iexact =self.author_slug_name)

        self.author_slug = self.author.slugs
        self.author_name = self.author.username

        self.queryset = DataPost.objects.filter(author=self.author, priority="Normal").order_by("-created_at")

        if self.category:
            return self.queryset.filter(category__iexact=self.category)

        return self.queryset.filter(category__iexact="lifestyle")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        # ✅ Get current page number
        page_number = self.request.GET.get("page") or 1
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        # ✅ Handle Normal posts
        normal_posts = self.get_queryset()
        paginator = Paginator(normal_posts, self.paginate_by)
        page_obj = paginator.get_page(page_number)
        paginated_posts = list(page_obj.object_list)

      

        context["recent_post"] = paginated_posts[:2]
        context["first_all_posts"] = paginated_posts[2:5]
        context["second_all_posts"] = paginated_posts[5:6]
        context["third_all_posts"] = paginated_posts[6:8]
        context["page_obj"] = page_obj
        context["selected_category"] = self.kwargs.get("category", "").lower()
        if  not context["selected_category"]:
            context["selected_category"]= "lifestyle"   
        

        # ✅ Handle BiggerPics pagination — 1 per page
        bigger_pics_all = DataPost.objects.filter(
            author=self.author,
            priority="BiggerPics", category__iexact=self.kwargs.get("category")
        ).order_by("-created_at")

        bigger_pics_paginator = Paginator(bigger_pics_all, 1)
        context["bigger_pics"] = bigger_pics_paginator.get_page(page_number).object_list
        
        # ✅ Handle footerPics pagination — 1 per page
        footer_pics_all = DataPost.objects.filter(
            author=self.author,
            priority="FooterPics",category__iexact=self.kwargs.get("category") or "lifestyle"
        ).order_by("-created_at")

        footer_pics_paginator = Paginator(footer_pics_all, 1)
        context["footer_pics"] = footer_pics_paginator.get_page(page_number).object_list

        context["author"] = self.author
        context["author_slug"] = self.author_slug
        context["category_author"] = self.author_name
        return context
# for blogpost creation for author
# class CreateAuthorPost(LoginRequiredMixin, CreateView):
#     model=DataPost
#     template_name='Create_post.html'
#     fields=('Title','PostImage','category','priority','Description')

#     def test_func(self): 
#         obj = self.get_object()
#         return obj.author == self.request.user
class DeleteAuthorPost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=DataPost
    template_name='Delete_post2.html'
    def get_success_url(self):
        return reverse_lazy('PostViews', kwargs={
            'slugs': self.request.user.slugs,
            'category': self.object.category.lower(),
        })
    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user
   
class EditAuthorPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=DataPost
    template_name='Edit_post.html'
    context_object_name='Edit'
    form_class = DataPostForm
    def get_success_url(self):
        return reverse_lazy('PostViews', kwargs={
            'slugs': self.request.user.slugs,
            'category': self.object.category,
        })

    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user





class DetailAuthorPost(DetailView):
    model = DataPost
    template_name = "Detail_post.html"
    context_object_name = "Post"
    slug_url_kwarg = 'slug'  # optional but clarifies intent
  

    def get_object(self, queryset=None):
        user_model = get_user_model()
        author = get_object_or_404(user_model, username__iexact=self.kwargs['author'])

        self.slug = self.kwargs.get('slug')  # From URL
        self.category_name = self.kwargs.get('category')

      


        # Safely fetch post matching slug, author, and (optional) category
        obj = get_object_or_404(
            DataPost,
            slug=self.slug,
            author=author,
            category__iexact=self.category_name  # optional but useful for validation
        )
        return obj

    def get_related_posts(self):
        random_posts = (
            DataPost.objects
            .filter(category__iexact=self.category_name)
            .exclude(slug=self.slug)
            .order_by('?')
        )

        seen_images = set()
        seen_titles = set()
        unique_posts = []

        for post in random_posts:
            image_url = post.PostImage.url if post.PostImage else None
            if image_url and image_url not in seen_images and post.Title not in seen_titles:
                seen_images.add(image_url)
                seen_titles.add(post.Title)
                unique_posts.append(post)
            if len(unique_posts) == 3:
                break

        return unique_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_random_posts'] = self.get_related_posts()
        return context


# @csrf_exempt  # Needed because the request is made via raw JavaScript (no CSRF token by default)
# def upload_image_temp(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES['image']
#         filename = f"{uuid.uuid4()}_{image_file.name}"
#         file_path = os.path.join('temp_uploads/', filename)

#         # Save file
#         saved_path = default_storage.save(file_path, ContentFile(image_file.read()))

#         # Build accessible URL for preview or form submission
#         file_url = default_storage.url(saved_path)

#         return JsonResponse({'file_url': file_url})
    
#     return JsonResponse({'error': 'Invalid request'}, status=400)


