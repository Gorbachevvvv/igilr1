from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models



class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('Имя пользователя', max_length=20)
    companyname = models.CharField('Название компании', max_length=20)
    birth_date = models.DateField('Дата рождения',null=True, blank=True)
    def __str__(self):
        return self.companyname

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name=models.CharField('Имя пользователя', max_length=20)
    phone_number = models.CharField('Номер телефона', max_length=15, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )], blank=True)
    city=models.CharField('Город',max_length=20)
    adress=models.CharField('Адрес', max_length=100)
    email=models.EmailField('Почта')
    birth_date = models.DateField('Дата рождения', null=True, blank=True)


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    mark = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    # parking_spot = models.ForeignKey('ParkingSpot', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.mark} {self.model} ({self.license_plate})"


class ParkingSpot(models.Model):
    number = models.PositiveIntegerField(unique=True, validators=[MaxValueValidator(1000)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_busy = models.BooleanField(default=False)
    cars = models.ManyToManyField(Car, help_text="Select a car for this parking", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='parkings', blank=True, null=True)
    date_of_rent = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Parking Spot {self.number}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    park = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='parking_spot', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    # Дата начисления
    receipt_date = models.DateField(blank=True, null=True)
    receipt_time = models.TimeField(blank=True, null=True)
    # Дата погашения платежа
    repayment_date = models.DateField(blank=True, null=True)
    repayment_time = models.TimeField(blank=True, null=True)


class Account(models.Model):  # счет в банке, для возможности оплаты
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class News(models.Model):
    news_label = models.CharField(max_length=30, default='article title')
    news = models.CharField('Краткая', max_length=100, default='content')
    news_long = models.CharField('Полная', max_length=300, default='content')
    newsimg = models.ImageField('Картинка', upload_to='static', default='asd')
    date = models.DateField('Дата', blank=True, null = True)
    def str(self):
        return self.news


class Rating(models.IntegerChoices):
    ONE = 1, 'One'
    TWO = 2, 'Two'
    THREE = 3, 'Three'
    FOUR = 4, 'Four'
    FIVE = 5, 'Five'

class Feedbacks(models.Model): #отзывы
    name = models.CharField('Имя пользователя', max_length=20)
    rating = models.IntegerField()
    text = models.TextField('Отзыв', max_length=2500)

    def __str__(self):
        return f"{self.name} {self.rating}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    dating=models.DateField('Дата публикации', auto_now_add=True)

class About(models.Model):
    logo = models.ImageField('Логотип')
    aboutcompany = models.TextField('Рассказ о компании')
    requisites = models.TextField('Реквизиты')
    video = models.FileField('Видео о компании', upload_to='static')

    def __str__(self):
        return self.requisites
    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=100)
    answer = models.CharField('Ответ', max_length=500)
    date=models.DateField('Дата добавления')
    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'


class Contacts(models.Model):

    name = models.CharField('Имя', max_length=10)
    email = models.EmailField('Емаил сотрудника')
    aboutwork=models.TextField('Выполняемая работа', max_length=500)
    phone_number = models.CharField('Номер телефона',max_length=15,validators=[RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )],blank=True)
    image = models.ImageField('Фото', upload_to='static')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

class Vacancies(models.Model):

     name = models.CharField('Название вакансии', max_length=25)
     about = models.TextField('О вакансии', max_length=500)

     def __str__(self):
         return self.name

     class Meta:
         verbose_name = 'Вакансия'
         verbose_name_plural = 'Вакансии'

class Promocodes(models.Model):
    work = models.BooleanField('Действует или в нет (в архиве)?', default=True)
    name = models.CharField('Промокод', max_length=30)
    about = models.IntegerField('Сколько (в рублях)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
