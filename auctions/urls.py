from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("categories", views.categories, name="categories"),
    path("<str:c>", views.categorie_page, name="categorie_page"),
]
