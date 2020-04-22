from django import template
from social.models import Like, Dislike, Follower, Comment

register = template.Library()

@register.simple_tag
def total_likes(post):
    return Like.objects.filter(liked_post=post).count()

@register.simple_tag
def total_dislikes(post):
    return Dislike.objects.filter(disliked_post=post).count()

@register.simple_tag
def total_followers(user):
    return Follower.objects.filter(user=user).count()
    
@register.simple_tag
def total_followed(user):
    return Follower.objects.filter(is_followed_by=user).count()

@register.simple_tag
def already_followed(user, followed_by):
    following = Follower.objects.filter(user=user, is_followed_by=followed_by)
    if following:
        return "Unfollow"
    else:
        return "Follow"

@register.simple_tag
def replies(in_reply_to_comment):
    return Comment.objects.filter(in_reply_to_comment=in_reply_to_comment)
