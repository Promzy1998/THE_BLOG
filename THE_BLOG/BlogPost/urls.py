from django.urls import path
from . import views
from .views import DataPostView, PostView,   EditAuthorPost, DeleteAuthorPost, DetailAuthorPost
urlpatterns=[
path("AuthorPost/<slug:slugs>/<str:category>", PostView.as_view(), name="PostViews"),
path("AuthorPost/<slug:slugs>", PostView.as_view(), name="PostView"),
path("BlogUpload/", DataPostView.as_view(), name="DataPostView"),
path("AuthorPost/<slug:slugs>/<str:category>/<slug:slug>/delete", DeleteAuthorPost.as_view(), name="DeletePostView"),
path("AuthorPost/<str:author>/<slug:slug>/edit", EditAuthorPost.as_view(), name="EditPostView"),
path('AuthorPost/<str:author>/<str:category>/<slug:slug>', DetailAuthorPost.as_view(),name='DetailPostView'),

]


