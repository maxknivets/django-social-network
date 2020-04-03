from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from social.models import Post

class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField()

class PostForm(forms.Form):
    post_text = forms.CharField(min_length=1, max_length=200, widget=forms.Textarea(attrs={'placeholder': 'How was your day?', 'id': 'post-field', 'class':'postinput'}))
    post_image = forms.ImageField(required=False)

class EditForm(forms.Form):
    id = forms.IntegerField(widget=forms.Textarea(attrs={'id': 'edit-id'}))
    new_text = forms.CharField(min_length=1, max_length=200, widget=forms.Textarea(attrs={'placeholder': 'Edit your mishaps here', 'id': 'edit-field'})) # TODO

class DeleteForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'delete-id'}))

class CommentForm(forms.Form):
    comment = forms.CharField(min_length=1, max_length=200, widget=forms.Textarea(attrs={'placeholder': 'What do you think?', 'id': 'comment-field'}), label='')
    id = forms.IntegerField(widget=forms.HiddenInput())
    in_reply_to_user = forms.IntegerField(widget=forms.HiddenInput())
    in_reply_to_comment = forms.IntegerField(widget=forms.HiddenInput())

class ChangeForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={'placeholder': 'Your first name', 'id': 'first-name-field'}))
    last_name = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={'placeholder': 'Your last name', 'id': 'last-name-field'}))
    bio = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={'placeholder': 'Everyone likes reading a good bio', 'id': 'bio-field'}))
    location = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={'placeholder': 'Your location', 'id': 'location-field'}))

class PFPForm(forms.Form):
    profile_picture = forms.ImageField()
    

