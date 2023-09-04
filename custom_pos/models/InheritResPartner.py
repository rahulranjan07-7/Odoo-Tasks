from odoo import models, fields,api
class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    new_phone_number = fields.Char(string="New Phone Number")

    @api.model
    def _order_fields(self,ui_order):
        res=super(InheritResPartner,self)._order_fields(ui_order)
        res.update({
            'new_phone_number':ui_order.get('new_phone_number'),
        })
        return res
