from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    volume = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50)
    exchange_books = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(upload_to='book_images/')
    
    def __str__(self):
        return self.name
    

from django.db import models



class ReadAndEarnBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    volume = models.CharField(max_length=100, blank=True, null=True)
    date_of_submission = models.DateTimeField(blank=True,null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='read_and_earn_books/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class BookReview(models.Model):
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    volume = models.CharField(max_length=100, blank=True, null=True)
    availability = models.CharField(max_length=200)
    review = models.TextField()
    pros = models.TextField()
    cons = models.TextField()
    reviewed_by = models.CharField(max_length=100)
    review_date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='book_reviews/', blank=True, null=True)

    def __str__(self):
        return self.book_name
    
class Comment(models.Model):
    book_review = models.ForeignKey(BookReview, related_name='comments', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.book_review}'
    
# class Blog(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=100)
#     date = models.DateField(default=timezone.now)
#     content = models.TextField()
#     image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

#     def __str__(self):
#         return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date = models.DateField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.blog}'
    
from django.db import models

class Package(models.Model):
    PACKAGE_CHOICES = [
        ('Diamond', 'Diamond'),
        ('Platinum', 'Platinum'),
        ('Gold', 'Gold'),
    ]

    book_name = models.CharField(max_length=200)
    book_cost = models.DecimalField(max_digits=10, decimal_places=2)
    book_link = models.URLField()
    package = models.CharField(max_length=10, choices=PACKAGE_CHOICES)
    book_image = models.ImageField(upload_to='package_images/')
    book_pdf = models.FileField(upload_to='package_pdfs/')

    def __str__(self):
        return self.book_name








