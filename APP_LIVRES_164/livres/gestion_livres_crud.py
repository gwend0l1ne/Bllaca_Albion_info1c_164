"""Gestion des "routes" FLASK et des données pour les livres.
Fichier : gestion_livres_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_LIVRES_164.database.database_tools import DBconnection
from APP_LIVRES_164.erreurs.exceptions import *
from APP_LIVRES_164.livres.gestion_livres_wtf_forms import FormWTFUpdateLivre, FormWTFAddLivre, FormWTFDeleteLivre

"""Ajouter un livre grâce au formulaire "livre_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /livre_add

Test : exemple: cliquer sur le menu "Livres/Genres" puis cliquer sur le bouton "ADD" d'un "livre"

Paramètres : sans


Remarque :  Dans le champ "nom_livre_update_wtf" du formulaire "livres/livres_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""


@app.route("/livre_add", methods=['GET', 'POST'])
def livre_add_wtf():
    # Objet formulaire pour AJOUTER un livre
    form_add_livre = FormWTFAddLivre()
    if request.method == "POST":
        try:
            if form_add_livre.validate_on_submit():
                nom_livre_add = form_add_livre.nom_livre_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_nom_livre": nom_livre_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_livre = """INSERT INTO t_livre (id_livre,nom_livre) VALUES (NULL,%(value_nom_livre)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_livre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau livre (id_livre_sel=0 => afficher tous les livres)
                return redirect(url_for('livres_genres_afficher', id_livre_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{livre_add_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("livres/livre_add_wtf.html", form_add_livre=form_add_livre)


"""Editer(update) un livre qui a été sélectionné dans le formulaire "livres_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /livre_update

Test : exemple: cliquer sur le menu "Livres/Genres" puis cliquer sur le bouton "EDIT" d'un "livre"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

Remarque :  Dans le champ "nom_livre_update_wtf" du formulaire "livres/livres_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/livre_update", methods=['GET', 'POST'])
def livre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_livre"
    id_livre_update = request.values['id_livre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_livre = FormWTFUpdateLivre()
    try:
        print(" on submit ", form_update_livre.validate_on_submit())
        if form_update_livre.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_livre_update = form_update_livre.nom_livre_update_wtf.data
            page_livre_update = form_update_livre.page_livre_update_wtf.data
            description_livre_update = form_update_livre.description_livre_update_wtf.data
            cover_link_livre_update = form_update_livre.cover_link_livre_update_wtf.data
            datesortie_livre_update = form_update_livre.datesortie_livre_update_wtf.data

            valeur_update_dictionnaire = {"value_id_livre": id_livre_update,
                                          "value_nom_livre": nom_livre_update,
                                          "value_page_livre": page_livre_update,
                                          "value_description_livre": description_livre_update,
                                          "value_cover_link_livre": cover_link_livre_update,
                                          "value_datesortie_livre": datesortie_livre_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_livre = """UPDATE t_livre SET nom_livre = %(value_nom_livre)s,
                                                            page_livre = %(value_page_livre)s,
                                                            description_livre = %(value_description_livre)s,
                                                            cover_link_livre = %(value_cover_link_livre)s,
                                                            date_sortie_livre = %(value_datesortie_livre)s
                                                            WHERE id_livre = %(value_id_livre)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_livre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le livre modifié, "ASC" et l'"id_livre_update"
            return redirect(url_for('livres_genres_afficher', id_livre_sel=id_livre_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_livre" et "intitule_genre" de la "t_genre"
            str_sql_id_livre = "SELECT * FROM t_livre WHERE id_livre = %(value_id_livre)s"
            valeur_select_dictionnaire = {"value_id_livre": id_livre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_livre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_livre = mybd_conn.fetchone()
            print("data_livre ", data_livre, " type ", type(data_livre), " genre ",
                  data_livre["nom_livre"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "livre_update_wtf.html"
            form_update_livre.nom_livre_update_wtf.data = data_livre["nom_livre"]
            form_update_livre.page_livre_update_wtf.data = data_livre["page_livre"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" page livre  ", data_livre["page_livre"], "  type ", type(data_livre["page_livre"]))
            form_update_livre.description_livre_update_wtf.data = data_livre["description_livre"]
            form_update_livre.cover_link_livre_update_wtf.data = data_livre["cover_link_livre"]
            form_update_livre.datesortie_livre_update_wtf.data = data_livre["date_sortie_livre"]

    except Exception as Exception_livre_update_wtf:
        raise ExceptionLivreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{livre_update_wtf.__name__} ; "
                                     f"{Exception_livre_update_wtf}")

    return render_template("livres/livre_update_wtf.html", form_update_livre=form_update_livre)


"""Effacer(delete) un livre qui a été sélectionné dans le formulaire "livres_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /livre_delete
    
Test : ex. cliquer sur le menu "livre" puis cliquer sur le bouton "DELETE" d'un "livre"
    
Paramètres : sans

Remarque :  Dans le champ "nom_livre_delete_wtf" du formulaire "livres/livre_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/livre_delete", methods=['GET', 'POST'])
def livre_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_livre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_livre"
    id_livre_delete = request.values['id_livre_btn_delete_html']

    # Objet formulaire pour effacer le livre sélectionné.
    form_delete_livre = FormWTFDeleteLivre()
    try:
        # Si on clique sur "ANNULER", afficher tous les livres.
        if form_delete_livre.submit_btn_annuler.data:
            return redirect(url_for("livres_genres_afficher", id_livre_sel=0))

        if form_delete_livre.submit_btn_conf_del_livre.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "livres/livre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_livre_delete = session['data_livre_delete']
            print("data_livre_delete ", data_livre_delete)

            flash(f"Effacer le livre de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_livre.submit_btn_del_livre.data:
            valeur_delete_dictionnaire = {"value_id_livre": id_livre_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_livre_genre = """DELETE FROM t_genre_livre WHERE fk_livre = %(value_id_livre)s"""
            str_sql_delete_livre = """DELETE FROM t_livre WHERE id_livre = %(value_id_livre)s"""
            # Manière brutale d'effacer d'abord la "fk_livre", même si elle n'existe pas dans la "t_genre_livre"
            # Ensuite on peut effacer le livre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_livre"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_livre_genre, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_livre, valeur_delete_dictionnaire)

            flash(f"Livre définitivement effacé !!", "success")
            print(f"Livre définitivement effacé !!")

            # afficher les données
            return redirect(url_for('livres_genres_afficher', id_livre_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_livre": id_livre_delete}
            print(id_livre_delete, type(id_livre_delete))

            # Requête qui affiche le livre qui doit être efffacé.
            str_sql_genres_livres_delete = """SELECT * FROM t_livre WHERE id_livre = %(value_id_livre)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_livres_delete, valeur_select_dictionnaire)
                data_livre_delete = mydb_conn.fetchall()
                print("data_livre_delete...", data_livre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "livres/livre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_livre_delete'] = data_livre_delete

            # Le bouton pour l'action "DELETE" dans le form. "livre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_livre_delete_wtf:
        raise ExceptionLivreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{livre_delete_wtf.__name__} ; "
                                     f"{Exception_livre_delete_wtf}")

    return render_template("livres/livre_delete_wtf.html",
                           form_delete_livre=form_delete_livre,
                           btn_submit_del=btn_submit_del,
                           data_livre_del=data_livre_delete
                           )
