from odoo import fields, models, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tags'
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
