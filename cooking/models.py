from django.db import models
from django.contrib.auth.models import User
import uuid

class IngredientType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    kcal = models.IntegerField()

    def update(self,*args, **kwargs):
        for name, values in kwargs.items():
            try:
                setattr(self,name,values)
            except KeyError:
                pass
        self.save()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    ingredient_type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity} {self.ingredient_type.name}'


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, default=f'{uuid.uuid4()}'.replace('-', ''), unique=True)

    def __str__(self):
        return self.token


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=100)
    body = models.JSONField()
    response = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.endpoint} - {self.date}'
    

class Recipe(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    total_kcal = models.IntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        self.total_kcal = sum([ingredient.ingredient_type.kcal * (ingredient.quantity/100) for ingredient in self.ingredients.all()])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name