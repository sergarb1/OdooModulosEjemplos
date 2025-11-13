# -*- coding: utf-8 -*-

# Importaciones necesarias
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


# ==========================================================
# MODELO ABSTRACTO - BaseArchive
# Este modelo NO crea una tabla en la base de datos.
# Se utiliza para heredar funcionalidad común a otros modelos.
# ==========================================================
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Modelo abstracto de archivo (archivable)'

    # Campo booleano que indica si el registro está activo
    activo = fields.Boolean(default=True)

    # Método para alternar el estado de "activo" (lo activa o desactiva)
    def archivar(self):
        for record in self:
            record.activo = not record.activo


# ==========================================================
# MODELO PRINCIPAL - BibliotecaComic
# Representa un cómic dentro del sistema de biblioteca.
# Hereda del modelo abstracto BaseArchive.
# ==========================================================
class BibliotecaComic(models.Model):
    _name = 'biblioteca.comic'
    _description = 'Cómic de la biblioteca'
    _inherit = ['base.archive']  # Herencia del modelo abstracto

    # Orden por defecto: primero los más recientes, luego por nombre
    _order = 'fecha_publicacion desc, nombre'

    # Campo que se usará para mostrar el registro en las vistas Many2One
    _rec_name = 'nombre'

    # ==========================================================
    # CAMPOS BÁSICOS
    # ==========================================================

    nombre = fields.Char(
        string='Título',
        required=True,
        index=True,
        help='Título del cómic.'
    )

    estado = fields.Selection(
        selection=[
            ('borrador', 'No disponible'),
            ('disponible', 'Disponible'),
            ('perdido', 'Perdido'),
        ],
        string='Estado',
        default='borrador',
        help='Estado actual del cómic.'
    )

    descripcion = fields.Html(
        string='Descripción',
        sanitize=True,
        strip_style=False,
        help='Descripción en formato HTML del contenido del cómic.'
    )

    portada = fields.Binary(
        string='Portada del cómic',
        help='Imagen de portada (campo binario).'
    )

    fecha_publicacion = fields.Date(
        string='Fecha de publicación',
        help='Fecha en la que se publicó el cómic.'
    )

    precio = fields.Float(
        string='Precio',
        help='Precio del cómic en euros.'
    )

    paginas = fields.Integer(
        string='Número de páginas',
        groups='base.group_user',  # Visible solo para usuarios normales
        help='Cantidad total de páginas del cómic.',
        company_dependent=False
    )

    valoracion_lector = fields.Float(
        string='Valoración media lectores',
        digits=(14, 4),
        help='Puntuación promedio otorgada por los lectores.'
    )

    # ==========================================================
    # RELACIONES CON OTROS MODELOS
    # ==========================================================

    autor_ids = fields.Many2many(
        'res.partner',
        string='Autores',
        help='Autores del cómic (partners).'
    )

    editorial_id = fields.Many2one(
        'res.partner',
        string='Editorial',
        help='Editorial que ha publicado el cómic.'
    )

    categoria_id = fields.Many2one(
        'biblioteca.comic.categoria',
        string='Categoría',
        help='Categoría a la que pertenece el cómic.'
    )

    # ==========================================================
    # CAMPO COMPUTADO - Días desde el lanzamiento
    # ==========================================================
    dias_lanzamiento = fields.Integer(
        string='Días desde lanzamiento',
        compute='_compute_dias_lanzamiento',    # Cálculo del campo
        inverse='_inverse_dias_lanzamiento',    # Inversa: permite escribir en el campo
        search='_search_dias_lanzamiento',      # Personalización de búsqueda
        store=False,                            # No se almacena en la base de datos
        compute_sudo=True                       # Computa como superusuario
    )

    # ==========================================================
    # REFERENCIA A OTROS MODELOS (genérica)
    # ==========================================================
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Referencia a documento',
        help='Referencia a cualquier documento de Odoo (genérico).'
    )

    @api.model
    def _referencable_models(self):
        """
        Devuelve los modelos que pueden referenciarse (que tienen mensajes).
        """
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    # ==========================================================
    # MÉTODOS COMPUTADOS
    # ==========================================================

    @api.depends('fecha_publicacion')
    def _compute_dias_lanzamiento(self):
        """
        Calcula la cantidad de días desde la fecha de publicación hasta hoy.
        """
        hoy = fields.Date.today()
        for comic in self:
            if comic.fecha_publicacion:
                delta = hoy - comic.fecha_publicacion
                comic.dias_lanzamiento = delta.days
            else:
                comic.dias_lanzamiento = 0

    def _inverse_dias_lanzamiento(self):
        """
        Permite modificar la fecha_publicacion al escribir directamente el campo
        dias_lanzamiento (campo inverso).
        """
        hoy = fields.Date.today()
        for comic in self:
            if comic.dias_lanzamiento is not None:
                nueva_fecha = hoy - timedelta(days=comic.dias_lanzamiento)
                comic.fecha_publicacion = nueva_fecha

    def _search_dias_lanzamiento(self, operator, value):
        """
        Permite buscar por este campo computado (dias_lanzamiento).
        Convierte la comparación a una búsqueda por fecha_publicacion.
        """
        hoy = fields.Date.today()
        fecha_limite = hoy - timedelta(days=value)

        # Invertimos el operador porque más días = fecha más antigua
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('fecha_publicacion', new_op, fecha_limite)]

    # ==========================================================
    # NOMBRE MOSTRADO PERSONALIZADO
    # ==========================================================
    def name_get(self):
        """
        Cambia cómo se muestra cada cómic en los desplegables (Many2One).
        Ejemplo: "Spiderman (2021-06-15)"
        """
        result = []
        for record in self:
            nombre = "%s (%s)" % (record.nombre, record.fecha_publicacion or 'Sin fecha')
            result.append((record.id, nombre))
        return result

    # ==========================================================
    # CONSTRAINTS (REGLAS DE VALIDACIÓN)
    # ==========================================================

    # Constraints SQL — se aplican directamente en base de datos
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El título del cómic debe ser único.'),
        ('positive_page', 'CHECK(paginas>0)', 'El cómic debe tener al menos una página.')
    ]

    # Constraint Python — se ejecuta al guardar
    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        """
        Verifica que la fecha de publicación no sea futura.
        """
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise ValidationError('La fecha de publicación no puede ser en el futuro.')
