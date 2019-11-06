from .models import Comment, Post
from django import forms
from markdownx.fields import MarkdownxFormField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


MARKDOWN_HELP_TEXT = """
Please use
<a href="http://daringfireball.net/projects/markdown/syntax">Markdown</a>.
Examples:
<br>
*italic*, **bold**, - bulleted, 1. numbered
<br>
&lt;http://google.com&gt;
<br>
[click here](http://google.com)
<br>
![squirrel](http://squirrel.jpg)
<br>
![squirrel](http://squirrel.jpg "My Pet Squirrel")
"""


class PostForm(forms.ModelForm):
    # time_published = forms.DateTimeField(required=False,
    #                                      widget=AdminSplitDateTime(),
    #                                      label='Publication time',
    #                                      help_text=DATETIME_HELP_TEXT)

    # content = forms.CharField(
    #     widget=forms.Textarea(attrs={'rows': '24', 'cols': '80'}),
    #     help_text=MARKDOWN_HELP_TEXT)

    body = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ['title', 'author', 'slug', 'body', 'status']

    def save(self, commit=True, publish=False):
        instance = super(PostForm, self).save(commit=False)
        if publish and not instance.status == 1:
            instance.status = 1

        if commit:
            instance.save()

        return instance