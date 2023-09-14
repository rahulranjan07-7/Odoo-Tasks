from odoo import http
from odoo.http import request

class Hello(http.Controller):
    @http.route('/rahul/ranjan/',website = True, auth = 'public')
    def know_ledge(self,**kw):
        students = request.env['school.management.student'].sudo().search([])
        return request.render("school_management.new_page", {
            'students': students
        })