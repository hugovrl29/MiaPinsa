from django.conf.urls.static import static
from django.urls import path
from .views import *
from MiaPinsa import settings

urlpatterns = [
    path('', index, name="livraison-index"),
    path('plats/', food_display, name="affiche-produits"),
    path('product/<str:slug>/ajouter/<int:panier>/', commander_food, name="add_to_cart"),
    path('product/<str:slug>/retirer/<int:panier>', retirer_produit, name="remove_from_cart"),
    path('supprimer_panier/', supprimer_panier, name="delete_cart"),
    path('valider_panier/', commander_payer, name="confirm_cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
