from odoo import http

class EmployeeDetails(http.Controller):

    @http.route('/employee/', auth = 'public', type = 'json', methods = ['POST'])
    def all_employees(self):
        employee = http.request.env['employee.details'].search_read([],['emp_name', 'emp_image', 'emp_phone_number', 'emp_work_exp', 'emp_city'])
        return employee