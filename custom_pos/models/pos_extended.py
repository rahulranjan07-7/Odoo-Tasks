from functools import partial
from odoo import models, fields, api

class InheritPos(models.Model):
    _description = 'Inherited POS model'
    _inherit = ['pos.order']
    

    phone_number = fields.Char(string='Phone Number')

    @api.model
    def _order_fields(self, ui_order):
        process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])
        order_vals = super(InheritPos, self)._order_fields(ui_order)
        order_vals.update({
            'phone_number': ui_order.get('customer_phone_number', ''),
        })
        return order_vals
