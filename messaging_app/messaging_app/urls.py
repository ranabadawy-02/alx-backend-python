from django.contrib import admin
from django.urls import path, include
from messaging_app.chats.auth import LoginView, RefreshTokenView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/auth/login/', LoginView, name='login'),
    path('api/auth/refresh/', RefreshTokenView, name='token_refresh'),

    # Chats API
    path('api/chats/', include('messaging_app.chats.urls')),
]
