from django.db import models

# Create your models here.
class Blog(models.Model):
    blog_Id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 100)
    content = models.TextField()
    slug = models.CharField(max_length = 100, unique = True)
    author = models.CharField(max_length = 30)
    datetime = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.author + ': ' + self.title

class Contact(models.Model):
    contact_Id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
