from django.db import models


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    available_quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=20)
    unit_price = models.FloatField()
    def get_absolute_url(self):
        return "/inventory/ingredient/list"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()

    def available(self):
        recipe_requiements = self.reciperequirement_set.all()
        for r_r in recipe_requiements :
            if r_r.quantity_required > r_r.ingredient.available_quantity :
                return False
        return True

    def get_absolute_url(self):
        return "/inventory/menu_item/list"
    def __str__(self):
        return self.name


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.FloatField()
    def get_absolute_url(self):
        return "/inventory/recipe_requirement/add"
    def __str__(self):
        return "{} : {} {}".format(self.menu_item, self.quantity_required, self.ingredient)


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return "/inventory/purchase/list"
    def __str__(self):
        return "{} : {}".format(self.menu_item.name, self.date)
