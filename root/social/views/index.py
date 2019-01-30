from django.shortcuts import render, redirect
from django.utils import timezone
from social.models import Post#, Followers
from social.forms import PostForm, EditForm, DeleteForm, CommentForm


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[::1] 
        return render(request, 'social/index.html', {'latest_posts_list':posts, 'postform':PostForm(), 'editform':EditForm(), 'commentform':CommentForm()})
    return redirect('/login')


#        following_list = []
#        for follows in Followers.objects.filter(is_followed_by=request.user):
#            following_list.append(follows.user.username)
