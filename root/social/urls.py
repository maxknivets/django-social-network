from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = 'social'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls, name='admin'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('following/<int:user_id>/', views.following, name='following'),
    path('followers/<int:user_id>/', views.followers, name='followers'),
    path('<int:comment_id>/showcomment/', views.showcomment, name='view_comment'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('settings/', views.changeinfo, name='changeinfo'),
    path('', views.index, name='index'),

    path('api/validate_username/', views.validate_username, name='validate_username'),
    path('api/post/', views.post, name='post'),
	path('api/databasecheck/<int:post_id>/', views.databasecheck, name='databasecheck'),
	path('api/commentdatabasecheck/<int:comment_id>/', views.commentdatabasecheck, name='commentdatabasecheck'),
    path('api/getpostinfo/<int:post_id>/', views.getpostinfo, name='getpostinfo'),
    path('api/getcommentinfo/<int:comment_id>/', views.getcommentinfo, name='getcommentinfo'),
    path('api/like/', views.like, name='like'),
    path('api/dislike/', views.dislike, name='dislike'),
    path('api/edit/', views.edit, name='edit'),
    path('api/delete/', views.delete, name='delete'),
    path('api/comment/', views.comment, name='comment'),
    path('api/commentedit/', views.commentedit, name='commentedit'),
    path('api/commentdelete/', views.commentdelete, name='commentdelete'),
    path('api/follow/', views.follow, name='follow'),
    ]
