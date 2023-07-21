from odoo import models, fields

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    total_weight = fields.Float(compute='get_weight')

    def get_weight(self):
        for line in self:
            line.total_weight = line.product_id.weight * line.qty_done

