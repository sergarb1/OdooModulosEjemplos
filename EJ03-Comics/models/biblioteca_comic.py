# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


# Modelo base, creado como modelo abstracto (Fin didáctico)
class BaseArchive(models.AbstractModel):
    #Nombre y descripcion del modelo
    _name = 'base.archive'
    _description = 'Fichero abstracto'

    #Introduce el atributo "Activo"
    activo = fields.Boolean(default=True)

    #Introducice metodo "archivar" que invierte el estado de "activo"
    def archivar(self):
        for record in self:
            record.activo = not record.activo


#Definimos modelo Biblioteca comic
class BibliotecaComic(models.Model):

    #Nombre y descripcion del modelo
    _name = 'biblioteca.comic'
    #Hereda de "base.archive" (el modelo abstracto creado antes)
    _inherit = ['base.archive']

    _description = 'Comic de biblioteca'

    #Parametros de ordenacion por defecto
    _order = 'fecha_publicacion desc, nombre'

    #ATRIBUTOS

    #Atributo nombre
    nombre = fields.Char('Titulo', required=True, index=True)
    #Atributo para seleccionar entre varios
    estado = fields.Selection(
        [('borrador', 'No disponible'),
         ('disponible', 'Disponible'),
         ('perdido', 'Perdido')],
        'Estado', default="borrador")
    #Campo con HTML (Sanitizado) donde se guarda la descripción del comic
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)
    #Dato binario, para guardar un binario (en la vista indicaremos que es una imagen) con la portada del comic
    portada = fields.Binary('Portada Comic')

    #Fecha de publicación
    fecha_publicacion = fields.Date('Fecha publicación')

    #Precio del libro    
    precio = fields.Float('Precio')
    #Numero de paginas. 
    paginas = fields.Integer('Numero de páginas',
        #Por comentar 
        grupos='base.group_user',
        #Si esta perdido, el numero de paginas no se puede cambiar
        estados={'perdido': [('readonly', True)]},
        help='Total numero de paginas', company_dependent=False)
 
    #Valoración lector, indicando como son los datos
    valoracion_lector = fields.Float(
        'Valoración media lectores',
        digits=(14, 4),  # Precision opcional (total, decimales),
    )
    # Relación muchos a muchos de autores utilizando un "partner"
    # de Odoo (Es un elemento que puede ser empresa o individuo)
    autor_ids = fields.Many2many('res.partner', string='Autores')

    # Relación muchos a uno utilizando un "partner"
    # de Odoo (Es un elemento que puede ser empresa o individuo)

    editorial_id = fields.Many2one('res.partner', string='Editorial',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )

    #Relacion muchos a uno con el modelo de las categorias
    categoria_id = fields.Many2one('biblioteca.comic.categoria')
    
    #Variable computada para calcular dias desde el lanzamiento
    dias_lanzamiento = fields.Integer(
        string='Dias desde lanzamiento',
        compute='_compute_anyo', inverse='_inverse_anyo', search='_search_anyo',
        store=False,
        compute_sudo=True,
    )

    #Para poder meter referencias a elementos de Odoo (por ejemplo, una factura) como 
    #un dato del modelo. Para saber que documentos, usa "referencable_models"
    ref_doc_id = fields.Reference(selection='_referencable_models', string='Referencia a documento')

    #Funcion usada para obtener que elementos pueden ser refernciados 
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]


    #Funciones para computar "Dias desde lanzamiento"
    @api.depends('fecha_publicacion')
    def _compute_anyo(self):
        hoy = fields.Date.today()
        for comic in self:
            if comic.fecha_publicacion:
                delta = hoy - comic.fecha_publicacion
                comic.dias_lanzamiento = delta.days
            else:
                comic.dias_lanzamiento = 0

    def _inverse_anyo(self):
        hoy = fields.Date.today()
        for comic in self.filtered('fecha_publicacion'):
            d = hoy - timedelta(days=comic.dias_lanzamiento)
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


    #Constraints de SQL del modelo
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'El titulo Comic debe ser único.'),
        ('positive_page', 'CHECK(paginas>0)', 'El comic debe tener al menos una página')
    ]

    #Constraints de atributos
    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise models.ValidationError('La fecha de lanzamiento debe ser anterior a la actual')


