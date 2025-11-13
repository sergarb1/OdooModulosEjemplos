# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# ------------------------------------------------------------------------------
# MODELO SOCIO
# Este modelo almacena información de los socios de una organización.
# ------------------------------------------------------------------------------

class Socio(models.Model):
    _name = 'socio'  # Nombre técnico del modelo
    _description = 'Modelo para almacenar socios'
    _order = 'nombre'  # Orden por defecto al listar los registros

    # ---------------------------------------------
    # _rec_name indica qué campo se mostrará como nombre del registro
    # en los campos many2one y listas desplegables.
    # ---------------------------------------------
    _rec_name = 'nombre'  # Usamos 'nombre' como identificador legible

    # ---------------------------------------------
    # DEFINICIÓN DE CAMPOS
    # ---------------------------------------------

    # Número único de socio (clave externa lógica, no técnica)
    num_socio = fields.Integer("Número de socio", required=True)

    # Nombre del socio
    nombre = fields.Char("Nombre", required=True, index=True)

    # Apellidos del socio
    apellidos = fields.Char("Apellidos", required=True, index=True)

    # Imagen de perfil del socio
    foto = fields.Image("Foto del socio", max_width=100, max_height=100)

    # Imagen del código de barras del carnet
    barcode_carnet = fields.Image("Código de barras del carnet", max_width=100, max_height=100)

    # ---------------------------------------------
    # CONSTRAINTS DE BASE DE DATOS (nivel SQL)
    # ---------------------------------------------
    _sql_constraints = [
        (
            'socio_uniq',               # Nombre de la constraint
            'UNIQUE (num_socio)',      # Regla SQL: num_socio debe ser único
            'El número de socio debe ser único.'  # Mensaje de error en caso de conflicto
        ),
    ]

    # ---------------------------------------------
    # VALIDACIONES ADICIONALES (opcional)
    # Puedes agregar validaciones personalizadas aquí con @api.constrains
    # ---------------------------------------------
    # @api.constrains('nombre', 'apellidos')
    # def _check_nombre_apellidos(self):
    #     if not self.nombre or not self.apellidos:
    #         raise ValidationError("Debe completar nombre y apellidos.")
