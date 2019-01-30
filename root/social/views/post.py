from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import escape
from social.models import User, Post, Likes, Dislikes
from social.forms import PostForm, EditForm, DeleteForm



def post(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('post_text')
            in_future = form.cleaned_data.get('post_in_future')
            date = timezone.now()
            
            if in_future is not None and in_future > 0:
                date += datetime.timedelta(days=in_future)
            
            post = Post(post_text=text, user=request.user, pub_date=date)
            post.save()
            
            data= {
                'post_text': escape(post.post_text),
                'post_date': post.get_readable_date(),
                'post_id': post.pk,
                'user_id': request.user.pk,
                'username': request.user.username,
            }
            
            return JsonResponse(data)    
    return redirect('/')



def edit(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('id')
            post = get_object_or_404(Post, pk=post_id)
            if request.user == post.user:
                new_text = form.cleaned_data.get('new_text')
                post.post_text = new_text
                post.save()
                data = { 'new_text': escape(new_text) }
                return JsonResponse(data)
    return redirect('/')



def delete(request):
    if request.user.is_authenticated:
        post_id = request.GET.get('id')
        post = get_object_or_404(Post, pk=post_id)
        if request.user == post.user:
            post.delete()
            data = { 'post_id': post_id }
            return JsonResponse(data)
    return redirect('/')





def likes(request):
    if request.user.is_authenticated:
        liked_post_id = request.GET.get('post', None)
        post = get_object_or_404(Post, pk=liked_post_id)
        already_liked = Likes.objects.filter(liked_by=request.user, liked_post=post).first()
        already_disliked = Dislikes.objects.filter(disliked_by=request.user, disliked_post=post).first()
        if not already_liked:
            if already_disliked:
                already_disliked.delete()
            like = Likes(liked_post=post, liked_by=request.user)
            like.save()
        else:
            already_liked.delete()
        data = {
            'total_likes': Likes.objects.filter(liked_post=post).count(),
            'total_dislikes': Dislikes.objects.filter(disliked_post=post).count()
        }
        return JsonResponse(data)
    return redirect('/')
    


def dislikes(request):
    if request.user.is_authenticated:
        disliked_post_id = request.GET.get('post', None)
        post = get_object_or_404(Post, pk=disliked_post_id)
        already_liked = Likes.objects.filter(liked_by=request.user, liked_post=post).first()
        already_disliked = Dislikes.objects.filter(disliked_by=request.user, disliked_post=post).first()
        if not already_disliked:
            if already_liked:
                already_liked.delete()
            dislike = Dislikes(disliked_post=post, disliked_by=request.user)
            dislike.save()
        else:
            already_disliked.delete()
        data = {
            'total_likes': Likes.objects.filter(liked_post=post).count(),
            'total_dislikes': Dislikes.objects.filter(disliked_post=post).count()
        }
        return JsonResponse(data)
    return redirect('/')

