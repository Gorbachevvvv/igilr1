import urllib
from datetime import datetime, timedelta
from django.utils import timezone
import mpld3 as mpld3
import pytz
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .context_processors import is_seller
from .forms import *
from .models import *

import matplotlib.pyplot as plt

import logging

logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format='%(asctime)s, %(levelname)s, %(message)s')




def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    latest_news = News.objects.latest('date')
    user_tz = request.session.get('user_tz', 'UTC')
    current_time = timezone.now().astimezone(pytz.timezone(user_tz))

    # Получение всех парковочных мест и их количества
    parkings = ParkingSpot.objects.all()
    parkings_count = parkings.count()

    # Создание графика
    fig, ax = plt.subplots()
    prices = [parking.price for parking in parkings]
    numbers = [parking.number for parking in parkings]

    ax.bar(numbers, prices)
    ax.set_xlabel('Parking Spot Number')
    ax.set_ylabel('Price')
    ax.set_title('Parking Spot Prices')

    # Преобразование графика в HTML-код с помощью mpld3
    graph_html = mpld3.fig_to_html(fig)

    return render(
        request,
        'index.html',
        context={
            'parkings': parkings,
            'parkings_count': parkings_count,
            'graph': graph_html,
            'user_tz': user_tz,
            'latest_news':latest_news,
            'current_time': current_time
        },
    )


def customer(request):
    error = ''
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Create a new user
            user = User.objects.create_user(username=username, password=password)

            # Create a new account for the user
            account = Account.objects.create(user=user, amount=0)

            # Create a new customer and associate it with the user and account
            cust = form.save(commit=False)
            cust.user = user
            cust.account = account
            cust.save()

            return redirect('index')
        else:
            error = 'Неверное заполнение'
    else:
        form = CustomerForm()
    data = {'error': error, 'form': form}
    return render(request, 'registration.html', data)
def seller(request):
    error = ''
    if request.method == "POST":
        form = SellerForm(request.POST)
        if form.is_valid():
            sell = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            sell.user = user
            sell.save()
            return redirect('index')
        else:
            error = 'Вам должно быть 18 лет'
    form = SellerForm()
    data = {'error': error, 'form': form}
    return render(request, 'registration.html', data)


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'index.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def parking_list(request):
    filter_busy = request.GET.get('busy')
    filter_min_price = request.GET.get('min_price')
    filter_max_price = request.GET.get('max_price')

    parkings = ParkingSpot.objects.all()

    if filter_busy == 'busy':
        parkings = parkings.filter(is_busy=True)
    elif filter_busy == 'free':
        parkings = parkings.filter(is_busy=False)

    if filter_min_price:
        parkings = parkings.filter(price__gte=float(filter_min_price))
    if filter_max_price:
        parkings = parkings.filter(price__lte=float(filter_max_price))

    parkings_count = parkings.count()

    return render(
        request,
        'myparking/parking_list.html',
        context={'parkings': parkings, 'parkings_count': parkings_count, },
    )


def rent_parking(request, id):
    parking = get_object_or_404(ParkingSpot, id=id)
    user = request.user

    if request.method == 'POST':
        # Присвоение парковочного места пользователю

        user.parkings.add(parking)
        сurrent_date = datetime.now()
        payment = Payment(owner=user,
                          park=parking,
                          amount=parking.price,
                          receipt_date=сurrent_date,
                          receipt_time=сurrent_date.time())
        payment.save()
        user.payments.add(payment)
        parking.is_busy = True
        parking.date_of_rent = сurrent_date
        parking.save()
        return redirect('parking_list')  # Перенаправление на список парковочных мест

    return render(
        request,
        'myparking/rent_parking.html',
        context={'parking': parking, },
    )


def my_parking_list(request):
    user = request.user
    parkings = user.parkings.all()
    parkings_count = parkings.count()

    return render(
        request,
        'myparking/my_parking_list.html',
        context={'parkings': parkings, 'parkings_count': parkings_count, },
    )


def my_cars(request):
    user = request.user
    cars = user.cars.all()
    cars_count = cars.count()

    return render(
        request,
        'myparking/my_cars.html',
        context={'cars': cars, 'cars_count': cars_count, },
    )


