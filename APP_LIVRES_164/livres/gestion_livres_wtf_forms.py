"""Gestion des formulaires avec WTF pour les livres
Fichier : gestion_livres_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddLivre(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_livre_regexp = ""
    nom_livre_add_wtf = StringField("Nom du livre ", validators=[Length(min=2, max=2000, message="min 2 max 20"),
                                                               Regexp(nom_livre_regexp,
                                                                      message="Pas de chiffres, de caractères "
                                                                              "spéciaux, "
                                                                              "d'espace à double, de double "
                                                                              "apostrophe, de double trait union")
                                                               ])

    submit = SubmitField("Enregistrer livre")


class FormWTFUpdateLivre(FlaskForm):
    """
        Dans le formulaire "livre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    nom_livre_update_wtf = StringField("Clavioter le titre", widget=TextArea())
    page_livre_update_wtf = IntegerField("Durée du livre (minutes)", validators=[NumberRange(min=1, max=5000,
                                                                                            message=u"Min %(min)d et "
                                                                                                    u"max %(max)d "
                                                                                                    u"Selon Wikipédia "
                                                                                                    u"L'Incendie du "
                                                                                                    u"monastère du "
                                                                                                    u"Lotus rouge "
                                                                                                    u"durée 1620 "
                                                                                                    u"min")])

    description_livre_update_wtf = StringField("Description du livre ", widget=TextArea())
    cover_link_livre_update_wtf = StringField("Lien de l'affiche du livre ", widget=TextArea())
    datesortie_livre_update_wtf = DateField("Date de sortie du livre", validators=[InputRequired("Date obligatoire"),
                                                                                 DataRequired("Date non valide")])
    submit = SubmitField("Update livre")


class FormWTFDeleteLivre(FlaskForm):
    """
        Dans le formulaire "livre_delete_wtf.html"

        nom_livre_delete_wtf : Champ qui reçoit la valeur du livre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "livre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_livre".
    """
    nom_livre_delete_wtf = StringField("Effacer ce livre")
    submit_btn_del_livre = SubmitField("Effacer livre")
    submit_btn_conf_del_livre = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
