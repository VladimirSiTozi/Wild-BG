from django.contrib import admin
from .models import Landmark, AdditionalLandmarkInfo, Review, Like, Visit


@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'location_name', 'level', 'user', 'created_at', 'updated_at')
    list_display_links = ('name',)
    search_fields = ('name', 'location_name', 'user__email')
    list_filter = ('level', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location_name', 'description', 'image', 'map_location')
        }),
        ('Details', {
            'fields': ('level', 'user', 'created_at', 'updated_at')
        }),
    )


@admin.register(AdditionalLandmarkInfo)
class AdditionalLandmarkInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'landmark', 'is_transition', 'is_accessible', 'distance_km', 'suitable_for_children')
    list_display_links = ('landmark',)
    search_fields = ('landmark__name',)
    list_filter = ('is_transition', 'is_accessible', 'suitable_for_children', 'has_eating_places', 'is_ennobled')
    fieldsets = (
        ('Basic Info', {
            'fields': ('landmark', 'is_transition', 'is_accessible', 'distance_km')
        }),
        ('Additional Details', {
            'fields': ('suitable_for_children', 'has_eating_places', 'is_ennobled', 'start_point', 'end_point',
                       'accessible_by_car', 'has_parking')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'landmark', 'rating', 'created_at')
    list_display_links = ('user',)
    search_fields = ('user__email', 'landmark__name')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Review Details', {
            'fields': ('user', 'landmark', 'rating', 'comment', 'created_at')
        }),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'landmark', 'created_at')
    list_display_links = ('user',)
    search_fields = ('user__email', 'landmark__name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Like Information', {
            'fields': ('user', 'landmark', 'created_at')
        }),
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'landmark', 'created_at')
    list_display_links = ('user',)
    search_fields = ('user__email', 'landmark__name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Visit Details', {
            'fields': ('user', 'landmark', 'created_at')
        }),
    )
