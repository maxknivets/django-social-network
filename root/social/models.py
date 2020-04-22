from django.db import models
from django.contrib.auth.models import User
# class User attributes (https://docs.djangoproject.com/en/2.0/ref/contrib/auth/)
# username,  first_name, last_name, email, password, groups, user_permissions, is_staff, is_active, is_superuser, last_login, date_joined

class Post(models.Model):
    post_text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Publication Date')
    image = models.ImageField(upload_to='post-images', blank=True)
    
    def info(self):
        return 'Post Text: %s \nPosted By: %s\nPublished At: %s' % (self.post_text, self.user, self.pub_date)
    
    def get_readable_date(self):
        return self.pub_date.strftime("%B %d, %Y")
    
    def __str__(self):
        return self.post_text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100,blank=True)
    profile_picture = models.ImageField(upload_to="profile-pictures", blank=True)
    
    def __str__(self):
        return str(self.user)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    is_followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed_by')

    def follows(self, user):
        return Followers.objects.filter(is_followed_by=user)
        
    def followers(self, user):
        followers_list = Followers.objects.filter(user=user).exclude(is_followed_by=user)
        
    def __str__(self):
        return str(self.user)

class Like(models.Model):
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.liked_by)

class Dislike(models.Model):
    disliked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    disliked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.disliked_by)

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    post_date = models.DateTimeField('Publication Date')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    in_reply_to_comment = models.IntegerField(blank=True, null=True)
    in_reply_to_user = models.IntegerField(blank=True, null=True)
    
    def get_readable_date(self):
        return self.post_date.strftime("%l:%M%p on %B %d, %Y")
    
    def get_comment(self):
        return Comment.objects.filter(pk=self.in_reply_to_comment).first()
    
    def get_user(self):
        return User.objects.filter(pk=self.in_reply_to_user).first()
    
    def __str__(self):
        return self.comment