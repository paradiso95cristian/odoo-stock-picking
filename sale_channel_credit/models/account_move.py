from odoo import fields, models,api


class AccountMove(models.Model):

    _inherit = 'account.move'

    sale_channel_id = fields.Many2one('sale.channel')
    amount_total_currency = fields.Monetary(string='Total currency', compute='compute_amount_currency')
    
    @api.depends('amount_total', 'currency_id')
    def compute_amount_currency(self):
        for invoice in self:
            if invoice.company_currency_id and invoice.company_currency_id != invoice.currency_id:
                invoice.amount_total_currency = invoice.amount_residual * invoice.company_currency_id.rate
            else:
                invoice.amount_total_currency = invoice.amount_residual
