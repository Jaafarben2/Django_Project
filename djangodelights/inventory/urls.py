from django.urls import path
from . import  views
from django.urls import include

urlpatterns = [

    path('', views.home, name="home"),
    path('ingredient/list', views.IngredientListView.as_view(), name="ingredient_list"),
    path('menu_item/list', views.MenuItemListView.as_view(), name="menu_item_list"),
    path('purchase/list', views.PurchaseListView.as_view(), name="purchase_list"),
    path('ingredient/add', views.AddIngredientView.as_view(), name="ingredient_add"),
    path('menu_item/add', views.AddMenuItemView.as_view(), name="menu_item_add"),
    path('purchase/add', views.AddPurchaseView.as_view(), name="purchase_add"),
    path('recipe_requirement/add', views.AddRecipeRequirementView.as_view(), name="recipe_requirement_add"),
    path('ingredient/update/<int:pk>',views.UpdateIngredientView.as_view(), name="ingredient_update"),
    path('report', views.ReportView.as_view(), name='report'),
    path("logout/", views.logout_view, name="_logout"),
]