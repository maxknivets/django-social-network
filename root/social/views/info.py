from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from social.models import User, Post, Comment, Follower, Profile
from social.forms import Edit_form, Delete_form, Comment_form, Change_profile_info_form, Profile_picture_form
import datetime, pdb

def changeinfo(request):
    if request.user.is_authenticated:
        changes_saved = None
        profile = Profile.objects.filter(user=request.user).first()
        if request.method == 'POST':
            changes_saved = False
            form = Change_profile_info_form(request.POST)
            profile_picture_form = Profile_picture_form(request.POST, request.FILES)
            if profile_picture_form.is_valid():
                changes_saved = True
                profile.profile_picture = profile_picture_form.cleaned_data['profile_picture']
                profile.save()
            elif form.is_valid():
                changes_saved = True
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.save()
                profile.bio = form.cleaned_data['bio']
                profile.location = form.cleaned_data['location']
                profile.save()
        form = Change_profile_info_form(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'bio': profile.bio,
            'location': profile.location,
        })
        return render(request, 'social/change_info.html', 
        {'change_profile_info_form': form, 
        'profile_picture_form': Profile_picture_form, 
        'response': changes_saved, 
        'logged_user': request.user.pk
        })
    return redirect('/')

def user(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        profile_picture = Profile.objects.filter(user=user).first().profile_picture
        logged_user_profile_picture = Profile.objects.filter(user=request.user).first().profile_picture
        users_posts = Post.objects.filter(user=user)
        info = Profile.objects.filter(user=user).first()
        following = Follower.objects.filter(is_followed_by=user)
        return render(request, 'social/user.html', 
        {'profile':info,
        'theuser':user, 
        'pfp':profile_picture, 
        'loggeduserpfp': logged_user_profile_picture,
        'latest_posts_list':users_posts, 
        'latest_post':users_posts.first(), 
        'following':following, 
        'editform':Edit_form(), 
        'commentform':Comment_form()
        })
    return redirect('/')

def showcomment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        replies = Comment.objects.filter(in_reply_to_comment=comment_id)
        return render(request, 'social/singlecomment.html',{'comment':comment, 'replies':replies, 'post':comment.post, 'editform':Edit_form(), 'commentform':Comment_form()})
    return redirect('/')