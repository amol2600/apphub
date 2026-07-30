from django.urls import path
from . import views

urlpatterns = [
    path("", views.transaction_list, name="transaction_list"),

    path(
        "add/",
        views.add_transaction,
        name="add_transaction",
    ),

    path(
        "categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "categories/add/",
        views.add_category,
        name="add_category",
    ),

    path(
        "categories/edit/<int:id>/",
        views.edit_category,
        name="edit_category",
    ),

    path(
        "categories/delete/<int:id>/",
        views.delete_category,
        name="delete_category",
    ),

    path(
        "transactions/edit/<int:id>/",
        views.edit_transaction,
        name="edit_transaction",
    ),

    path(
        "transactions/delete/<int:id>/",
        views.delete_transaction,
        name="delete_transaction",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
]