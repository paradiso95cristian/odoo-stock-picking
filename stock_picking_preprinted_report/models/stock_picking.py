from odoo import models
from datetime import date


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def create_template_report(self):
        return self.env.ref('stock_picking_preprinted_report.action_report_preprinted_report').report_action(self)

    def today(self):
        today = date.today()
        return today

    def get_payment_term(self):
        sale_order_id = self.env['sale.order'].search([('name','=',self.origin)])
        if sale_order_id and sale_order_id.payment_term_id:
            return sale_order_id.payment_term_id.name
        else:
            return ""