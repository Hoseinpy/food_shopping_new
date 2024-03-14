from django.db import models

# food category
class FoodCategory(models.Model):
    title = models.CharField(max_length=100)
    url_title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categorys'

    def __str__(self) -> str:
        return self.url_title


# food model
class FoodModel(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food', null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    short_description = models.TextField(max_length=200)
    description = models.TextField(max_length=500)
    rating = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'food'
        verbose_name_plural = 'foods'

    def __str__(self) -> str:
        return self.name