from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
import uuid

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=256)
    apartment = models.CharField(max_length=50)
    entrance = models.SmallIntegerField(blank=True, null=True)
    floor = models.SmallIntegerField(blank=True, null=True)
    intercom = models.SmallIntegerField(blank=True, null=True)
    clarification_to_the_address = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'

class Authors(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'authors'

    def __str__(self):
        return self.name
    
class Basket(models.Model):
    basket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.CASCADE, null=True)
    book = models.ForeignKey('Books', models.CASCADE)
    quantity = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'basket'

class BindingType(models.Model):
    binding_type_id = models.AutoField(primary_key=True)
    name_binding_type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'binding_type'
    
    def __str__(self):
        return self.name_binding_type
    
class BookSeries(models.Model):
    book_series_id = models.AutoField(primary_key=True)
    name_book_series = models.CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'book_series'

    def __str__(self):
        return self.name_book_series
    
class Books(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Authors, models.DO_NOTHING)
    binding_type = models.ForeignKey(BindingType, models.DO_NOTHING)
    series = models.ForeignKey('BookSeries', models.DO_NOTHING, db_column='series_id', blank=True, null=True)
    publisher = models.ForeignKey('Publisher', models.DO_NOTHING)
    title = models.CharField(max_length=100)
    price_book = models.DecimalField(max_digits=10, decimal_places=2)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    stock = models.IntegerField(blank=True, null=True)
    image_path = models.TextField()
    age_limit = models.CharField(max_length=3, blank=True, null=True)
    language_code = models.ForeignKey('Languages', models.DO_NOTHING, db_column='language_code')
    description = models.TextField()
    circulation = models.IntegerField()
    weight = models.SmallIntegerField()
    size = models.CharField(max_length=20)
    isbn = models.CharField(max_length=20, unique=True)
    pages = models.SmallIntegerField()
    year_of_publication = models.IntegerField()
    year_of_release = models.IntegerField(blank=True, null=True)
    rating = models.ImageField()

    class Meta:
        managed = False
        db_table = 'books'
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name_category = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'category'

    def __str__(self):
        return self.name_category
    
class GeneralsProducts(models.Model):
    general_products_id = models.UUIDField(primary_key=True)
    stationery = models.ForeignKey('Stationery', models.DO_NOTHING)
    subcategory = models.ForeignKey('SubcategoryStationery', models.DO_NOTHING)
    material = models.CharField(max_length=50, blank=True, null=True)
    number_of_punched_sheets = models.SmallIntegerField(blank=True, null=True)
    calculator_bit_size = models.SmallIntegerField(blank=True, null=True)
    number_stapler = models.CharField(max_length=10, blank=True, null=True)
    peculiarity = models.TextField(blank=True, null=True)
    number_staples = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'generals_products'
    
class Languages(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'languages'

    def __str__(self):
        return self.name

class OrderDetails(models.Model):
    order_detail_id = models.UUIDField(primary_key=True, db_default=uuid.uuid4, editable=False)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    quantity = models.SmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'order_details'

    def save(self, *args, **kwargs):
        self.price = self.book.price_book * self.quantity
        super().save(*args, **kwargs)

class Orders(models.Model):

    STATUS_CHOICES = [
        ('Ожидание оплаты', 'Ожидание оплаты'),
        ('Оплачен', 'Оплачен'),
        ('Собран', 'Собран'),
        ('Передан в доставку', 'Передан в доставку'),
        ('В пути', 'В пути'),
        ('Доставлен', 'Доставлен'),
        ('Отменён', 'Отменён'),
        ('Возврат', 'Возврат'),
        ('Завершён', 'Завершён'),
    ]

    order_id = models.UUIDField(primary_key=True, db_default=uuid.uuid4, editable=False)
    user = models.ForeignKey('Users', models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        managed = False
        db_table = 'orders'

class PaperProducts(models.Model):
    paper_products_id = models.UUIDField(primary_key=True)
    stationery = models.ForeignKey('Stationery', models.DO_NOTHING)
    subcategory = models.ForeignKey('SubcategoryStationery', models.DO_NOTHING)
    number_of_sheets = models.SmallIntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, blank=True, null=True)
    type_of_ruler = models.CharField(max_length=50, blank=True, null=True)
    peculiarity = models.TextField(blank=True, null=True)
    mounting_type = models.CharField(max_length=50, blank=True, null=True)
    calendar_year = models.SmallIntegerField(blank=True, null=True)
    quantity_colors = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paper_products'

class Payment(models.Model):
    STATUS_CHOICES = [
        ('успешно', 'Успешно'),
        ('ошибка', 'Ошибка'),
        ('ожидание', 'Ожидание'),
        ('возврат', 'Возврат'),
    ]

    payment_id = models.UUIDField(primary_key=True, db_default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    order = models.OneToOneField(Orders, models.DO_NOTHING)
    payment_date = models.DateTimeField(auto_now_add=True, editable=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.TextField()
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ожидание'
    )

    class Meta:
        managed = False
        db_table = 'payment'

    def save(self, *args, **kwargs):
        if self.order:
            total_amount = self.order.orderdetails_set.aggregate(total=models.Sum('price'))['total']
            self.amount = total_amount if total_amount is not None else 0
        super().save(*args, **kwargs)

class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    name_publisher = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'publisher'

    def __str__(self):
        return self.name_publisher
    
class Reviews(models.Model):
    reviews_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Books, models.CASCADE, db_column='book_id')
    rating = models.SmallIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255)
    review_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        managed = False
        db_table = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'], 
                name='unique_user_book_review'
            ),
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_range'
            )
        ]

