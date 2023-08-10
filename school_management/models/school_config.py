from odoo import models, fields, api

class SchoolSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    director_name = fields.Char(string='Director Name')
    school_estd_date = fields.Date(string='Establish Date')
    admission_fee = fields.Integer(string='Admission Fee')
    school_open = fields.Boolean(string='School Open Today', default=True)
    is_registered = fields.Boolean(string='Is Registered', default=True)
    registration_number = fields.Char(string='Registration Number')

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].set_param('my_module.director_name', self.director_name or '')
        self.env['ir.config_parameter'].set_param('my_module.school_estd_date', str(self.school_estd_date) or '')
        self.env['ir.config_parameter'].set_param('my_module.admission_fee', str(self.admission_fee) or '')
        self.env['ir.config_parameter'].set_param('my_module.school_open', str(self.school_open))
        self.env['ir.config_parameter'].set_param('my_module.is_registered', str(self.is_registered))
        self.env['ir.config_parameter'].set_param('my_module.registration_number', self.registration_number or '')

    @api.model
    def get_values(self):
        director_name = self.env['ir.config_parameter'].sudo().get_param('my_module.director_name', '')
        school_estd_date = self.env['ir.config_parameter'].sudo().get_param('my_module.school_estd_date', '')
        admission_fee = self.env['ir.config_parameter'].sudo().get_param('my_module.admission_fee', '')
        school_open = self.env['ir.config_parameter'].sudo().get_param('my_module.school_open', 'True') == 'True'
        is_registered = self.env['ir.config_parameter'].sudo().get_param('my_module.is_registered', 'True') == 'True'
        registration_number = self.env['ir.config_parameter'].sudo().get_param('my_module.registration_number', '')

        return {
            'director_name': director_name,
            'school_estd_date': school_estd_date,
            'admission_fee' : admission_fee,
            'school_open': school_open,
            'is_registered': is_registered,
            'registration_number' : registration_number,
        }
