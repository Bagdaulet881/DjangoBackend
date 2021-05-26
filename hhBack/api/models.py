from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.postgres.fields import ArrayField
from .managers import ProductsManager
from django.contrib.auth.models import User
# TEST TASK Models

class Status(models.Model):
    title = models.CharField(max_length=1000, default='not defined')

    def __str__(self):
        return '{}:{}'.format(self.id, self.title)

class User2(models.Model):
    name = models.CharField(max_length=1000, default='UserName')
    email = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    def __str__(self):
        return '{}:{}'.format(self.id, self.email)

class Record(models.Model):
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d")
    created_at = models.CharField(max_length=1000, default=formatedDate, blank = True)
    # created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=1000, default='7775556881')
    description = models.CharField(max_length=1000, default='some descrip lorem is')
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return '{}:{}'.format(self.id, self.created_at)

# MY PROJECT MODELS
# class Category(models.Model):
#     class Meta:
#         verbose_name_plural = 'categories'

#     img_link = models.CharField(max_length=1000, default='https://i1.imageban.ru/out/2017/12/11/e7afe65c4f3028db5e2127f32740ac3d.jpg')
#     time = models.CharField(max_length=1000, default='0 hr 15 min')
#     name = models.CharField(max_length=1000, default='categoryName')


#     def __str__(self):
#         return '{}:{}'.format(self.id, self.name)

# class Product(models.Model):
#     class Meta:
#         verbose_name_plural = 'products'

#     category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=1000)
#     time = models.CharField(max_length=1000, default='0 hr 15 min')
#     description = models.CharField(max_length=1000)
#     image = models.CharField(max_length=1000, default='https://i1.imageban.ru/out/2017/12/11/e7afe65c4f3028db5e2127f32740ac3d.jpg')
#     rating = models.FloatField(default=0.0)
#     ingredients = models.CharField(max_length=1000, default=' ')
#     methods = models.CharField(max_length=1000, default=' ')

#     objects = ProductsManager()

#     def __str__(self):
#         return '{}:{}'.format(self.id, self.name)

# class Comment(models.Model):
#     class Meta:
#         verbose_name_plural = 'comments'

#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     login = models.CharField(max_length=1000)
#     date = models.DateTimeField(editable=False)
#     text = models.CharField(max_length=1000)

#     def __str__(self):
#         return '{}:{}'.format(self.id, self.login)

#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.date = timezone.now()
#         return super(Comment, self).save(*args, **kwargs)

# class MyUser(models.Model):
#     class Meta:
#         verbose_name_plural = 'users'

#     username = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100, default='')
#     password = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=50, default='')
#     is_superuser = models.BooleanField(default=False)

#     def __str__(self):
#         return '{}:{}'.format(self.id, self.login)
# #-------------------------------
# class Company(models.Model):
#     class Meta:
#         verbose_name_plural = 'companies'

#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=1000, default=' ')
#     city = models.CharField(max_length=200)
#     address = models.CharField(max_length=1000, )

#     def to_json(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#             'city': self.city,
#             'address': self.address
#         }
#     def __str__(self):
#         return '{}:{}'.format(self.id, self.name)

# class Vacancy(models.Model):
#     class Meta:
#         verbose_name_plural = 'vacancies'

#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=1000, default=' ')
#     salary = models.FloatField(default=0.0)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)

#     def to_json(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#             'salary': self.salary,
#             'company': self.company.name
#         }
#     def __str__(self):
#         return '{}:{}'.format(self.id,self.name)