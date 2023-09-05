from odoo import models, fields,api
from odoo.exceptions import ValidationError

class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    new_phone_number = fields.Char(string="New Phone Number")


    

    @api.constrains('new_phone_number')
    def _check_unique_mobile(self):
        records = self.env['res.partner']
        for order in self:
            if order.new_phone_number:
                duplicate_orders = records.search_count([['new_phone_number', '=', order.new_phone_number],['id', '!=', order.id]])
                
                if duplicate_orders>0 :
                    raise ValidationError("Phone number must be unique per customer.")
            