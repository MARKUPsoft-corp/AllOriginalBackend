from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, ProductSpecification, SpecificationType, Review, ReviewImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary', 'alt_text')

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = ('name', 'spec_type', 'value', 'is_highlighted', 'display_order')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'price_display', 'promotion_display', 'category', 'stock_status', 'is_featured', 'is_active')
    list_filter = ('brand', 'status', 'category', 'is_featured', 'is_active')
    search_fields = ('name', 'brand', 'model', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'promo', 'discounted_price', 'in_stock')
    inlines = [ProductImageInline, ProductSpecificationInline]
    list_editable = ('price', 'is_featured', 'is_active')
    list_per_page = 20
    
    def price_display(self, obj):
        if obj.promo:
            return format_html('<span style="text-decoration: line-through;">{}</span> <strong style="color: green;">{}</strong>', 
                              f"{obj.original_price} FCFA", f"{obj.price} FCFA")
        return f"{obj.price} FCFA"
    price_display.short_description = "Prix"
    price_display.admin_order_field = 'price'
    
    def promotion_display(self, obj):
        if obj.promo:
            discount = round((1 - (obj.price / obj.original_price)) * 100)
            return format_html('<span class="badge badge-success">-{}%</span>', discount)
        return "-"
    promotion_display.short_description = "Promo"
    
    def stock_status(self, obj):
        if obj.in_stock:
            return format_html('<span style="color: green;">✓ En stock</span>')
        return format_html('<span style="color: red;">✗ Indisponible</span>')
    stock_status.short_description = "Disponibilité"
    stock_status.admin_order_field = 'status'
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Informations produit', {
            'fields': ('brand', 'model')
        }),
        ('Prix et promotions', {
            'fields': ('price', 'original_price'),
            'description': 'Si le prix original est supérieur au prix actuel, le produit est considéré comme en promotion.'
        }),
        ('Disponibilité', {
            'fields': ('status',),
            'description': 'Le statut "En stock" indique que le produit est disponible.'
        }),
        ('Options', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('is_primary',)

@admin.register(SpecificationType)
class SpecificationTypeAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'description')
    search_fields = ('name', 'display_name', 'description')
    list_per_page = 20
    ordering = ('display_name',)

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value', 'is_highlighted', 'display_order')
    list_filter = ('name', 'is_highlighted')
    search_fields = ('product__name', 'name', 'value')
    list_editable = ('is_highlighted', 'display_order')


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'author_name', 'rating_stars', 'title', 'created_at', 'is_verified', 'is_approved')
    list_filter = ('rating', 'is_verified', 'is_approved', 'created_at')
    search_fields = ('product__name', 'author_name', 'author_email', 'title', 'comment')
    list_editable = ('is_verified', 'is_approved')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReviewImageInline]
    list_per_page = 20
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #FFD700;">{}</span>', stars)
    rating_stars.short_description = 'Note'
    rating_stars.admin_order_field = 'rating'
