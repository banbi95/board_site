from django import forms

from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'placeholder': '你在想什么？'}),
                              max_length=4000,
                              help_text='输入内容不超过4000个字符')

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': '在这里回复'}),
                              max_length=4000,

                              help_text='输入内容不超过4000个字符')
    class Meta:
        model = Post
        fields = ['message', ]
