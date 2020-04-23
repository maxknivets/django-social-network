from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import escape
from social.models import User, Post, Like, Dislike
from social.forms import Post_form, Edit_form, Delete_form

def post(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = Post_form(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('post_text')
            image = request.FILES.get('post_image')
            date = timezone.now()            
            post = Post(post_text=text, user=request.user, pub_date=date)
            if image:
                post = Post(post_text=text, user=request.user, pub_date=date, image=image)
            post.save()

            data = {}
            data['post_image'] = None
            if image:
                data['post_image'] = post.image.url
            data['post_text'] = escape(post.post_text)
            data['post_date'] = post.get_readable_date()
            data['post_id'] = post.pk
            data['user_id'] = request.user.pk
            data['username'] = request.user.username
            return JsonResponse(data)
        return redirect('/')

def databasecheck(request, post_id):
    if request.user.is_authenticated:
        data={'currentId':Post.objects.last().pk, 'lastId':post_id}
        return JsonResponse(data)
    return redirect('/')

def getpostinfo(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        data={
            'post_text': escape(post.post_text),
            'post_date': post.get_readable_date(),
            'post_id': post.pk,
            'request_user_id': request.user.pk,
            'user_id': post.user.pk,
            'username': post.user.username,
        }
        if post.image:
        	data['post_image'] = post.image.url
        return JsonResponse(data)
    return redirect('/')

def view_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'social/single_post.html',{'post':post, 'replies':replies, 'post':comment.post, 'editform':Edit_form(), 'commentform':Comment_form()})
    return redirect('/')

def edit(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = Edit_form(request.POST)
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

def like(request):
    if request.user.is_authenticated:
        liked_post_id = request.GET.get('post', None)
        post = get_object_or_404(Post, pk=liked_post_id)
        already_liked = Like.objects.filter(liked_by=request.user, liked_post=post).first()
        already_disliked = Dislike.objects.filter(disliked_by=request.user, disliked_post=post).first()
        if not already_liked:
            if already_disliked:
                already_disliked.delete()
            like = Like(liked_post=post, liked_by=request.user)
            like.save()
        else:
            already_liked.delete()
        data = {
            'total_likes': Like.objects.filter(liked_post=post).count(),
            'total_dislikes': Dislike.objects.filter(disliked_post=post).count()
        }
        return JsonResponse(data)
    return redirect('/')

def dislike(request):
    if request.user.is_authenticated:
        disliked_post_id = request.GET.get('post', None)
        post = get_object_or_404(Post, pk=disliked_post_id)
        already_liked = Like.objects.filter(liked_by=request.user, liked_post=post).first()
        already_disliked = Dislike.objects.filter(disliked_by=request.user, disliked_post=post).first()
        if not already_disliked:
            if already_liked:
                already_liked.delete()
            dislike = Dislike(disliked_post=post, disliked_by=request.user)
            dislike.save()
        else:
            already_disliked.delete()
        data = {
            'total_likes': Like.objects.filter(liked_post=post).count(),
            'total_dislikes': Dislike.objects.filter(disliked_post=post).count()
        }
        return JsonResponse(data)
    return redirect('/')