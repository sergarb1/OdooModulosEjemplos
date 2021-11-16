# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Fichero abstracto'

    activo = fields.Boolean(default=True)

    def archivar(self):
        for record in self:
            record.activo = not record.activo


class BibliotecaComic(models.Model):
    _name = 'biblioteca.comic'
    _inherit = ['base.archive']

    _description = 'Comic de biblioteca'

    _order = 'fecha_publicacion desc, nombre'

    nombre = fields.Char('Titulo', required=True, index=True)
    nombre_corto = fields.Char('Titulo corto',translate=True, index=True)
    anotaciones = fields.Text('Anotaciones internas')
    estado = fields.Selection(
        [('borrador', 'No disponible'),
         ('disponible', 'Disponible'),
         ('perdido', 'Perdido')],
        'State', default="borrador")
    descripcion = fields.Html('Descripcion', sanitize=True, strip_style=False)
    cubierta = fields.Binary('Cubierta Comic')
    fecha_publicacion = fields.Date('Fecha publicación')
    fecha_actualizacion = fields.Datetime('Última actualización', copy=False)
    paginas = fields.Integer('Numero de páginas',
        grupos='base.group_user',
        estados={'perdido': [('readonly', True)]},
        help='Total numero de paginast', company_dependent=False)
    valoracion_lector = fields.Float(
        'Valoración media lectores',
        digits=(14, 4),  # Precision opcional (total, decimales),
    )
    autor_ids = fields.Many2many('res.partner', string='Autores')
    precio_coste = fields.Float('Coste Comic', digits='Precio Comic')
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary('Retail Price') # optional attribute: currency_field='currency_id' incase currency field have another name then 'currency_id'

    editorial_id = fields.Many2one('res.partner', string='Editorial',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    
    editorial_ciudad = fields.Char('Ciudad Editorial', related='editorial_id.city', readonly=True)

    categoria_id = fields.Many2one('biblioteca.comic.categoria')
    anyo_dias = fields.Float(
        string='Dias desde lanzamiento',
        compute='_compute_anyo', inverse='_inverse_anyo', search='_search_anyo',
        store=False,
        compute_sudo=True,
    )

    ref_doc_id = fields.Reference(selection='_referencable_models', string='Referencia a documento')

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    @api.depends('fecha_publicacion')
    def _compute_anyo(self):
        hoy = fields.Date.today()
        for comic in self:
            if comic.fecha_publicacion:
                delta = hoy - comic.fecha_publicacion
                comic.anyo_dias = delta.dias
            else:
                comic.anyo_dias = 0

    def _inverse_anyo(self):
        hoy = fields.Date.today()
        for comic in self.filtered('fecha_publicacion'):
            d = hoy - timedelta(days=comic.anyo_dias)
            comic.fecha_publicacion = d

    def _search_age(self, operator, value):
        hoy = fields.Date.today()
        value_dias = timedelta(dias=value)
        value_fecha = hoy - value_dias
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('fecha_publicacion', new_op, value_fecha)]

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.nombre, record.fecha_publicacion)
            result.append((record.id, rec_name))
        return result

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'),
        ('positive_page', 'CHECK(paginas>0)', 'El comic debe tener al menos una página')
    ]

    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise models.ValidationError('La fecha de lanzamiento debe ser anterior a la actual')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    editorial_comics_ids = fields.One2many('biblioteca.comic', 'editorial_id', string='Comics editorial')
    autores_comics_ids = fields.Many2many(
        'biblioteca.comic',
        string='Autores de Comics',
        # relation='biblioteca_comic_res_partner_rel'  # opcional
    )

    cuenta_comics = fields.Integer('Numero de Comics del autor', compute='_compute_cuenta_comics')

    @api.depends('autores_comics_ids')
    def _compute_cuenta_comics(self):
        for r in self:
            r.cuenta_comics = len(r.autores_comics_ids)


class BibliotecaMiembro(models.Model):
    _name = 'biblioteca.miembro'
    _inherits = {'res.partner': 'partner_id'}

    _description = 'Miembro biblioteca'

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    fecha_inicio = fields.Date('Miembro desde')
    fecha_fin = fields.Date('Fecha finalización')
    numero_miembro = fields.Char()
    fecha_nacimiento = fields.Date('Fecha de nacimiento')