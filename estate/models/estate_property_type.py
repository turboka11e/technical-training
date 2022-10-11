from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = 'name'

    name = fields.Char(required=True)

    property_ids = fields.One2many("estate.property", "property_type_id")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_count_offers")

    @api.depends("offer_ids")
    def _compute_count_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
