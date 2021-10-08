from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.

class IngredientListView(LoginRequiredMixin, ListView):
    template_name = "inventory/ingredients_list.html"
    model = Ingredient


class MenuItemListView(LoginRequiredMixin, ListView):
    template_name = "inventory/menu_items_list.html"
    model = MenuItem


class PurchaseListView(LoginRequiredMixin, ListView):
    template_name = "inventory/purchases_list.html"
    model = Purchase


class AddIngredientView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/add_ingredient.html"
    form_class = IngredientForm


class AddMenuItemView(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory/add_menu_item.html"
    form_class = MenuItemForm


class AddPurchaseView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/add_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.all()
        return context

    def post(self, request):
        menu_item_id = request.POST.get("menu_item")
        print(menu_item_id)
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        purchase = Purchase(menu_item=menu_item)
        for r_r in menu_item.reciperequirement_set.all():
            ingredient = r_r.ingredient
            ingredient.available_quantity -= r_r.quantity_required
            ingredient.save()
        purchase.save()
        return redirect('purchase_list')


class AddRecipeRequirementView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/add_recipe_requirement.html"
    form_class = RecipeRequirementForm


class UpdateIngredientView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/update_ingredient.html"
    form_class = IngredientForm


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(Sum('menu_item__price'))['menu_item__price__sum']
        cost = 0
        for p in Purchase.objects.all():
            r_rs = p.menu_item.reciperequirement_set.all()
            for r_r in r_rs:
                cost += r_r.ingredient.unit_price * r_r.quantity_required
        context['revenue'] = revenue
        context['cost'] = cost
        context['profit'] = revenue - cost
        return context


@login_required
def home(request):
    return render(request, "inventory/home.html")


def logout_view(request):
    logout(request)
    return redirect("home")
