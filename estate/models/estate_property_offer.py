import logging

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    # validity = fields.Integer(default=7)

    # Computed fields
    # date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Relations
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')
    # property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string='Property Type')

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Datetime.now()
            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'offer accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'

    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(vals['property_id']).state = 'offer received'

        return super().create(vals)