def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user  # Установка владельца
            car.save()
            cars = request.user.cars.all()
            return render(request,
                          'myparking/my_cars.html',
                          context={'cars': cars, 'cars_count': cars.count(), }, )
    else:
        form = CarForm()

    return render(request, 'myparking/add_car.html', {'form': form})


def delete_car(request, id):
    try:
        Car.objects.filter(id=id).delete()
    except Exception as e:
        print(f"Удаление не получилось. Код ошибки {str(e)}")
    return redirect('my_cars')


def car_in_park(request, park_id, status):
    parking = get_object_or_404(ParkingSpot, id=park_id)

    if status == 'add':
        user_cars = request.user.cars.all()
        parking_cars = parking.cars.all()
        cars_to_add = user_cars.difference(parking_cars)
    if status == 'del':
        cars_to_add = parking.cars.all()

    return render(
        request,
        'myparking/car_list_for_park.html',
        context={'parking': parking, 'cars': cars_to_add,
                 'cars_count': cars_to_add.count(), 'status': status},
    )


def interaction_car_for_parking(request, car_id, park_id, status):
    car = get_object_or_404(Car, id=car_id)
    parking = get_object_or_404(ParkingSpot, id=park_id)
    try:
        if status == 'add':
            parking.cars.add(car)
        if status == 'del':
            parking.cars.remove(car)
    except Exception as e:
        print(f"Код ошибки {str(e)}")
    return redirect('my_parking_list')


def delete_park(request, park_id):
    parking = get_object_or_404(ParkingSpot, id=park_id)
    user = request.user
    try:
        for payment in user.payments.filter(park_id=park_id):
            if not payment.is_paid:
                return render(request, 'myparking/not_all_payments_paid.html')
        parking.is_busy = False
        parking.save()
        user.parkings.remove(parking)

    except Exception as e:
        print(f"Код ошибки {str(e)}")
    return redirect('my_parking_list')


def my_payments(request):
    user = request.user
    payments = user.payments.all()

    payments = payments.order_by('-id')
    payments_count = payments.count()

    # Создание массива, для вычисления, сколько дней осталось до погашения платежей
    datetimes = [datetime.combine(payment.receipt_date, payment.receipt_time) for payment in payments]
    time_to_repay_the_payment = timedelta(weeks=1)
    # time_to_repay_the_payment = timedelta(seconds=20)
    current_datetime = datetime.now()
    zero_timedelta = timedelta(0)
    datetimes_for_repay_the_payment = [
        dt + time_to_repay_the_payment - current_datetime
        if dt + time_to_repay_the_payment - current_datetime >= zero_timedelta else 0
        for dt in datetimes
    ]

    return render(
        request,
        'myparking/my_payments.html',
        context={'payments': payments,
                 'payments_count': payments_count,
                 'datetimes_for_repay_the_payment': datetimes_for_repay_the_payment},
    )


def payment_paid(request, payment_id):
    user = request.user
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':
        account = get_object_or_404(Account, user=user)

        if account.amount < payment.amount:
            return render(request, 'myparking/not_enough_money_for_paid.html')

        payment.repayment_date = datetime.now()
        payment.repayment_time = payment.repayment_date.time()
        payment.is_paid = True
        payment.save()

        account.amount -= payment.amount
        account.save()
        return redirect('my_payments')

    return render(
        request,
        'myparking/payment_paid.html',
        context={'payment': payment, },
    )


def update_payments(request):
    user = request.user
    payments = user.payments.all()
    current_date = datetime.now()
    # time_to_repeat_the_payment = timedelta(weeks=4)
    time_to_repeat_the_payment = timedelta(days=1)
    for park in user.parkings.all():
        print(park.date_of_rent)
        print(time_to_repeat_the_payment)
        print(park.date_of_rent + time_to_repeat_the_payment)

        if park.date_of_rent + time_to_repeat_the_payment <= current_date.date():
            new_payment = Payment(owner=user,
                                  park=park,
                                  amount=park.price,
                                  receipt_date=current_date,
                                  receipt_time=current_date.time())
            new_payment.save()
            user.payments.add(new_payment)
            park.date_of_rent = current_date
            park.save()
    return redirect('my_payments')


def get_ip(request):
    url = f'https://api.ipify.org?format=json'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return render(request, 'myparking/get_ip.html',
                      {'ip': data['ip'], })
    else:
        error_message = f"Error: {response.status_code}"
        return render(request, 'myparking/get_ip.html',
                      {'error_message': error_message})


