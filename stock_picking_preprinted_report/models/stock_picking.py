from odoo import models,fields,api
from datetime import date


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    stated_value = fields.Float(compute='_compute_stated_value',string="Valor declarado")   
    purchase_order = fields.Char(string="OC Nº")
    express_address_id = fields.Many2one('res.partner',string="Dirección de expreso")

    @api.depends('origin')
    def _compute_stated_value(self):
        for record in self:
            stated_value = False
            if record.origin:
                sale_order = self.env['sale.order'].search([('name','=',record.origin)])
                if sale_order:
                    total = 0
                    for line in sale_order.order_line:
                        total += line.product_uom_qty * line.price_unit
                    stated_value = total
            record.stated_value = stated_value


    def get_weight(self):
        for picking in self:
            total = 0
            if picking.move_line_ids_without_package:
                for line in picking.move_line_ids_without_package:
                    total += line.total_weight
            return total
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

