from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SchoolPayments(models.Model):
    _name = 'school.payments'
    _inherit = 'mail.thread'
    _description = 'School Payments'
    _log_access = False

    name_enroll = fields.Many2one('school.management.student', 
                                  string = 'Name and Enroll.', required=True, tracking=True)
    
    amount = fields.Char(string= 'Paid amount', required=True, tracking=True)

    payment_status=fields.Selection([
        ('paid',"Paid"),
        ('half paid',"Half Paid"),
        ('unpaid',"Unpaid"),
    ],string="Payment Status", required=True, tracking=True)
    
    student_dig_sign= fields.Char(string='Student E-Sign', required=True)

    @api.ondelete(at_uninstall=False)
    def _check_payments(self):
        for rec in self:
            if rec.amount:
                raise ValidationError ('You cannot delete a payment form containing paid amount.')

    def change_status_to_fee_paid(self):
        for rec in self:
            rec.payment_status = 'paid'