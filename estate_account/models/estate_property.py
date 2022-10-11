import logging
from odoo import models, fields, api, tools, _
from odoo.exceptions import AccessError, UserError

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self._create_invoices()

        return super().action_sold()

    def _prepare_invoice(self):
        self.ensure_one()
        _logger.error("Prepare Invoice")
        journal = self.env['account.journal'].search([('code', '=', 'INV')], limit=1)

        if not journal:
            raise UserError("Journal Error")
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'journal_id': journal.id,
        }
        return invoice_vals

    def _create_invoices(self):
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        invoice_vals_list = []
        for order in self:
            invoice_vals = order._prepare_invoice()

            invoice_vals['invoice_line_ids'] = [
                (0, 0,
                 {
                     'name': self.name,
                     'sequence': 0,
                     'quantity': 1,
                     'price_unit': self.selling_price * 0.06
                 }
                 ),
                (0, 0,
                 {
                     'name': 'Administration Fee',
                     'sequence': 1,
                     'quantity': 1,
                     'price_unit': 100,
                 })
            ]

            invoice_vals_list.append(invoice_vals)

        # Create invoices
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
        return moves
