from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from social.models import Post#, Follower
from social.forms import Post_form, Edit_form, Delete_form, Comment_form

@login_required
def index(request):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[::1]
    last_post = Post.objects.get_queryset().last()
    return render(request, 'social/index.html', {
        'latest_posts_list':posts,
        'latest_post':last_post,
        'postform':Post_form(),
        'editform':Edit_form(),
        'commentform':Comment_form(),
        'request_user': request.user,
    })