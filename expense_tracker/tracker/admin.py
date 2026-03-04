from django.contrib import admin
from .models import Category, Transaction

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'type', 'category', 'date', 'description')
    list_filter = ('type', 'category', 'date', 'user')
    search_fields = ('description', 'user__username', 'category__name')
    date_hierarchy = 'date'
