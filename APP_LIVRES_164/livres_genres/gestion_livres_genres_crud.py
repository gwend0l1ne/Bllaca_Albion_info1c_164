"""
    Fichier : gestion_livres_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les livres et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_LIVRES_164.database.database_tools import DBconnection
from APP_LIVRES_164.erreurs.exceptions import *

"""
    Nom : livres_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /livres_genres_afficher
    
    But : Afficher les livres avec les genres associés pour chaque livre.
    <
    Paramètres : id_genre_sel = 0 >> tous les livres.
                 id_genre_sel = "n" affiche le livre dont l'id est "n"
                 
"""


@app.route("/livres_genres_afficher/<int:id_livre_sel>", methods=['GET', 'POST'])
def livres_genres_afficher(id_livre_sel):
    print(" livres_genres_afficher id_livre_sel ", id_livre_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_genres_livres_afficher_data = """SELECT id_livre, nom_livre, nom_auteur, description_livre, cover_link_livre, date_sortie_livre,
                                                            GROUP_CONCAT(intitule_genre) as GenresLivres FROM t_genre_livre
                                                            RIGHT JOIN t_livre ON t_livre.id_livre = t_genre_livre.fk_livre
                                                            LEFT JOIN auteur ON auteur.id_auteur = t_genre_livre.fk_auteur
                                                            LEFT JOIN t_genre ON t_genre.id_genre = t_genre_livre.fk_genre
                                                            GROUP BY id_livre"""
                if id_livre_sel == 0:
                    # le paramètre 0 permet d'afficher tous les livres
                    # Sinon le paramètre représente la valeur de l'id du livre
                    mc_afficher.execute(strsql_genres_livres_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du livre sélectionné avec un nom de variable
                    valeur_id_livre_selected_dictionnaire = {"value_id_livre_selected": id_livre_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_genres_livres_afficher_data += """ HAVING id_livre= %(value_id_livre_selected)s"""

                    mc_afficher.execute(strsql_genres_livres_afficher_data, valeur_id_livre_selected_dictionnaire)

                # Récupère les données de la requête.
                data_genres_livres_afficher = mc_afficher.fetchall()
                print("data_genres ", data_genres_livres_afficher, " Type : ", type(data_genres_livres_afficher))

                # Différencier les messages.
                if not data_genres_livres_afficher and id_livre_sel == 0:
                    flash("""La table "t_livre" est vide. !""", "warning")
                elif not data_genres_livres_afficher and id_livre_sel > 0:
                    # Si l'utilisateur change l'id_livre dans l'URL et qu'il ne correspond à aucun livre
                    flash(f"Le livre {id_livre_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données livres et genres affichés !!", "success")

        except Exception as Exception_livres_genres_afficher:
            raise ExceptionLivresGenresAfficher(f"fichier : {Path(__file__).name}  ;  {livres_genres_afficher.__name__} ;"
                                               f"{Exception_livres_genres_afficher}")

    print("livres_genres_afficher  ", data_genres_livres_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("livres_genres/livres_genres_afficher.html", data=data_genres_livres_afficher)


"""
    nom: edit_genre_livre_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du livre sélectionné par le bouton "MODIFIER" de "livres_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au livre selectionné.
    3) Les genres non-attribués au livre sélectionné.

    On signale les erreurs importantes

