from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        if len(post_data['name']) < 3:
            errors['name'] = "Name must be 3 characters or more!"
        if len(post_data['alias']) < 3:
            errors['alias'] = "Alias must be 3 characters or more!"
        if len(post_data['email']) < 8:
            errors['email'] = "Email must be 8 characters or more!"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be 8 characters or more!"
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm'] = "Passwords don't match!"
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        if len(post_data['email']) < 8:
            errors['email'] = "Email must be 8 characters or more!"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be 8 characters or more!"
        return errors
    
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Author(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Book(models.Model):
    title = models.CharField(max_length=55)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    submitter = models.ForeignKey(User, related_name="submitted_books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    content = models.CharField(max_length=255)
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name="submitted_reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)