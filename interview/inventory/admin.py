from django.contrib import admin
from .models import Inventory, InventoryTag, InventoryLanguage, InventoryType


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'language', 'created_at', 'updated_at')
    list_filter = ('name', 'type', 'language', 'created_at', 'updated_at')
    search_fields = ('name', 'tags__name')
    filter_horizontal = ('tags',)


@admin.register(InventoryTag)
class InventoryTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(InventoryLanguage)
class InventoryLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(InventoryType)
class InventoryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
