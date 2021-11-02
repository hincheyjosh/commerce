from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("watchlist", views.watchlist, name='watchlist'),
    path("addWatchlist<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist<int:listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("closeAuction<int:listing_id>", views.closeAuction, name="closeAuction"),
    path("categories", views.categories, name="categories"),
    path("<str:category>", views.category, name="category"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
