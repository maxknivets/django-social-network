from django.shortcuts import render, redirect
from django.utils import timezone
from social.models import Post, Profile#, Follower
from social.forms import Post_form, Edit_form, Delete_form, Comment_form

def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[::1]
        last_post = Post.objects.get_queryset().last()
        return render(request, 'social/index.html', 
        {'latest_posts_list':posts,
        'latest_post':last_post,
        'postform':Post_form(),
        'editform':Edit_form(),
        'commentform':Comment_form(),
        'loggeduserpfp':Profile.objects.filter(user=request.user).first().profile_picture,
        })
        pdb.set_trace()
    return redirect('/login')

#        personal_feed = []
#        for follows in Follower.objects.filter(is_followed_by=request.user):
#            personal_feed.append(follows.user.username)