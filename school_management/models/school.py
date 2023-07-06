from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class SchoolManagement(models.Model):
    _name = 'school.management.student'
    _inherit = 'mail.thread'
    _description = 'Student'

    
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean('Active', default=True)
    standard_division = fields.Char(string='Standard & Division')
    roll_number = fields.Char(string='Roll Number')
    enrollment_number = fields.Char(string='Enrollment Number', compute='_compute_enrollment_number', store=True)
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    zip_code = fields.Char(string='ZIP Code')
    country_id = fields.Many2one('res.country', default=lambda self: self.env.ref('base.in'), string='Country', readonly= True)
    state_id = fields.Many2one('res.country.state', domain="[('country_id', '=', country_id)]")
    address = fields.Text(string='Address', compute='_compute_address', store=True)
    phone_number = fields.Char(string='Phone Number', required=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    parent_name = fields.Char(string= 'Parent Name')
    parent_phone_number = fields.Char(string='Parent Phone Number')
    relation_with_child = fields.Selection([
        ('Father', 'Father'), 
        ('Mother', 'Mother'), 
        ('Others', 'Others')
    ])

    birth_month = fields.Selection([ 
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
        ], string='Birth Month', compute='_compute_birth_month', store=True) 
    
    @api.depends('date_of_birth') 
    def _compute_birth_month(self): 
        for student in self: 
            if student.date_of_birth: 
                student.birth_month = student.date_of_birth.strftime('%m') 
            else: 
                student.birth_month = False

                
    stream = fields.Selection([
        ('science', 'Science'), 
        ('arts', 'Arts'), 
        ('commerce', 'Commerce')
    ])


    email_address = fields.Char(string = 'Email Address')
    previous_roll_number = fields.Char(string='Old Roll Number')
    admission_date = fields.Date(string='Admission Date')
    leaving_date = fields.Date(string='Leaving Date')
    school_name = fields.Char(string= 'School Name',)
    class_teacher = fields.Many2one('school.management.teacher', string= 'Class Teacher', compute='_onchange_stream', store=True)

    @api.constrains('phone_number')
    def _check_phone_number(self):
        for record in self:
            if record.phone_number and (not record.phone_number.isdigit() or len(record.phone_number) < 10):
                raise ValidationError("Phone number should contain only numeric values and have a maximum length of 10 digits!")
            
            duplicate_records = self.search([('phone_number', '=', record.phone_number), ('id', '!=', record.id)]) 
            if duplicate_records: 
                raise ValidationError("Phone number is already assigned to another student")

    @api.constrains('parent_phone_number')
    def _check_parent_phone_number(self):
        for record in self:
            if record.parent_phone_number and (not record.parent_phone_number.isdigit() or len(record.parent_phone_number) < 10):
                raise ValidationError("Phone number should contain only numeric values and have a maximum length of 10 digits!")

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                date_of_birth = fields.Date.from_string(record.date_of_birth)
                record.age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            else:
                record.age = 0
    
    @api.depends('street', 'city', 'state_id', 'country_id', 'zip_code')
    def _compute_address(self):
        for record in self:
            address_parts = []
            if record.street:
                address_parts.append(record.street)
            if record.city:
                address_parts.append(record.city)
            if record.state_id:
                address_parts.append(record.state_id.name)
            if record.zip_code:
                address_parts.append(record.zip_code)
            record.address = ", ".join(address_parts)

    @api.constrains('zip_code')
    def _check_pincode_format(self):
        for visitor in self:
            if visitor.zip_code and not visitor.zip_code.isdigit() or len(visitor.zip_code) != 6:
                raise ValidationError('Invalid pin code format!')


    @api.constrains('age')
    def _calculate_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                check_age = today.year - record.date_of_birth.year
                if check_age < 4:
                    raise ValidationError('Age cannot be less than 4')
                record.age = check_age
            else:
                record.age = 0   

    @api.depends('name')
    def _compute_enrollment_number(self):
        for record in self:
            if record.name:
                record.enrollment_number = 'ENR' + str(record.id).zfill(6)
            else:
                record.enrollment_number = ''       

    @api.constrains('email_address') 
    def check_email_address(self): 
        for visitor in self: 
            if visitor.email_address and '@' not in visitor.email_address: 
                raise ValidationError("Invalid email address.")

        
    @api.onchange('standard_division')
    def _onchange_standard_division(self):
        if self.standard_division:
            if int(self.standard_division.split(" ")[0]) < 11:
                teacher = self.env['school.management.teacher'].search([
                    ('standard_division', '=', self.standard_division)
                ], limit=1)
                if teacher:
                    self.class_teacher = teacher.id
                else:
                    self.class_teacher = False
            else:
                self.class_teacher = False

    @api.depends('stream')
    def _onchange_stream(self):
        if self.stream:
            print(self.stream, self.standard_division)
            teacher = self.env['school.management.teacher'].search([
                ('stream', '=', self.stream.lower()), ('standard_division', '=', str(self.standard_division))
            ])
            print(teacher)
            if teacher:
                self.class_teacher = teacher.id

            
class SchoolManagementTeacher(models.Model): 
    _name = 'school.management.teacher' 
    _description = 'Teacher'
    
    name = fields.Char(string='Name', required=True)
    standard_division = fields.Char(string='Standard & Division', required=True) 
    stream= fields.Selection(selection=[('science','Science'),
                                        ('commerce','Commerce'),
                                        ('arts','Arts')])
    student_id = fields.One2many('school.management.student', 'class_teacher', string='students')