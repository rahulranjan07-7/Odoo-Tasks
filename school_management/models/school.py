from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date


class SchoolManagement(models.Model):
    _name = 'school.management.student'
    _description = 'Student'
    _inherit = ['school.payments', 'mail.thread']
    _rec_name = 'enrollment_number'


    student_name = fields.Many2one('school.management.student', string = 'Student Name')

    name = fields.Char(string='Name', required=True)

    standard_division = fields.Char(string='Standard & Division')

    active = fields.Boolean('Active', default=True)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self:self.env.company)

    currency_id = fields.Many2one('res.currency', related = 'company_id.currency_id')
    
    roll_number = fields.Char(string='Roll Number')

    active = fields.Boolean(default=True)

    image = fields.Binary(string='Student Image')

    fee_status = fields.Selection([
        ('paid', 'Paid'), 
        ('half paid', 'Half Paid'), 
        ('pending', 'Pending')
    ], string='Fee Status')

    gender = fields.Selection([
        ('male', 'Male'), 
        ('female', 'Female'), 
        ('others', 'Others')
        ], string = 'Gender:')

    enrollment_number = fields.One2many('school.management.library')

    enrollment_number = fields.Char(string='Enrollment Number', compute='_compute_enrollment_number', store=True)

    street = fields.Char(string='Street')

    city = fields.Char(string='City')

    zip_code = fields.Char(string='ZIP Code')

    is_good = fields.Boolean(string='Is Good Student?:')

    country_id = fields.Many2one('res.country', default=lambda self: self.env.ref('base.in'), 
                                 string='Country', readonly= True)
    
    state_id = fields.Many2one('res.country.state', 
                               domain="[('country_id', '=', country_id)]")
    
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

    hobbies_ids = fields.One2many('school.management.hobbies', 'enrollment_number', 
                                  string = ' hobbies ')
    
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

    teacher_details = fields.Many2many('school.management.teacher', string='Teacher Details')

    email_address = fields.Char(string = 'Email Address')

    previous_roll_number = fields.Char(string='Old Roll Number')

    admission_date = fields.Date(string='Admission Date')

    leaving_date = fields.Date(string='Leaving Date')

    status=fields.Selection([
        ('applied',"Applied"),
        ('selected',"Selected"),
        ('rejected',"Rejected"),
    ],string="Status")

    school_name = fields.Char(string= 'School Name',)

    class_teacher = fields.Many2one('school.management.teacher', 
                                    string= 'Class Teacher', compute='_onchange_stream', store=True)

    @api.constrains('phone_number')
    def _check_phone_number(self):
        for record in self:
            if record.phone_number and (not record.phone_number.isdigit() or len(record.phone_number) < 10):
                raise ValidationError("Phone number should contain only numeric values and have a maximum length of 10 digits!")
            
            duplicate_records = self.search([('phone_number', '=', record.phone_number), ('id', '!=', record.id)]) 
            if duplicate_records: 
                raise ValidationError("Phone number is already assigned to another student")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     print(vals_list)
    #     for vals in vals_list:
    #       if 'roll_number' not in vals:
    #         vals['roll_number'] = self.env['ir.sequence'].next_by_code('school.management.student') or '/'
    #     return super(SchoolManagement, self).create(vals)

    def unlink(self):
        if self.status == 'selected':
            raise ValidationError("You cannot delete a student record with 'Selected' status")
        return super(SchoolManagement, self).unlink()

    def action_url(self):
        return{
            'type':'ir.actions.act_url',
            'target':'self',
            'url':'https://www.iima.ac.in/'
        }


    def change_status(self):
        for rec in self:
            rec.fee_status == 'pending' or 'half paid'
            rec.fee_status = 'paid'


    def change_status_to_half_paid(self):
        for rec in self:
            rec.fee_status == 'paid' or 'pending'
            rec.fee_status = 'half paid'


    def change_status_to_pending(self):
        for rec in self:
            rec.fee_status == 'paid' or 'half paid'
            rec.fee_status = 'pending'


    def change_status_to_selected(self):
        for rec in self:
            rec.status == 'applied' or 'rejected'
            rec.status = 'selected'




    def change_status_to_rejected(self):
        for rec in self:
            rec.status == 'applied' or 'selected'
            rec.status = 'rejected'


    def change_status_to_applied(self):
        for rec in self:
            rec.status == 'selected' or 'rejected'
            rec.status = 'applied'

    @api.onchange('roll_number')
    def _onchange_roll_number(self):
        if int(self.roll_number) <= 10:
            self.is_good = True
        else:
            self.is_good = False

    _sql_constraints = [
        ('unique_roll_number', 'unique (roll_number)',
         'Roll Number must be a unique.')
    ]

    @api.model
    def search(self, args, offset = 0, limit = None, order = None, count = False):
        args += ['|', ('payment_status', '=', 'paid'), ('status', '=', 'selected')]
        # offset, limit, order = 3,5, 'name ASC'
        return super(SchoolManagement, self).search(args, offset, limit, order, count)
    
    @api.returns('self', lambda value: value.id) 
    def copy(self, default=None): 
        default = dict({}) 
        default['name'] = self.name + ' (Copy)'
        return super(SchoolManagement, self).copy(default)

    @api.constrains('parent_phone_number')
    def _check_parent_phone_number(self):
        for record in self:
            if record.parent_phone_number and (not record.parent_phone_number.isdigit() or len(record.parent_phone_number) < 10):
                raise ValidationError("Phone number should contain only numeric values and have a maximum length of 10 digits!")

    def name_get(self):
        students_list = []
        for record in self:
            name = record.name + ' ' + record.enrollment_number
            students_list.append((record.id, name ))
        return students_list
        
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = args + ['|', '|', ('phone_number', operator, name), ('name', operator, name), ('enrollment_number', operator, name)]
        return super(SchoolManagement, self).search(domain, limit=limit).name_get()


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

    @api.constrains('name')
    def check_name(self): 
        for rec in self:    
            if not 5 <= len(rec.name) <= 15 or not re.match(r"^[a-zA-Z][ a-zA-Z]*", rec.name):
                raise ValidationError(('Name field only contain 10-15 alphabets and spaces')) 

    @api.depends('name')
    def _compute_enrollment_number(self):
        
        for record in self:
            if record.name:
                record.enrollment_number = 'ENR-' + str(record.id).zfill(6)
                
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


class Partner (models.Model):
    _inherit = "res.partner"

    @api.model
    def craeate(self, vals):
        print("User Env.", self.env.context)

        return super(Partner, self).create(vals)
    

class LibraryManagement(models.Model):
    _name = 'school.management.library'
    _description = 'Library Management'

    name_enrol = fields.Many2one('school.management.student', string='Name and Enroll')
    book_name = fields.Char(string='Book Name')
    book_id = fields.Char(string='Book ID')
    issue_date = fields.Date()
    return_date = fields.Date()


class HobbiesDetails(models.Model):
    _name = 'school.management.hobbies'
    _description = 'Hobbies Details'

    fav_sports = fields.Char(string='Fav Sports')
    no_of_sports = fields.Integer(string='No. of Sports')
    enrollment_number = fields.Many2one('school.management.student', string='Enrollment ')
    currency_id = fields.Many2one('res.currency', related='enrollment_number.currency_id')
    sports_fee = fields.Integer(string='Sports Fee')
    fee_sub_total = fields.Monetary(string='Subtotal', compute= '_compute_fee_sub_total')


    @api.depends('no_of_sports', 'sports_fee')
    def _compute_fee_sub_total(self):
        for rec in self:
            rec.fee_sub_total = rec.no_of_sports * rec.sports_fee