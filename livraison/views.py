from statistics import mean

import geopy.distance
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from folium import plugins
from geopy import Nominatim

from .forms import *
from .models import *
import folium
import osmnx as ox
import networkx as nx



def dispatch_trajets(commande_id):
    current_commande = Commande.objects.get(id=commande_id)

    trajets = Trajet.objects.all().order_by('-trajet_depart', 'trajet_distance')

    locator = Nominatim(user_agent="myGeocoder")
    # TODO ne trouve pas l'adresse
    client_location = locator.geocode(current_commande.commande_client.adresse)
    local_location = locator.geocode("Chaussée de Liège, 556 - 5100 Jambes")

    if trajets is None:
        livreurs = Livreur.objects.all()

        if livreurs is None:
            livreur = Livreur.objects.create(livreur_nom="test", livreur_prenom="test")
            livreur.save()
        else:
            livreur = livreurs[0]

        distance = geopy.distance.geodesic([client_location.latitude, client_location.longitude],
                                           [local_location.latitude, local_location.longitude]).km
        trajet = Trajet.objects.create(trajet_livreur=livreur, trajet_distance=distance)
        trajet.save()

        return trajet

    else:
        for trajet in trajets:
            trajet_commandes = Commande.objects.filter(commande_trajet=trajet)

            # get the max distance from the furthest client of command
            max_distance = 0
            for cmd in trajet_commandes:
                other_client_location = locator.geocode(cmd.commande_client.adresse)
                other_client_distance = geopy.distance.geodesic(local_location, other_client_location).km
                if other_client_distance == trajet.trajet_distance:
                    max_client = cmd.commande_client

            distance_between = geopy.distance.geodesic([client_location.latitude, client_location.longitude],
                                                [other_client_location.latitude, other_client_location.longitude]).km

            if distance_between < trajet.trajet_distance:
                return trajet

    livreurs = Livreur.objects.all()
    if not livreurs:
        livreur = Livreur.objects.create(livreur_nom="test", livreur_prenom="test")
        livreur.save()

        distance = geopy.distance.geodesic([client_location.latitude, client_location.longitude], [local_location.latitude, local_location.longitude]).km
        trajet = Trajet.objects.create(trajet_livreur=livreur, trajet_distance=distance)
        trajet.save()
    else:
        distance = geopy.distance.geodesic([client_location.latitude, client_location.longitude],
                                           [local_location.latitude, local_location.longitude]).km
        trajet = Trajet.objects.create(trajet_livreur=livreurs[0], trajet_distance=distance)
        trajet.save()

    return trajet


def index(request):
    user = request.user

    commande = Commande.objects.get(commande_client=user)

    locator = Nominatim(user_agent="myGeocoder")

    local_location = locator.geocode("Chaussée de Liège, 556 - 5100 Jambes")

    commande.commande_trajet = dispatch_trajets(commande.id)
    all_command_trajet = Commande.objects.filter(commande_trajet=commande.commande_trajet).order_by('commande_date')

    last_location = locator.geocode(all_command_trajet[-1].commande_client.adresse)

    map_latitude = mean([last_location.latitude, local_location.latitude])
    map_longitude = mean([last_location.longitude, local_location.longitude])
    m = folium.Map(location=[map_latitude, map_longitude], width=425, height=350, zoom_start=13)

    tooltip = "Details"

    folium.Marker(
        [local_location.latitude, local_location.longitude], popup="<b>MiaPinsa</b>", tooltip=tooltip
    ).add_to(m)

    for cmd in all_command_trajet:
        client_location = locator.geocode(cmd.commande_client.adresse)
        if cmd.commande_client == user:
            folium.Marker(
                [cmd.client_location.latitude, client_location.longitude], popup="<b>Domicile</b>",
                tooltip=tooltip, color='white'
            ).add_to(m)
        else:
            folium.Marker(
                [cmd.client_location.latitude, client_location.longitude], popup="<b>Autre arrêt</b>",
                tooltip=tooltip
            ).add_to(m)

    plugins.AntPath([[local_location.latitude,
                    local_location.longitude], [client_location.latitude, client_location.longitude]]).add_to(m)
    m.save("livraison/templates/livraison/map_trajet.html")
    return render(request, "livraison/index.html")


