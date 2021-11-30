# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError



#Definimos modelo Liga Equipo, que almacenara información de cada equipo
class LigaEquipo(models.Model):

    #Nombre y descripcion del modelo
    _name = 'liga.equipo'

    _description = 'Equipo de la liga'

    #Parametros de ordenacion por defecto
    _order = 'nombre'

    #ATRIBUTOS

    #PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR NOMBRE DE UN REGISTRO
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
    #Indicamos que atributo sera el que se usara para mostrar nombre.
    #Por defecto es "name", pero si no hay un atributo que se llama name, aqui lo indicamos
    #Aqui indicamos que se use el atributo "nombre"
    _rec_name = 'nombre'


    #Atributo nombre
    nombre = fields.Char('Nombre equipo', required=True, index=True)
    #Dato binario, para guardar un binario (en la vista indicaremos que es una imagen) con la portada del comic
    escudo = fields.Binary('Escudo equipo')

    #Anyo de fundacion
    fecha_fundacion = fields.Date('Fecha fundación')

    #Campo con HTML (Sanitizado) donde se guarda la descripción del comic
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)
    

    #Constraints de SQL del modelo
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El nombre del equipo.')
    ]

    #Constraints de atributos
    @api.constrains('fecha_fundacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_fundacion and record.fecha_fundacion > fields.Date.today():
                raise models.ValidationError('La fecha de fundación del club debe ser anterior a la actual')


