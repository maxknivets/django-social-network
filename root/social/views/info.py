from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from social.models import User, Post, Comment, Follower, Profile
from social.forms import Edit_form, Delete_form, Comment_form, Change_profile_info_form, Profile_picture_form
import datetime, pdb

def changeinfo(request):
    if request.user.is_authenticated:
        response = None
        if request.method == 'POST':
            response = False
            form = Change_profile_info_form(request.POST)
            if form.is_valid():
                response = True
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.save()
                profile = Profile.objects.filter(user=request.user).first()
                if profile:
                    profile.bio=form.cleaned_data['bio']
                    profile.location=form.cleaned_data['location']
                else:
                    profile = Profile(user=request.user, bio=form.cleaned_data['bio'], location=form.cleaned_data['location'])
                profile.save()
        return render(request, 'social/change_info.html', {'change_profile_info_form': Change_profile_info_form, 'response': response})
    return redirect('/')

def changepfp(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = Profile_picture_form(request.POST, request.FILES)
        if form.is_valid():
            picture = Profile.objects.filter(user=request.user).first()
            if picture:
                picture.profile_picture = form.cleaned_data['profile_picture']
            else:
                picture = ProfilePicture(user = request.user, profile_picture = form.cleaned_data['profile_picture'])
            picture.save()
        return render(request, 'social/change_info.html', {})
    return redirect('/')

def user(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        profile_picture = Profile.objects.filter(user=user).first()
        if profile_picture:
            profile_picture = profile_picture.profile_picture
        logged_user_profile_picture = Profile.objects.filter(user=request.user).first()
        if logged_user_profile_picture:
            logged_user_profile_picture = logged_user_profile_picture.profile_picture
        users_posts = Post.objects.filter(user=user)
        info = Profile.objects.filter(user=user).first()
        following = Follower.objects.filter(is_followed_by=user)
        return render(request, 'social/user.html', {'profile':info,'theuser':user, 'pfp':profile_picture, 'loggeduserpfp': logged_user_profile_picture,'latest_posts_list':users_posts, 'latest_post':users_posts.first(), 'following':following, 'editform':Edit_form(), 'commentform':Comment_form()})
    return redirect('/')

def showcomment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        replies = Comment.objects.filter(in_reply_to_comment=comment_id)
        return render(request, 'social/singlecomment.html',{'comment':comment, 'replies':replies, 'post':comment.post, 'editform':Edit_form(), 'commentform':Comment_form()})
    return redirect('/')