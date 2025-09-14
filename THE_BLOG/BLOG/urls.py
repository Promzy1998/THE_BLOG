from django.urls import path
from .views import HomePageView, AuthorAccountView, DetailAuthorPost, EditAuthorPost, DeleteAuthorPost

urlpatterns = [
       
    path('Author/', AuthorAccountView.as_view(), name='author_account'),
    path('', HomePageView.as_view(), name='Index'),
    path('<str:category_str>/<str:category>', HomePageView.as_view(), name='Index_category'),
    path('<str:category_str>/<str:category>/<slug:slug>', DetailAuthorPost.as_view(), name='DetailPost'),

    path('update/<str:category>/<slug:slug>/edit', EditAuthorPost.as_view(), name='EditPost'),

    path("author's_delete/<str:category>/<slug:slug>/delete", DeleteAuthorPost.as_view(), name='DeletePost'), 
  
]