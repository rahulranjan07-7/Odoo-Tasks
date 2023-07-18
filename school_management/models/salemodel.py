from odoo import fields, models
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    okay_field = fields.Many2one('res.users', string='okay model')