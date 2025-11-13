# -*- coding: utf-8 -*-

# Importación de las clases base
from odoo import models, fields

# ======================================================
# MODELO DE CATEGORÍA DE CÓMIC
# ======================================================
class BibliotecaComicCategoria(models.Model):
    _name = 'biblioteca.comic.categoria'  # Nombre técnico del modelo
    _description = 'Categoría de cómics'

    # ======================================================
    # CAMPOS DEL MODELO
    # ======================================================

    nombre = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la categoría (por ejemplo: Superhéroes, Manga, Ciencia Ficción, etc.)'
    )

    descripcion = fields.Text(
        string='Descripción',
        help='Descripción de la categoría.'
    )

    # ======================================================
    # RELACIÓN INVERSA (opcional)
    # Permite ver qué cómics pertenecen a esta categoría
    # ======================================================
    comic_ids = fields.One2many(
        comodel_name='biblioteca.comic',
        inverse_name='categoria_id',
        string='Cómics en esta categoría'
    )
