from odoo import models, fields,api
from odoo.exceptions import ValidationError

class PartnerDetailsSession(models.Model):
    _inherit ="pos.session"
    
    @api.model
    def _loader_params_res_partner(self):
        params = super(PartnerDetailsSession, self)._loader_params_res_partner()
        params['search_params']['fields'].append('new_phone_number')
        return params
        

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result.get('search_params').get('fields').append('qty_available')
        print(result,"=========================")
        return result