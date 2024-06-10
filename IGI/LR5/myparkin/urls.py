from django.urls import path
from . import views
from .views import news_list
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path(r'', views.index, name='index'),
     path('register/', views.registration_view, name='register'),
     path('register_s/', views.seller, name='register_s'),
     path('register_c/', views.customer, name='register_c'),

     path('parking_list/', views.parking_list, name='parking_list'),
     path('delete_park/<int:park_id>/', views.delete_park, name='delete_park'),
     path('my_parking_list/', views.my_parking_list, name='my_parking_list'),
     path('rent_parking/<int:id>/', views.rent_parking, name='rent_parking'),

     path('my_cars/', views.my_cars, name='my_cars'),
     path('add_car/', views.add_car, name='add_car'),
     path('delete_car/<int:id>/', views.delete_car, name='delete_car'),

     # Пути для перехода к списку машин на паркинге (status = add/del)
     path('car_in_park/<int:park_id>/<slug:status>/',views.car_in_park, name='car_in_park'),
     path('pay/<int:payment_id>/', views.pay_payment, name='pay_payment'),
     # Пути для перехода к действиям с авто из паркинга ("На паркинг", "С паркинга")
     path('interaction_car_for_parking/<int:car_id>/<int:park_id>/<slug:status>/',views.interaction_car_for_parking, name='interaction_car_for_parking'),
     path('parking-information/', views.parking_information, name='parking_information'),
     #  Payments
     path('my_payments/',views.my_payments, name='my_payments'),
     path('payment_paid/<int:payment_id>/',views.payment_paid, name='payment_paid'),
     path('update_payments/',views.update_payments, name='update_payments'),

     #api
     path('get_ip/',views.get_ip, name='get_ip'),
     path('get_fact_about_cats/',views.get_fact_about_cats, name='get_fact_about_cats'),


     path('news_list/', news_list, name='news_list'),
     path('faq/', views.faq, name='faq'),
     path('promo/', views.promocodes, name='promocodes'),
     path('vacancy/', views.vacancy, name='vacancy'),
     path('contacts/', views.contacts, name='contacts'),
     path('retings/', views.ratings, name='ratings'),
     path('about/', views.about, name='about'),
     path('add_feedback/', views.add_feedback, name='add_feedback'),
     path('conf/', views.conf, name='conf'),
     path('parking_spot/new/', views.create_parking_spot, name='create_parking_spot'),
     path('parking_spot/<int:pk>/edit/', views.edit_parking_spot, name='edit_parking_spot'),
     path('parking_spot/<int:pk>/delete/', views.delete_parking_spot, name='delete_parking_spot'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
