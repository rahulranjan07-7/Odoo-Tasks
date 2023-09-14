from odoo import models, fields

class Employees(models.Model):
    _name = 'employee.details'
    _description = 'Employee Details'


    emp_name = fields.Char(string='Employee Name')
    emp_image = fields.Binary(string='Employee Image')
    emp_phone_number = fields.Char(string='Employee Phone Number')
    emp_work_exp = fields.Char(string='Employee Work Exp.')
    emp_city = fields.Char(string='Employee City')