"""


@app.route("/edit_genre_livre_selected", methods=['GET', 'POST'])
def edit_genre_livre_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_genres_afficher = """SELECT id_genre, intitule_genre FROM t_genre ORDER BY id_genre ASC"""
                mc_afficher.execute(strsql_genres_afficher)
            data_genres_all = mc_afficher.fetchall()
            print("dans edit_genre_livre_selected ---> data_genres_all", data_genres_all)

            # Récupère la valeur de "id_livre" du formulaire html "livres_genres_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_livre"
            # grâce à la variable "id_livre_genres_edit_html" dans le fichier "livres_genres_afficher.html"
            # href="{{ url_for('edit_genre_livre_selected', id_livre_genres_edit_html=row.id_livre) }}"
            id_livre_genres_edit = request.values['id_livre_genres_edit_html']

            # Mémorise l'id du livre dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_livre_genres_edit'] = id_livre_genres_edit

            # Constitution d'un dictionnaire pour associer l'id du livre sélectionné avec un nom de variable
            valeur_id_livre_selected_dictionnaire = {"value_id_livre_selected": id_livre_genres_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_livres_afficher_data
            # 1) Sélection du livre choisi
            # 2) Sélection des genres "déjà" attribués pour le livre.
            # 3) Sélection des genres "pas encore" attribués pour le livre choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_livres_afficher_data"
            data_genre_livre_selected, data_genres_livres_non_attribues, data_genres_livres_attribues = \
                genres_livres_afficher_data(valeur_id_livre_selected_dictionnaire)

            print(data_genre_livre_selected)
            lst_data_livre_selected = [item['id_livre'] for item in data_genre_livre_selected]
            print("lst_data_livre_selected  ", lst_data_livre_selected,
                  type(lst_data_livre_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_genres_livres_non_attribues = [item['id_genre'] for item in data_genres_livres_non_attribues]
            session['session_lst_data_genres_livres_non_attribues'] = lst_data_genres_livres_non_attribues
            print("lst_data_genres_livres_non_attribues  ", lst_data_genres_livres_non_attribues,
                  type(lst_data_genres_livres_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_genres_livres_old_attribues = [item['id_genre'] for item in data_genres_livres_attribues]
            session['session_lst_data_genres_livres_old_attribues'] = lst_data_genres_livres_old_attribues
            print("lst_data_genres_livres_old_attribues  ", lst_data_genres_livres_old_attribues,
                  type(lst_data_genres_livres_old_attribues))

            print(" data data_genre_livre_selected", data_genre_livre_selected, "type ", type(data_genre_livre_selected))
            print(" data data_genres_livres_non_attribues ", data_genres_livres_non_attribues, "type ",
                  type(data_genres_livres_non_attribues))
            print(" data_genres_livres_attribues ", data_genres_livres_attribues, "type ",
                  type(data_genres_livres_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "intitule_genre"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_genres_livres_non_attribues = [item['intitule_genre'] for item in data_genres_livres_non_attribues]
            print("lst_all_genres gf_edit_genre_livre_selected ", lst_data_genres_livres_non_attribues,
                  type(lst_data_genres_livres_non_attribues))

        except Exception as Exception_edit_genre_livre_selected:
            raise ExceptionEditGenreLivreSelected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_genre_livre_selected.__name__} ; "
                                                 f"{Exception_edit_genre_livre_selected}")

    return render_template("livres_genres/livres_genres_modifier_tags_dropbox.html",
                           data_genres=data_genres_all,
                           data_livre_selected=data_genre_livre_selected,
                           data_genres_attribues=data_genres_livres_attribues,
                           data_genres_non_attribues=data_genres_livres_non_attribues)


"""
    nom: update_genre_livre_selected

    Récupère la liste de tous les genres du livre sélectionné par le bouton "MODIFIER" de "livres_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au livre selectionné.
    3) Les genres non-attribués au livre sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_genre_livre_selected", methods=['GET', 'POST'])
