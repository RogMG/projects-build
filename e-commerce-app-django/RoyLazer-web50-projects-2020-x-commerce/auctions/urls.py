from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('watchlist', views.watchlist, name = "watchlist"),
    path("create", views.create_view, name="createlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.filter, name="category"),
    path("listings/<str:product_id>", views.listings, name="listing"),
    path("new<str:product_id>", views.newBid, name="newBid"),
    path("comment<str:product_id>", views.newComment, name="newComment"),
    path("active<str:product_id>", views.active, name="active")
]

