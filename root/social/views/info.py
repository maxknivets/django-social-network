from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from social.models import User, Post, Comment, Followers, Profile
from social.forms import EditForm, DeleteForm, CommentForm, ChangeForm
import datetime, pdb



def settings(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = ChangeForm(request.POST)
        if form.is_valid():
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
            data = {
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'bio': profile.bio,
                'location': profile.location,
            }
            return JsonResponse(data)
    return redirect('/')



def user(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        users_posts = Post.objects.filter(user=user)
        info = Profile.objects.filter(user=user).first()
        following = Followers.objects.filter(is_followed_by=user)
        return render(request, 'social/user.html', {'profile':info,'theuser':user, 'latest_posts_list':users_posts, 'following':following, 'editform':EditForm(), 'commentform':CommentForm(), 'changeform':ChangeForm()})
    return redirect('/')



def showcomment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        replies = Comment.objects.filter(in_reply_to_comment=comment_id)
        return render(request, 'social/singlecomment.html',{'comment':comment, 'replies':replies, 'post':comment.post, 'editform':EditForm(), 'commentform':CommentForm()})
    return redirect('/')