def update_genre_livre_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du livre sélectionné
            id_livre_selected = session['session_id_livre_genres_edit']
            print("session['session_id_livre_genres_edit'] ", session['session_id_livre_genres_edit'])

            # Récupère la liste des genres qui ne sont pas associés au livre sélectionné.
            old_lst_data_genres_livres_non_attribues = session['session_lst_data_genres_livres_non_attribues']
            print("old_lst_data_genres_livres_non_attribues ", old_lst_data_genres_livres_non_attribues)

            # Récupère la liste des genres qui sont associés au livre sélectionné.
            old_lst_data_genres_livres_attribues = session['session_lst_data_genres_livres_old_attribues']
            print("old_lst_data_genres_livres_old_attribues ", old_lst_data_genres_livres_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_livres_modifier_tags_dropbox.html"
            new_lst_str_genres_livres = request.form.getlist('name_select_tags')
            print("new_lst_str_genres_livres ", new_lst_str_genres_livres)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_genre_livre_old = list(map(int, new_lst_str_genres_livres))
            print("new_lst_genre_livre ", new_lst_int_genre_livre_old, "type new_lst_genre_livre ",
                  type(new_lst_int_genre_livre_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_genre_livre".
            lst_diff_genres_delete_b = list(set(old_lst_data_genres_livres_attribues) -
                                            set(new_lst_int_genre_livre_old))
            print("lst_diff_genres_delete_b ", lst_diff_genres_delete_b)

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_genre_livre"
            lst_diff_genres_insert_a = list(
                set(new_lst_int_genre_livre_old) - set(old_lst_data_genres_livres_attribues))
            print("lst_diff_genres_insert_a ", lst_diff_genres_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_livre"/"id_livre" et "fk_genre"/"id_genre" dans la "t_genre_livre"
            strsql_insert_genre_livre = """INSERT INTO t_genre_livre (id_genre_livre, fk_genre, fk_livre)
                                                    VALUES (NULL, %(value_fk_genre)s, %(value_fk_livre)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_livre" et "id_genre" dans la "t_genre_livre"
            strsql_delete_genre_livre = """DELETE FROM t_genre_livre WHERE fk_genre = %(value_fk_genre)s AND fk_livre = %(value_fk_livre)s"""

            with DBconnection() as mconn_bd:
                # Pour le livre sélectionné, parcourir la liste des genres à INSÉRER dans la "t_genre_livre".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_ins in lst_diff_genres_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du livre sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_livre_sel_genre_sel_dictionnaire = {"value_fk_livre": id_livre_selected,
                                                               "value_fk_genre": id_genre_ins}

                    mconn_bd.execute(strsql_insert_genre_livre, valeurs_livre_sel_genre_sel_dictionnaire)

                # Pour le livre sélectionné, parcourir la liste des genres à EFFACER dans la "t_genre_livre".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_del in lst_diff_genres_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du livre sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_livre_sel_genre_sel_dictionnaire = {"value_fk_livre": id_livre_selected,
                                                               "value_fk_genre": id_genre_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_genre_livre, valeurs_livre_sel_genre_sel_dictionnaire)

        except Exception as Exception_update_genre_livre_selected:
            raise ExceptionUpdateGenreLivreSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{update_genre_livre_selected.__name__} ; "
                                                   f"{Exception_update_genre_livre_selected}")

    # Après cette mise à jour de la table intermédiaire "t_genre_livre",
    # on affiche les livres et le(urs) genre(s) associé(s).
    return redirect(url_for('livres_genres_afficher', id_livre_sel=id_livre_selected))


"""
    nom: genres_livres_afficher_data

    Récupère la liste de tous les genres du livre sélectionné par le bouton "MODIFIER" de "livres_genres_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


def genres_livres_afficher_data(valeur_id_livre_selected_dict):
    print("valeur_id_livre_selected_dict...", valeur_id_livre_selected_dict)
    try:

        strsql_livre_selected = """SELECT id_livre, nom_livre, page_livre, description_livre, cover_link_livre, date_sortie_livre, GROUP_CONCAT(id_genre) as GenresLivres FROM t_genre_livre
                                        INNER JOIN t_livre ON t_livre.id_livre = t_genre_livre.fk_livre
                                        INNER JOIN t_genre ON t_genre.id_genre = t_genre_livre.fk_genre
                                        WHERE id_livre = %(value_id_livre_selected)s"""

        strsql_genres_livres_non_attribues = """SELECT id_genre, intitule_genre FROM t_genre WHERE id_genre not in(SELECT id_genre as idGenresLivres FROM t_genre_livre
                                                    INNER JOIN t_livre ON t_livre.id_livre = t_genre_livre.fk_livre
                                                    INNER JOIN t_genre ON t_genre.id_genre = t_genre_livre.fk_genre
                                                    WHERE id_livre = %(value_id_livre_selected)s)"""

        strsql_genres_livres_attribues = """SELECT id_livre, id_genre, intitule_genre FROM t_genre_livre
                                            INNER JOIN t_livre ON t_livre.id_livre = t_genre_livre.fk_livre
                                            INNER JOIN t_genre ON t_genre.id_genre = t_genre_livre.fk_genre
                                            WHERE id_livre = %(value_id_livre_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_livres_non_attribues, valeur_id_livre_selected_dict)
            # Récupère les données de la requête.
            data_genres_livres_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("genres_livres_afficher_data ----> data_genres_livres_non_attribues ", data_genres_livres_non_attribues,
                  " Type : ",
                  type(data_genres_livres_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_livre_selected, valeur_id_livre_selected_dict)
            # Récupère les données de la requête.
            data_livre_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_livre_selected  ", data_livre_selected, " Type : ", type(data_livre_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_livres_attribues, valeur_id_livre_selected_dict)
            # Récupère les données de la requête.
            data_genres_livres_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_genres_livres_attribues ", data_genres_livres_attribues, " Type : ",
                  type(data_genres_livres_attribues))

            # Retourne les données des "SELECT"
            return data_livre_selected, data_genres_livres_non_attribues, data_genres_livres_attribues

    except Exception as Exception_genres_livres_afficher_data:
        raise ExceptionGenresLivresAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{genres_livres_afficher_data.__name__} ; "
                                               f"{Exception_genres_livres_afficher_data}")
