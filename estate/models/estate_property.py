from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Some information about estate properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('sout', 'South'), ('west', 'West'),
                                                     ('east', 'East')])

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')], default='new')

    # Relations
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    #
    # # Computed fields
    # total_area = fields.Integer(compute="_compute_total_area")
    # best_price = fields.Float(compute="_compute_best_price")
    #
    # @api.depends("living_area", "garden_area")
    # def _compute_total_area(self):
    #     for record in self:
    #         record.total_area = record.living_area + record.garden_area
    #
    # @api.depends("offer_ids.price")
    # def _compute_best_price(self):
    #     for record in self:
    #         best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0
    #         record.best_price = best_price
    #
    # @api.onchange("garden")
    # def _onchange_garden(self):
    #     if self.garden:
    #         self.garden_area = 10
    #         self.garden_orientation = "north"
    #     else:
    #         self.garden_area = None
    #         self.garden_orientation = None
    #
    # def action_sold(self):
    #     for record in self:
    #         if record.state == 'canceled':
    #             raise UserError("Canceled properties cannot be sold.")
    #         record.state = 'sold'
    #
    # def action_canceled(self):
    #     for record in self:
    #         if record.state == 'sold':
    #             raise UserError("Property already sold.")
    #         record.state = 'canceled'
    #
    # @api.constrains('selling_price')
    # def _check_selling_price(self):
    #     for record in self:
    #         if tools.float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1:
    #             raise ValidationError("Selling price is below 90% of expected price!")
    #
    # def unlink(self):
    #     for record in self:
    #         if record.state not in ["new", "canceled"]:
    #             raise UserError("Only new and canceled can be deleted!")
    #
    #     return super().unlink()