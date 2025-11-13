# -*- coding: utf-8 -*-

# Importamos los módulos necesarios de Odoo para definir modelos
from odoo import models, fields, api

# Creamos nuestro modelo de datos principal.
# Todos los modelos de Odoo deben heredar de models.Model
class ListaTareas(models.Model):  # Buenas prácticas: nombres de clase en PascalCase (MayúsculaInicial)
    
    # Nombre técnico del modelo. Es como Odoo lo guarda internamente en la base de datos
    _name = 'lista_tareas.lista'

    # Descripción que aparece en la documentación y ayuda
    _description = 'Modelo de la lista de tareas'

    # Indica qué campo se mostrará por defecto como nombre del registro (en vistas y menús desplegables)
    _rec_name = "tarea"

    # Definimos los campos (atributos) que tendrá cada registro de este modelo:

    # Campo de tipo texto (cadena). Será el nombre de la tarea.
    tarea = fields.Char(string="Tarea")

    # Campo de tipo entero. Se usará para indicar la prioridad (ej: 1 a 100)
    prioridad = fields.Integer(string="Prioridad")

    # Campo calculado de tipo booleano. Será True si la prioridad > 10
    # compute indica el método que lo calcula
    # store=True guarda el valor en la base de datos para poder filtrar y ordenar por él
    urgente = fields.Boolean(string="Urgente", compute="_value_urgente", store=True)

    # Campo booleano normal. Será marcado si la tarea ya se realizó.
    realizada = fields.Boolean(string="Realizada")

    # -------------------------------
    # MÉTODO COMPUTADO
    # -------------------------------
    # Este método se ejecuta cada vez que cambie el campo 'prioridad'
    @api.depends('prioridad')
    def _value_urgente(self):
        for record in self:
            # Si la prioridad es mayor que 10, se considera urgente
            record.urgente = record.prioridad > 10