class Stationery(models.Model):
    stationery_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_stationery = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True)
    date_of_receipt = models.DateTimeField()
    size = models.CharField(max_length=20, blank=True, null=True)
    weight = models.SmallIntegerField(blank=True, null=True)
    age_limit = models.CharField(max_length=3, blank=True, null=True)
    material_color = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stationery'

class StorageType(models.Model):
    storage_type_id = models.UUIDField(primary_key=True)
    stationery = models.ForeignKey(Stationery, models.DO_NOTHING)
    subcategory = models.ForeignKey('SubcategoryStationery', models.DO_NOTHING)
    material = models.CharField(max_length=50, blank=True, null=True)
    number_of_branches = models.SmallIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    peculiarity = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'storage_type'

class Subcategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, models.CASCADE)
    name_subcategory = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'subcategory'

    def __str__(self):
        return self.name_subcategory
    
class SubcategoryStationery(models.Model):
    subcategory_id = models.UUIDField(primary_key=True)
    name_subcategory = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'subcategory_stationery'


class Subscriptions(models.Model):
    subscriptions_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    author = models.ForeignKey(Authors, models.DO_NOTHING, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscriptions'

class CategoryBooks(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(
        'Books',
        on_delete=models.CASCADE,
        db_column='book_id'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='category_id'
    )
    subcategory = models.ForeignKey(
        'Subcategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='subcategory'
    )

    class Meta:
        db_table = 's_books.category_books'
        managed = False

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class Users(AbstractBaseUser, PermissionsMixin): 
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=254)
    password = models.CharField(max_length=128)  
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(unique=True, max_length=16)
    date_registered = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(blank=True, null=True, editable=False)

    is_active = models.BooleanField(default=True)  # Добавляем активность
    is_staff = models.BooleanField(default=False)  # Разрешает вход в админку
    is_superuser = models.BooleanField(default=False)  # Указывает, является ли пользователь суперпользователем

    objects = UserManager()  # Указываем менеджер

    USERNAME_FIELD = 'email'  # Поле для логина
    REQUIRED_FIELDS = ['name', 'last_name', 'phone']  # Обязательные поля

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return f"{self.name} {self.last_name}"
    

class Wishlists(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.CASCADE)
    book = models.ForeignKey(Books, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'wishlists'

class WritingMaterials(models.Model):
    writing_materials_id = models.UUIDField(primary_key=True)
    stationery = models.ForeignKey(Stationery, models.DO_NOTHING)
    subcategory = models.ForeignKey(SubcategoryStationery, models.DO_NOTHING)
    inc_color = models.CharField(max_length=50, blank=True, null=True)
    inc_base = models.CharField(max_length=50, blank=True, null=True)
    pen_thickness = models.CharField(max_length=50, blank=True, null=True)
    peculiarity = models.TextField(blank=True, null=True)
    quantity_colors = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'writing_materials'