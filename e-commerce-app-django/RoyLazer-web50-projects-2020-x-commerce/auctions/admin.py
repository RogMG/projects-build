from django.contrib import admin
from .models import User, Products, Watchlist, comments, Categories
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username","email")

class ProductsAdmin(admin.ModelAdmin):
    list_display = ("id","name_product","image","bid","owner","last_user_bid","description","category","active")

class WatchAdmin(admin.ModelAdmin):
    list_display=("id","product_id","user_id")

class CommentsAdmin(admin.ModelAdmin):
    list_display=("id","user_id","product_id","comment")

class CategoriesAdmin(admin.ModelAdmin):
    list_display=("id","category_name")

admin.site.register(User, UserAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Watchlist, WatchAdmin)
admin.site.register(comments, CommentsAdmin)
admin.site.register(Categories,CategoriesAdmin)