from django.urls import include, path

urlpatterns = [
    path("users/", include(("authapp.users.urls", "users"))),
]
