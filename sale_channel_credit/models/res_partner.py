from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    control_credit = fields.Boolean()
    credit_groups_ids = fields.Many2many('credit.groups')