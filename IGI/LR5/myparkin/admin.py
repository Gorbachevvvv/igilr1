from django.contrib import admin

from .models import *


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'mark', 'model', 'license_plate',)
    list_filter = ('owner', 'mark', 'model', 'license_plate',)


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('number', 'price', 'is_busy')
    list_filter = ('number', 'price', 'is_busy')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'park', 'amount', 'receipt_date', 'is_paid', 'repayment_date')
    list_filter = ('receipt_date', 'is_paid', 'repayment_date', 'amount')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')
    list_filter = ('amount', 'user')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_label', 'news', 'newsimg', )
    search_field = ('news_label',)

admin.site.register(Feedbacks)
admin.site.register(About)
admin.site.register(FAQ)
admin.site.register(Contacts)
admin.site.register(Vacancies)
admin.site.register(Promocodes)