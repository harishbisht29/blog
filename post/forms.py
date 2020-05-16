from django import forms
from tinymce import TinyMCE
from .models import Post, Comment

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostForm(forms.ModelForm):
    content = forms.CharField(
        required=False,
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    
    class Meta:
        model = Post
        fields = (
             
            'title','overview'\
            ,'content','feature_image'\
            ,'cover','thumbnail'\
            ,'thumbnail_small'
            ,'categories'\
            ,'next_post','previous_post',\
            'is_draft')  

class CommentForm(forms.ModelForm):

    content= forms.CharField(label='',widget= forms.Textarea(attrs={
        'class':  'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows':'4',
        
    }))
    email=  forms.EmailField( widget=forms.TextInput(
        attrs={'type':'email',
        'class':'form-control',
         'placeholder': 'email (will not be published)'}),label='')
    username= forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Name',
        'class':'form-control'}))
    class Meta:
        model= Comment
        fields = ('username', 'email', 'content', )