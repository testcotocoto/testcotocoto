from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    # 他のURLパターンをここに追加する

    # ログイン関連のURLパターン
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('radar_chart/', views.radar_chart_view, name='radar_chart'),
    path('upload/', views.upload, name='upload'),
    path('result/', views.result, name='result'),
    path('about/', views.about, name='about'),  # 'about'のURLパターンを追加
    path('register/', views.register, name='register'),
    path('save-api-data/', views.save_api_data, name='save_api_data'),
    path('admin/', admin.site.urls),
    path('daily_emotion_scores/', views.daily_emotion_scores, name='daily_emotion_scores'),


    # 他のURLパターン
]

# 開発中のみ静的ファイルを提供する設定
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

