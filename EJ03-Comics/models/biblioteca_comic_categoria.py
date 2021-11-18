# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    #Nombre y descripcion del modelo
    _name = 'biblioteca.comic.categoria'
    _description = 'Categoria de comics de la biblioteca'

    #Para guardar lo del padre y acelerar consultas
    # https://www.odoo.com/documentation/14.0/es/developer/reference/addons/orm.html#odoo.models.BaseModel._parent_store
    _parent_store = True
    #ID que indica el padre de este modelo
    _parent_name = "parent_id"

    #Atributos del modelo

    #Nombre categoria
    nombre = fields.Char('Categoria')
    #ID de la categoría padre (relación muchos a uno con este mismo modelo)
    parent_id = fields.Many2one(
        'biblioteca.comic.categoria',
        string='Categoria padre',
        ondelete='restrict',
        index=True
    )
    #ID de las categorias hijas (Relacion uno a muchos con este mismo modelo)
    child_ids = fields.One2many(
        'biblioteca.comic.categoria', 'parent_id',
        string='Categorias hijas')
    parent_path = fields.Char(index=True)

    #Decorador para introducir "constraints" https://odoo-development.readthedocs.io/en/latest/dev/py/constraints.html
    @api.constrains('parent_id')
    #Comprueba que no haya categorias recursivas
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('¡Error! No puedes crear categorias recursivas.')


