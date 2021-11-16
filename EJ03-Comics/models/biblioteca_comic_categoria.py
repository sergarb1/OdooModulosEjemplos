# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'biblioteca.comic.categoria'
    _description = 'Categoria de comics de la biblioteca'

    _parent_store = True
    _parent_name = "parent_id"

    nombre = fields.Char('Categoria')
    parent_id = fields.Many2one(
        'biblioteca.comic.categoria',
        string='Categoria padre',
        ondelete='restrict',
        index=True
    )
    child_ids = fields.One2many(
        'biblioteca.comic.categoria', 'parent_id',
        string='Categorias hijas')
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('¡Error! No puedes crear categorias recursivas.')