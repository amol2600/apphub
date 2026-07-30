from django.contrib import admin
from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "amount",
        "transaction_type",
        "category",
        "transaction_date",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "transaction_type",
        "category",
        "transaction_date",
    )

    ordering = ("-transaction_date",)
