from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("close/<int:auction_id>", views.close, name="close"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("categories/", views.categories, name="categories"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("toggle_watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
]
