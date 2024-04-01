from django.shortcuts import render, redirect, get_object_or_404
from  . import forms
from django.contrib import messages
from .models import Themes, Comments
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import logging
from taggit.models import Tag
from django.contrib.auth.models import AnonymousUser
from .forms import CreateThemeForm

logger = logging.getLogger(__name__)

# Create your views here.
def create_theme(request):
    if request.method == 'POST':
        create_theme_form = CreateThemeForm(request.POST)
        if create_theme_form.is_valid():
            if request.user.is_authenticated:
                create_theme_form.instance.user = request.user
                theme = create_theme_form.save(commit=False)
                theme.save()  # データベースに保存
                create_theme_form.save_m2m()
                messages.success(request, '掲示板を作成しました.')
                return redirect('boards:list_themes')
            else:
                messages.warning(request, 'ログインが必要です.')
                return redirect('boards:login')
    else:
        create_theme_form = CreateThemeForm()

    return render(request, 'boards/create_theme.html', context={'create_theme_form': create_theme_form})

def list_themes(request):
    themes = Themes.objects.fetch_all_themes()
    return render(
        request, 'boards/list_themes.html', context={
            'themes': themes
        }
    )


def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '掲示板を更新しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'id':id,
        }
    )

def delete_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid(): # csrf check
        theme.delete()
        messages.success(request, '掲示板を削除しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/delete_theme.html', context={
            'delete_theme_form': delete_theme_form,
        }
    )


def post_comments(request, theme_id):
    saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
    post_comment_form = forms.PostCommentForm(request.POST or None, initial={'comment': saved_comment})
    theme = get_object_or_404(Themes, id=theme_id)
    comments = Comments.objects.fetch_by_theme_id(theme_id)
    if post_comment_form.is_valid():
        if not request.user.is_authenticated:
            raise Http404
        post_comment_form.instance.theme = theme
        post_comment_form.instance.user = request.user
        post_comment_form.save()
        cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')
        return redirect('boards:post_comments', theme_id=theme_id)
    return render(
        request, 'boards/post_comments.html', context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )

def save_comment(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment = request.GET.get('comment')
        theme_id = request.GET.get('theme_id')
        if comment and theme_id:
            cache.set(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', comment)
            return JsonResponse({'message': '一時保存しました'})

@csrf_protect
@login_required        
def delete_comment(request, comment_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            comment = get_object_or_404(Comments, id=comment_id, user=request.user)
            comment.delete()
            return JsonResponse({'message': 'コメントを削除しました'})
        except Comments.DoesNotExist as e:
            return JsonResponse({'message': 'コメントが見つかりませんでした'}, status=404)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'message': '予期しないエラーが発生しました'}, status=500)
    else:
        # Handle non-Ajax requests (optional, you can redirect or return an HTML response)
        return JsonResponse({'message': 'このエンドポイントはAjaxリクエストのみ受け付けます'}, status=400)


def home(request):
    tags_to_display = ['しお', '醤油', '豚骨', '味噌', '魚介', '混ぜそば', '二郎系', 'こってり', 'あっさり', 'お気に入り']
    tags = Tag.objects.filter(name__in=tags_to_display)
    context = {'tags': tags}
    return render(request, 'home.html', context)

def tagged_ramen_list(request, tag_slug):

    print(f"Received tag_slug: {tag_slug}")

    # タグの slug から Tag オブジェクトを取得
    tag = get_object_or_404(Tag, slug=tag_slug)
    
    # タグに関連する Themes オブジェクトを取得
    themes = Themes.objects.filter(tags=tag)

    # テンプレートに渡すコンテキスト
    context = {'tag': tag, 'themes': themes}

    # テンプレートをレンダリングしてレスポンスを返す
    if themes.exists():
        return render(request, 'boards/tagged_ramen_list.html', context)
    else:
        return render(request, 'boards/no_posts.html', context)
    

def create_theme_view(request):
    if request.method == 'POST':
        form = CreateThemeForm(request.POST)
        if form.is_valid():
            theme = form.save()
            # フォームの保存が成功した場合の処理
            return redirect('boards:home')  # 例としてホーム画面にリダイレクト
    else:
        form = CreateThemeForm()

    return render(request, 'create_theme.html', {'create_theme_form': form})