from django.contrib import admin
from .models import *

admin.site.register(GeneralsProducts)
admin.site.register(PaperProducts)
admin.site.register(Stationery) 
admin.site.register(StorageType)
admin.site.register(SubcategoryStationery)
admin.site.register(WritingMaterials)

@admin.register(CategoryBooks)
class CategoryBooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'category', 'subcategory')
    search_fields = ('id', 'book__book_id', 'category__category_id', 'subcategory__subcategory_id')


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'year_of_publication', 'book_id')
    search_fields = ('title', 'isbn', 'book_id')
    list_filter = ('year_of_publication', 'author') 

@admin.register(Authors)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_id')
    search_fields = ('name', 'author_id')

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'phone', 'email', 'user_id')
    search_fields = ('name', 'last_name', 'phone', 'email', 'user_id')
    list_filter = ('date_registered',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'apartment', 'entrance', 'floor', 'intercom', 'user', 'address_id')
    search_fields = ('city', 'street', 'apartment', 'entrance', 'floor', 'intercom', 'user__name', 'address_id')

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('basket_id', 'user', 'book', 'quantity')
    search_fields = ('basket_id', 'user', 'book', 'quantity')

@admin.register(BindingType)
class BindingTypeAdmin(admin.ModelAdmin):
    list_display = ('binding_type_id', 'name_binding_type')
    search_fields = ('binding_type_id', 'name_binding_type')

@admin.register(BookSeries)
class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ('book_series_id', 'name_book_series')
    search_fields = ('book_series_id', 'name_book_series')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name_category')
    search_fields = ('category_id', 'name_category')

@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'order_date', 'status')
    search_fields = ('order_id', 'user_id__name', 'order_date', 'status')
    list_filter = ('order_date', 'status')
    
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('reviews_id', 'user', 'book', 'rating', 'comment', 'review_date')
    search_fields = ('reviews_id', 'user', 'book')
    list_filter = ('rating', 'review_date')

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_detail_id', 'order', 'book', 'quantity', 'price')
    search_fields = ('order_detail_id', 'order', 'book')
    list_filter = ('quantity',)
    readonly_fields = ('price',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user_id', 'order', 'amount', 'payment_method', 'payment_date', 'transaction_id') 
    search_fields = ('payment_id', 'user_id', 'order', 'payment_date', 'transaction_id')
    list_filter = ('payment_date',)
    readonly_fields = ('amount',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher_id', 'name_publisher')
    search_fields = ('publisher_id', 'name_publisher')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_id', 'category', 'name_subcategory')
    search_fields = ('subcategory_id', 'category', 'name_subcategory')

@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('subscriptions_id', 'user', 'author', 'publisher')
    search_fields = ('subscriptions_id', 'user', 'author', 'publisher')

@admin.register(Wishlists)
class WishlistsAdmin(admin.ModelAdmin):
    list_display = ('wishlist_id', 'user', 'book')
    search_fields = ('wishlist_id', 'user', 'book')
