from django import forms
from taggit.models import Tag
from .models import Themes, Comments


class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label='店舗名')

    AVAILABLE_TAGS = ['しお', '醤油', '豚骨', '味噌', '魚介', '混ぜそば', '二郎系', 'あっさり', 'こってり', 'お気に入り']

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkbox'}),
        required=True,
        initial=Tag.objects.none()  # 修正①
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(name__in=self.AVAILABLE_TAGS)  # 修正②

    class Meta:
        model = Themes
        fields = ('title', 'tags')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # タグを手動で設定
        instance.tags.clear()  # すでに関連付けられているタグをクリア
        for tag in self.cleaned_data['tags']:
            instance.tags.add(tag)

        if commit:
            instance.save()

        return instance
    
class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    photo = forms.ImageField(required=False)

    class Meta:
        model = Comments
        fields = ('comment', 'photo')