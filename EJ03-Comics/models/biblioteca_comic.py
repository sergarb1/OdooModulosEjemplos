# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Fichero abstracto'

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class Bibliotecacomic(models.Model):
    _name = 'biblioteca.comic'
    _inherit = ['base.archive']

    _description = 'Comic de biblioteca'

    _order = 'fecha_publicacion desc, name'

    name = fields.Char('Titulo', required=True, index=True)
    short_name = fields.Char('Titulo Corto',translate=True, index=True)
    notes = fields.Text('Anotaciones Internas')
    state = fields.Selection(
        [('borrador', 'No disponible'),
         ('disponible', 'Disponible'),
         ('perdido', 'Perdido')],
        'State', default="borrador")
    description = fields.Html('Descripcion', sanitize=True, strip_style=False)
    cover = fields.Binary('Cubierta Comic')
    fecha_publicacion = fields.Date('Fecha publicación')
    fecha_actualizacion = fields.Datetime('Última actualización', copy=False)
    pages = fields.Integer('Numero de páginas',
        groups='base.group_user',
        states={'perdido': [('readonly', True)]},
        help='Total numero de paginast', company_dependent=False)
    reader_rating = fields.Float(
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
    
    ciudad_editorial = fields.Char('Ciudad Editorial', related='publisher_id.city', readonly=True)

    category_id = fields.Many2one('biblioteca.comic.categoria')
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

    @api.depends('date_release')
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
            comic.date_release = d

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
        ('positive_page', 'CHECK(pages>0)', 'No of pages must be positive')
    ]

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('La fecha de lanzamiento debe estar en el pasado')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    editorial_comics_ids = fields.One2many('biblioteca.comic', 'editorial_id', string='Comics editorial')
    autores_comics_ids = fields.Many2many(
        'biblioteca.comic',
        string='Autores de Comics',
        # relation='biblioteca_comic_res_partner_rel'  # opcional
    )

    cuenta_comics = fields.Integer('Number de comics del autor', compute='_compute_cuenta_comics')

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