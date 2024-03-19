from django.db import models

from auth_api.models import UserModel


# food category
class FoodCategory(models.Model):
    image = models.ImageField(upload_to='category', null=True, blank=True, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    url_title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categorys'

    def __str__(self) -> str:
        return self.url_title


# food model
class FoodModel(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='category_food', db_index=True)
    image = models.ImageField(upload_to='food', null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    short_description = models.TextField(max_length=200)
    description = models.TextField(max_length=500)
    rating = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'food'
        verbose_name_plural = 'foods'

    def __str__(self):
        return self.name


class CartModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodModel, on_delete=models.CASCADE, related_name='food', db_index=True)
    quantity = models.PositiveIntegerField(default=1, blank=True, db_index=True)
    finall_price = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
