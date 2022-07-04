from django.urls import path
from blogapi import views

urlpatterns=[
    path('blogs',views.BlogView.as_view()),
    path('blogs/<int:blog_id>', views.BlogDetails.as_view()),
    path('user/account/signup', views.UserSignup.as_view()),
    path('user/account/login', views.UserLogin.as_view()),
    path('user/account/profile', views.AddUserProfile.as_view()),
    path('user/account/editprofile/', views.ProfileDetails.as_view()),
    path('blogs/likes/<int:blog_id>', views.BlogLikes.as_view()),
    path('blogs/comments/add/<int:blog_id>', views.Comments.as_view())
]
