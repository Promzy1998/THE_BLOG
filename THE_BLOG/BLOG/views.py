
from django.views.generic import TemplateView, ListView, DetailView
from THE_BLOG.BlogPost.models import DataPost
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
# from BlogPost.views import PostView
from BlogPost.views import DetailAuthorPost, EditAuthorPost,  DeleteAuthorPost

# Create your views here.

class HomePageView(ListView):
    model = DataPost
    template_name = 'Index.html'
    
    def get_queryset(self):
        self.paginate_normal_by = 8
        self.paginate_other_by = 1
        self.category=self.kwargs.get('category')
      
  
        if self.category:
             return DataPost.objects.filter(category__iexact=self.category)
        return DataPost.objects.filter(category__iexact='lifestyle') 

    # def get_context_data(self, **kwargs):
    #      return PostView().get_context_data(**kwargs)
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.queryset=self.get_queryset().filter(priority="Normal").order_by("-created_at")  
         # ✅ Get current page number
        page_number = self.request.GET.get("page") or 1
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

         # ✅ Handle normal posts  
        normal_posts = self.get_queryset()
        paginator = Paginator(self.queryset, self.paginate_normal_by)
        page_obj = paginator.get_page(page_number)
        paginated_posts = list(page_obj.object_list)

        # ✅ Handle Other posts 
        footer_post = self.get_queryset().filter(priority="FooterPics").order_by("-created_at")
        bigger_post=self.get_queryset().filter(priority="BiggerPics").order_by("-created_at")

        footer_paginator = Paginator(footer_post, self.paginate_other_by)
        bigger_paginator = Paginator(bigger_post, self.paginate_other_by)

        footer_page_obj = footer_paginator.get_page(page_number)
        bigger_page_obj = bigger_paginator.get_page(page_number)
        footer_paginated_posts = list(footer_page_obj.object_list)
        bigger_paginated_posts = list(bigger_page_obj.object_list)

        

        context["recent_post"] = paginated_posts[:2]
        context["bigger_post"]=bigger_paginated_posts[:1]
        context["first_all_posts"] = paginated_posts[2:5]
        context["second_all_posts"] = paginated_posts[5:6]
        context["third_all_posts"] = paginated_posts[6:8]
        context["footer_post"] = footer_paginated_posts[:1]
        context["page_obj"] = page_obj
        context["selected_category"] = self.kwargs.get("category", "").lower()
        if  not context["selected_category"]:
            context["selected_category"]= "lifestyle"   
        return context    

class DetailAuthorPost(DetailAuthorPost):
    def get_object(self, queryset=None):
        self.slug = self.kwargs.get('slug')  # or 'id' based on your URLConf
        self.category_name = self.kwargs.get('category')
        # Ensure we get the right post by slug and author
        obj = get_object_or_404(DataPost, slug=self.slug)
        return obj
class EditAuthorPost(EditAuthorPost):
    def get_object(self, queryset=None):
        return get_object_or_404(DataPost, slug=self.kwargs.get('slug'))
   
    def get_success_url(self):
        return reverse_lazy('Index_category', kwargs={
            'category': self.object.category.lower(),
            'category_str':"Category"
            
        }) 
class DeleteAuthorPost(DeleteAuthorPost):
    def get_object(self, queryset=None):
        return get_object_or_404(DataPost, slug=self.kwargs.get('slug'))

    def get_success_url(self):
         return reverse_lazy('Index_category', kwargs={
            'category': self.object.category.lower(),
        })               


class AuthorAccountView(TemplateView):
    template_name = 'author_account.html'
