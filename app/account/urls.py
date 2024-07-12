from rest_framework import routers
from django.urls import path

from account.views.auth import LoginView, LoginRefreshView, LogoutView, RegisterView

router = routers.SimpleRouter()

urlpatterns = router.urls + [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', LoginRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]