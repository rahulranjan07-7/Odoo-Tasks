from odoo import models, fields, api

class CreateSchoolInfoWizard(models.TransientModel):
    _name = 'create_school_info.wizard'
    _description = 'Create School Info Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CreateSchoolInfoWizard, self).default_get(fields)
        print("Default Get Executed", res)
        res["principal_name"] = "Principal Name"
        return res

    name = fields.Char(string='Name', required=True)

    principal_name = fields.Char(string='Principal Name', default= 'Mitesh Jayswal', readonly="1")

    address = fields.Char(string='Address', required=True)
    
    info_creation_date = fields.Date(string='Creation Date')

    def create_school(self):
        return