from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# You can extend these in the future if you want custom login responses:
LoginView = TokenObtainPairView.as_view()
RefreshTokenView = TokenRefreshView.as_view()
