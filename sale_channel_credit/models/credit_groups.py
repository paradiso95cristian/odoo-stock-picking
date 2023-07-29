from odoo import models, fields


class CreditGroups(models.Model):
    _name = 'credit.groups'
    _description = 'Credit Groups'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    sale_channel_id = fields.Many2one('sale.channel',required=True)
    global_credit = fields.Float(required=True)
    used_credit = fields.Float()
    available_credit = fields.Float(compute='get_available_credit')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('uniq_code', 'unique(code)', "code must be unique"),
    ]

    def get_available_credit(self):
        for group in self:
            client_ids = self.env['res.partner'].search([
                ('control_credit','=',True),
                ('credit_groups_ids','in',group.id)
            ])
            sale_ids = self.env['sale.order'].search([
                ('sale_channel_id','=',group.sale_channel_id.id),
                ('state','=','sale'),
                ('invoice_status','=','to invoice'),
                ('partner_id','in',client_ids.ids)
            ])
            invoice_ids = self.env['account.move'].search([
                ('sale_channel_id','=',group.sale_channel_id.id),
                ('state','!=','cancel'),
                ('partner_id','in',client_ids.ids)
            ])
            sale_total = 0
            invoice_total = 0
            if sale_ids:
                sale_total = sum(sale_ids.mapped('amount_total_currency'))
            if invoice_ids:
                invoice_total = sum(invoice_ids.mapped('amount_total_currency'))
            group.used_credit = sale_total + invoice_total
            group.available_credit = group.global_credit - group.used_credit

    def get_clients(self):
        client_ids = self.env['res.partner'].search([
            ('control_credit','=',True),
            ('credit_groups_ids','in',self.id)
        ])
        return client_ids

    def get_sale(self):
        sale_ids = self.env['sale.order'].search([
            ('sale_channel_id','=',self.sale_channel_id.id),
            ('state','=','sale'),
            ('invoice_status','=','to invoice'),
            ('partner_id','in',self.get_clients().ids)
        ])
        return sale_ids

    def get_invoice(self):
        invoice_ids = self.env['account.move'].search([
            ('sale_channel_id','=',self.sale_channel_id.id),
            ('state','!=','cancel'),
            ('partner_id','in',self.get_clients().ids)
        ])
        return invoice_ids