def get_fact_about_cats(request):
    url = f'https://catfact.ninja/fact'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return render(request, 'myparking/get_fact_about_cats.html',
                      {'fact': data['fact'], })
    else:
        error_message = f"Error: {response.status_code}"
        return render(request, 'myparking/get_fact_about_cats.html',
                      {'error_message': error_message})

def news_list(request):
    items = News.objects.all()
    return render(request, 'myparking/news_list.html', {'items': items})

@login_required
def pay_payment(request, payment_id):
    try:
        payment = Payment.objects.get(pk=payment_id)
    except Payment.DoesNotExist:
        return redirect('my_payments')

    # Проверка, что платеж уже оплачен
    if payment.is_paid:
        return redirect('my_payments')

    user = request.user

    # Проверка наличия аккаунта у пользователя
    try:
        account = user.account
    except Account.DoesNotExist:
        return redirect('my_payments')

    # Применение промокода автоматически, если он существует
    discount = 0
    try:
        promo = Promocodes.objects.filter(work=True).first()
        if promo:
            discount = promo.about
    except Promocodes.DoesNotExist:
        pass  # Нет действующих промокодов

    # Расчет окончательной суммы после применения скидки
    final_amount = max(payment.amount - discount, 0)

    # Проверка достаточности средств на счету пользователя
    if account.amount < final_amount:
        return redirect('my_payments')

    # Списание суммы платежа со счета пользователя
    account.amount -= final_amount
    account.save()

    # Обновление статуса платежа и даты/времени оплаты
    payment.is_paid = True
    payment.repayment_date = datetime.now().date()
    payment.repayment_time = datetime.now().time()
    payment.save()

    return redirect('my_payments')
@login_required
def parking_information(request):
    if not is_seller:
        return HttpResponseForbidden("You don't have permission to access this page.")

    parking_spots = ParkingSpot.objects.all()

    context = {
        'parking_spots': parking_spots
    }

    return render(request, 'myparking/parking_information.html', context)

def faq(request):
    faq = FAQ.objects.all()
    return render(request, 'myparking/faq.html', {'faq': faq})


def contacts(request):
    try:
        contacts = Contacts.objects.all()
        logging.info('Successfully retrieved contacts')
    except:
        logging.info('Error')
    return render(request, 'myparking/contacts.html', {'contacts': contacts})


def promocodes(request):
    promocodes = Promocodes.objects.all()
    logging.info('Successfully promocodes')
    return render(request, 'myparking/promocodes.html', {'promocodes': promocodes})

def about(request):
    info=About.objects.all()
    logging.info('Successfully about')
    return render(request, 'myparking/about.html', {'info':info})
def vacancy(request):
    vacancy = Vacancies.objects.all()
    logging.info('Successfully vacancy')
    return render(request, 'myparking/vacancy.html', {'vacancy': vacancy})

def conf(request):
    logging.info('Successfully conf')
    return render(request, 'myparking/conf.html')

def ratings(request):
    feedbacks = Feedbacks.objects.all
    return render(request, 'myparking/feedbacks.html', {'feedbacks': feedbacks})

@login_required
def add_feedback(request):
    error = ''
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.name = request.user.username
            feedback.save()
            return redirect('ratings')
        else:
            error = 'Неверное заполнение'
    form = FeedbackForm()
    data = {'error': error, 'form': form}
    return render(request, 'myparking/add_feedback.html', data)

@login_required
def create_parking_spot(request):
        if request.method == 'POST':
            form = ParkingSpotForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('parking_list')
        else:
            form = ParkingSpotForm()
        return render(request, 'myparking/create_parking_spot.html', {'form': form})


@login_required
def edit_parking_spot(request, pk):
    parking_spot = get_object_or_404(ParkingSpot, pk=pk)
    if request.method == 'POST':
        form = ParkingSpotForm(request.POST, instance=parking_spot)
        if form.is_valid():
            form.save()
            return redirect('parking_list')
    else:
        form = ParkingSpotForm(instance=parking_spot)
    return render(request, 'myparking/edit_parking_spot.html', {'form': form})


@login_required
def delete_parking_spot(request, pk):
    parking_spot = get_object_or_404(ParkingSpot, pk=pk)
    parking_spot.delete()
    return redirect('parking_list')
