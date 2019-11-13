from .models import Comment, Post
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class PostForm(forms.ModelForm):
    # time_published = forms.DateTimeField(required=False,
    #                                      widget=AdminSplitDateTime(),
    #                                      label='Publication time',
    #                                      help_text=DATETIME_HELP_TEXT)

    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'author', 'slug', 'content', 'status']

    def save(self, commit=True, publish=False):
        instance = super(PostForm, self).save(commit=False)
        if publish and not instance.status == 1:
            instance.status = 1

        if commit:
            instance.save()

        return instance