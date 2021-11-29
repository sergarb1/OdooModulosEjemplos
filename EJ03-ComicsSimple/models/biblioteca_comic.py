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

    #PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR NOMBRE DE UN REGISTRO
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
    #Indicamos que atributo sera el que se usara para mostrar nombre.
    #Por defecto es "name", pero si no hay un atributo que se llama name, aqui lo indicamos
    #Aqui indicamos que se use el atributo "nombre"
    _rec_name = 'nombre'
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
    # https://stackoverflow.com/questions/22927605/what-is-res-partner
    autor_ids = fields.Many2many('res.partner', string='Autores')

    #Constraints de SQL del modelo
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El titulo Comic debe ser único.'),
        ('positive_page', 'CHECK(paginas>0)', 'El comic debe tener al menos una página')
    ]

    #Constraints de atributos
    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise models.ValidationError('La fecha de lanzamiento debe ser anterior a la actual')


