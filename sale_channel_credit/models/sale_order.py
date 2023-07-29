from odoo import models, fields, _, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    sale_channel_id = fields.Many2one('sale.channel',required=True)
    credit = fields.Selection([
        ('credit_without_limits', 'Credit Without Limits'),
        ('credit_available', 'Credit Available'),
        ('blocked_credit', 'Blocked Credit')
        ], default = 'credit_without_limits'
    )
    amount_total_currency = fields.Monetary(string='Total currency', compute='compute_amount_currency')

    @api.onchange('sale_channel_id')
    def _onchange_sale_channel_id(self):
        for sale in self:
            if sale.sale_channel_id and sale.sale_channel_id.deposit_id:
                sale.warehouse_id = sale.sale_channel_id.deposit_id.id

    def action_confirm(self):
        res = super().action_confirm()
        for sale in self:
            if sale.credit == 'blocked_credit':
                raise UserError(
                    _("You cant confirm the sale if the value of the Credit field is Credit locked")
                )
            if sale.picking_ids:
                for picking in sale.picking_ids:
                    picking.sale_channel_id = sale.sale_channel_id.id
        return res

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        if self.sale_channel_id:
            res['sale_channel_id'] = self.sale_channel_id.id
            if self.sale_channel_id.journal_id:
                res['journal_id'] = self.sale_channel_id.journal_id.id
        return res

    
    @api.depends('amount_total', 'currency_id')
    def compute_amount_currency(self):
        for sale in self:
            if sale.company_id.currency_id and sale.company_id.currency_id != sale.currency_id:
                sale.amount_total_currency = sale.amount_total * sale.company_id.currency_id.rate
            else:
                sale.amount_total_currency = sale.amount_total

    @api.onchange('sale_channel_id','partner_id','amount_total')
    def _onchange_sale_channel_id(self):
        for sale in self:
            if sale.sale_channel_id and sale.partner_id and sale.partner_id.control_credit:
                group = self.env['credit.groups'].search([('sale_channel_id','=',sale.sale_channel_id.id),('id','in',sale.partner_id.credit_groups_ids.ids)],limit=1)
                if group:
                    if group.available_credit >= sale.amount_total_currency:
                        sale.credit = 'credit_available'
                    else:
                        sale.credit = 'blocked_credit' 