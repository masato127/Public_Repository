from django.urls import path
from . import views
from .views import delete_comment
from .views import home, tagged_ramen_list
from django.contrib.auth.views import LoginView


app_name = 'boards'

urlpatterns = [
    path('create_theme', views.create_theme, name='create_theme'),
    path('list_themes', views.list_themes, name='list_themes'),
    path('edit_theme/<int:id>', views.edit_theme, name='edit_theme'),
    path('delete_theme/<int:id>', views.delete_theme, name='delete_theme'),
    path('post_comments/<int:theme_id>', views.post_comments, name='post_comments'),
    path('save_comment', views.save_comment, name='save_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('', home, name='home'),
    path('tag/<slug:tag_slug>/', views.tagged_ramen_list, name='tagged_ramen_list'),
    path('login/', LoginView.as_view(), name='login'),
] 
