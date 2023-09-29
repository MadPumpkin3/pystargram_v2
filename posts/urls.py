from django.urls import path
from posts.views import feeds, comment_add, comment_delete, post_add

urlpatterns = [
    path("feeds/", feeds),
    path("comment_add/", comment_add),
    path("comment_delete/<int:comment_id>/", comment_delete),
    path("post_add/", post_add),
]
