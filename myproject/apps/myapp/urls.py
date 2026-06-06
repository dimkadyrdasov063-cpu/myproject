from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("home/", views.home, name="home"),
    
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path("create/", views.create_article, name="create_article"),
    path("article/<int:pk>/edit/", views.article_edit, name="article_edit"),
    path("article/<int:pk>/delete/", views.article_delete, name="article_delete"),
    path("article/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("article/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    
    path("my-articles/", views.my_articles, name="my_articles"),
    path("profile/", views.profile, name="profile"),
    
    path("login/", auth_views.LoginView.as_view(template_name="articles/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="articles:article_list"), name="logout"),
    path("signup/", views.signup, name="signup"),
    
    path("download-excel/", views.export_articles_to_excel, name="download_excel"),
    
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='articles/password_reset.html',
             success_url='/password_reset/done/'
         ),
         name='password_reset'),
    
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='articles/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='articles/password_reset_confirm.html',
             success_url='/reset/done/'
         ),
         name='password_reset_confirm'),
    
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='articles/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]