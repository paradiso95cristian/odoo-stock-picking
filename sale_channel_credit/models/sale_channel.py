from odoo import models, fields


class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Sale Channel'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    deposit_id = fields.Many2one('stock.warehouse')
    journal_id = fields.Many2one('account.journal')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('uniq_code', 'unique(code)', "code must be unique"),
    ]