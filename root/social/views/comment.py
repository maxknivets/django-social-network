from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import escape
from social.models import User, Like, Dislike, Comment, Post
from social.forms import Edit_form, Delete_form, Comment_form

@login_required
def view_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    replies = Comment.objects.filter(in_reply_to_comment=comment_id)
    return render(request, 'social/singlecomment.html', {
        'request-user': request.user,
        'comment':comment,
        'post':comment.post,
        'editform':Edit_form(),
        'commentform':Comment_form()
    })

@login_required
@require_http_methods(["POST"])
def comment(request):
    form = Comment_form(request.POST)
    if form.is_valid():
        post_id = form.cleaned_data.get('id')
        post = get_object_or_404(Post, pk=post_id)
        
        comment = form.cleaned_data.get('comment')
        in_reply_to_user = form.cleaned_data.get('in_reply_to_user')
        in_reply_to_comment = form.cleaned_data.get('in_reply_to_comment')
        date = timezone.now()
        data = {}
        new_comment = Comment(comment=comment, post_date=date, posted_by=request.user, post=post)
        
        if in_reply_to_user and in_reply_to_comment:
            new_comment.in_reply_to_user=in_reply_to_user
            new_comment.in_reply_to_comment=in_reply_to_comment
            data['in_reply_to_user']=in_reply_to_user
            data['in_reply_to_comment']=in_reply_to_comment
            data['get_username']=new_comment.get_user().username
        else:
            data['in_reply_to_user']=None
            data['in_reply_to_comment']=None
        
        new_comment.save()
        
        data['post_id']=post_id
        data['comment_text']=escape(new_comment.comment)
        data['comment_pk']=new_comment.pk
        data['posted_by']=new_comment.posted_by.username
        data['user_id']=new_comment.posted_by.pk
        data['date']=new_comment.get_readable_date()
        
        return JsonResponse(data)
    return redirect('/')

@login_required
@require_http_methods(["POST"])
def commentedit(request):
    form = Edit_form(request.POST)
    if form.is_valid():
        comment_id = form.cleaned_data.get('id')
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.posted_by:
            new_text = form.cleaned_data.get('new_text')
            comment.comment = new_text
            comment.save()
            data = { 'new_text': escape(new_text) }
            return JsonResponse(data)
    return redirect('/')

@login_required
def commentdelete(request):
    comment_id = request.GET.get('id')
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.posted_by:
        comment.delete()
        data = { 'comment_id': comment_id }
        return JsonResponse(data)
    return redirect('/')

@login_required
def getcommentinfo(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    data = {}
    if comment.in_reply_to_user and comment.in_reply_to_comment:
        data['in_reply_to_user']=comment.in_reply_to_user
        data['in_reply_to_comment']=comment.in_reply_to_comment
        data['get_username']=comment.get_user().username
    else:
        data['in_reply_to_user']=None
        data['in_reply_to_comment']=None
    data['request_user_id']=request.user.pk
    data['post_id']=comment.post.pk
    data['comment_text']=escape(comment.comment)
    data['comment_pk']=comment.pk
    data['posted_by']=comment.posted_by.username
    data['user_id']=comment.posted_by.pk
    data['date']=comment.get_readable_date()
    return JsonResponse(data)

@login_required
def commentdatabasecheck(request, comment_id):
    data={'currentId':Comment.objects.last().pk, 'lastId':comment_id}
    return JsonResponse(data)