def food_display(request):
    # user = request.user

    produits = Produit.objects.all()
    if not produits:
        Produit.objects.create(produit_libelle="Margherita", produit_prix=9, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Basilic", slug="margherita")
        Produit.objects.create(produit_libelle="Napoli", produit_prix=10, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Anchois, Câpres", slug="napoli")
        Produit.objects.create(produit_libelle="Prosciutto", produit_prix=10, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon", slug="prosciutto")
        Produit.objects.create(produit_libelle="Regina", produit_prix=10.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon, Champignons", slug="regina")
        Produit.objects.create(produit_libelle="Al tonno", produit_prix=11, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Thon, Oignons, Ail, Olives", slug="al-tonno")
        Produit.objects.create(produit_libelle="Bolognese", produit_prix=11, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Bolognaise, Mozzarella", slug="bolognese")
        Produit.objects.create(produit_libelle="Hawaï", produit_prix=10.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon, Ananas", slug="hawaii")
        Produit.objects.create(produit_libelle="Salame", produit_prix=11, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Salami", slug="salame")
        Produit.objects.create(produit_libelle="Salame Piccante", produit_prix=11, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Salami piquant", slug="salame-piccante")
        Produit.objects.create(produit_libelle="Capricciosa", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon, Champignons, Anchois, Olives",
                               slug="capricciosa")
        Produit.objects.create(produit_libelle="Pollo", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Poulet, Poivrons, Champignons, Olives",
                               slug="pollo")
        Produit.objects.create(produit_libelle="4 Stagioni", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon, Salami, Champignons, Artichaut",
                               slug="4-stagioni")
        Produit.objects.create(produit_libelle="4 Formaggi", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Bel paese, Gorgonzola, Taleggio",
                               slug="4-formaggi")
        Produit.objects.create(produit_libelle="Roma", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon, Salami, Oeufs, Oignons", slug="roma")
        Produit.objects.create(produit_libelle="Al Capone", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon, Poivrons, Oeuf dur, Ail, Anchois",
                               slug="al-capone")
        Produit.objects.create(produit_libelle="Fiorentina", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Jambon, Epinards, Oignon, Oeuf", slug="fiorentina")
        Produit.objects.create(produit_libelle="Forestière", produit_prix=12.5, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Champignons, Lardons, Oignons, Ail",
                               slug="forestiere")
        Produit.objects.create(produit_libelle="Frutti di mare", produit_prix=13, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Moules, Crevettes, Calamars, Ail",
                               slug="frutti-di-mare")
        Produit.objects.create(produit_libelle="Scampi", produit_prix=13, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Mozzarella, Scampis, Ail", slug="scampi")
        Produit.objects.create(produit_libelle="San Daniele", produit_prix=13, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, 4 fromages, jambon de Parme", slug="san-daniele")
        Produit.objects.create(produit_libelle="Ruccola", produit_prix=13, produit_type='PS', produit_sous_type='BQ',
                               produit_composition="Tomate, Jambon de Parme, Tomates Cerises, Roquette balsemique,\
                                                   Copeaux de parmesan", slug="ruccola")

    pinsa = Produit.objects.filter(produit_type="PS")
    antipasti = Produit.objects.filter(produit_type="AP")
    pasta = Produit.objects.filter(produit_type="PA")
    pastalforno = Produit.objects.filter(produit_type="PF")
    dessert = Produit.objects.filter(produit_type="DS")
    boisson = Produit.objects.filter(produit_type="BS")

    # if Commande.objects.filter(commande_client=user)

    return render(request, 'livraison/afficher_produits.html', {"pinsa": pinsa, "antipasti": antipasti,
                                                                "pasta": pasta, "pastalforno": pastalforno,
                                                                "dessert": dessert, "boisson": boisson})


def commander_food(request, slug, panier):
    user = request.user
    product = get_object_or_404(Produit, slug=slug)

    if Commande.objects.filter(commande_client=user).exists():
        command = Commande.objects.get(commande_client=user)
        if Detail.objects.filter(detail_commande=command, detail_produit=product).exists():
            detail = Detail.objects.get(detail_commande=command, detail_produit=product)
            detail.detail_quantite += 1
            detail.save()
        else:
            detail = Detail.objects.create(detail_produit=product, detail_commande=command)
            detail.save()
    else:
        command = Commande.objects.create(commande_client=user)
        detail = Detail.objects.create(detail_produit=product, detail_commande=command)
        detail.save()

    if panier == 1:
        return redirect("confirm_cart")

    return redirect("affiche-produits")


def retirer_produit(request, slug, panier):
    user = request.user
    product = get_object_or_404(Produit, slug=slug)

    if Commande.objects.filter(commande_client=user).exists():
        command = Commande.objects.get(commande_client=user)
        detail = Detail.objects.get(detail_commande=command, detail_produit=product)
        if detail is not None:
            if detail.detail_quantite > 1:
                detail.detail_quantite -= 1
                detail.save()
            elif detail.detail_quantite == 1:
                detail.delete()

    if panier == 1:
        return redirect("confirm_cart")

    return redirect("affiche-produits")


def supprimer_panier(request):
    user = request.user
    commande = Commande.objects.get(commande_client=user)
    if commande is not None:
        detail = Detail.objects.filter(detail_commande=commande)
        detail.delete()
        commande.delete()
    return redirect("affiche-produits")


def commander_payer(request):
    user = request.user
    commande = Commande.objects.get(commande_client=user)
    details = Detail.objects.filter(detail_commande=commande)
    total = 0
    for detail in details:
        total += (detail.detail_quantite * detail.detail_produit.produit_prix)

    return render(request, 'livraison/panier.html', {"details": details, "prix_total": total})

