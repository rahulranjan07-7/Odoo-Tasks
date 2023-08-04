from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date


class HobbiesDetails(models.Model):
    _name = 'school.management.hobbies'
    _description = 'Hobbies Details'

    fav_sports = fields.Char(string='Fav Sports')
    no_of_sports = fields.Integer(string='No. of Sports')
    enrollment_number = fields.Many2one(
        'school.management.student', string='Name and Enroll')
    currency_id = fields.Many2one(
        'res.currency', related='enrollment_number.currency_id')
    hobby_image = fields.Binary(string='Game Image')
    sports_fee = fields.Float(string='Sports Fee', digits='Product Price')
    fee_sub_total = fields.Monetary(
        string='Subtotal', compute='_compute_fee_sub_total', store=False)

    # @api.depends('no_of_sports', 'sports_fee')
    def _compute_fee_sub_total(self):
        for rec in self:
            rec.fee_sub_total = rec.no_of_sports * rec.sports_fee


class SchoolManagement(models.Model):
    _name = 'school.management.student'
    _description = 'Student'
    _inherit = ['school.payments']
    _rec_name = 'enrollment_number'


    @api.model
    def test_cron_job(self):
        print("abcd")


    student_name = fields.Many2one(
        'school.management.student', string='Student Name')
    name = fields.Char(string='Name', required=True)
    standard_division = fields.Char(string='Standard & Division')
    date_of_birth = fields.Date(string='Date of Birth')
    is_good = fields.Boolean(string='Is Good Student?:')

    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ], string='Gender:')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    phone_number = fields.Char(
        string='Phone Number', required=True, tracking=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id')
    handle = fields.Integer()
    roll_number = fields.Char(string='Roll Number')
    active = fields.Boolean(default=True)
    student_image = fields.Binary(string='Student Image')
    class_teacher_image = fields.Binary(string='Class Teacher Image')
    fee_status = fields.Selection(selection=[
        ('paid', 'Paid'),
        ('half paid', 'Half Paid'),
        ('pending', 'Pending')
    ], string='Fee Status')
    enrollment_number = fields.One2many('school.management.library')
    enrollment_number = fields.Char(
        string='Enrollment Number', compute='_compute_enrollment_number', store=True)
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    zip_code = fields.Char(string='ZIP Code')
    country_id = fields.Many2one('res.country', default=lambda self: self.env.ref('base.in'),
                                 string='Country', readonly=True)
    state_id = fields.Many2one('res.country.state',
                               domain="[('country_id', '=', country_id)]")
    address = fields.Text(
        string='Address', compute='_compute_address', store=True)
    parent_name = fields.Char(string='Parent Name')
    parent_phone_number = fields.Char(string='Parent Phone Number')
    relation_with_child = fields.Selection(selection=[
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Others', 'Others')
    ])
    status = fields.Selection(selection=[
        ('applied', "Applied"),
        ('selected', "Selected"),
        ('rejected', "Rejected"),
    ], string="Status")
    hobbies_ids = fields.One2many('school.management.hobbies', 'enrollment_number',
                                  string=' hobbies ')
    total_hobby_fee = fields.Monetary(
        string='Total Hobby Fee', digits='Product Price', compute='_compute_total_hobby_fee', store=True)

    @api.depends('hobbies_ids.fee_sub_total')
    def _compute_total_hobby_fee(self):
        sum = 0
        for student in self.hobbies_ids:
            sum += student.fee_sub_total

        for rec in self:
            rec.total_hobby_fee = sum

    birth_month = fields.Selection(selection=[
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

    stream = fields.Selection(selection=[
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('commerce', 'Commerce')
    ])

    teacher_details = fields.Many2many(
        'school.management.teacher', string='Teacher Details')

    email_address = fields.Char(string='Email Address')

    progress_bar = fields.Integer(
        compute='_compute_progress_bar', string='Progress')

    previous_roll_number = fields.Char(string='Old Roll Number')

    admission_date = fields.Date(string='Admission Date')

    leaving_date = fields.Date(string='Leaving Date')

    school_name = fields.Char(string='School Name',)

    class_teacher = fields.Many2one('school.management.teacher', compute='_onchange_standard_division',
                                    string='Class Teacher', store=True)

    @api.depends('name', 'standard_division', 'roll_number', 'enrollment_number', 'student_image',
                 'fee_status', 'gender', 'street', 'city', 'zip_code', 'is_good',
                 'country_id', 'state_id', 'phone_number', 'age', 'date_of_birth', 'parent_name', 'parent_phone_number',
                 'active', 'birth_month', 'standard_division', 'status', 'relation_with_child', 'hobbies_ids', 'teacher_details',
                 'email_address', 'previous_roll_number', 'admission_date', 'leaving_date', 'school_name')
    def _compute_progress_bar(self):

        fields_to_include = [
            'name', 'standard_division', 'roll_number', 'enrollment_number', 'student_image',
            'fee_status', 'gender', 'street', 'city', 'zip_code', 'is_good',
            'country_id', 'state_id', 'phone_number', 'age', 'date_of_birth', 'parent_name', 'parent_phone_number',
            'active', 'birth_month', 'standard_division', 'status', 'relation_with_child', 'hobbies_ids', 'teacher_details',
            'email_address', 'previous_roll_number', 'admission_date', 'leaving_date', 'school_name'
        ]
        total_fields = len(fields_to_include)
        filled_fields = 0

        for record in self:
            for field_name in fields_to_include:
                field_value = record[field_name]
                if field_value:
                    filled_fields += 1

            if total_fields > 0:
                progress_percentage = (filled_fields / total_fields) * 100
                record.progress_bar = min(int(progress_percentage), 100)
            else:
                record.progress_bar = 0

    @api.constrains('phone_number')
    def _check_phone_number(self):
        for record in self:
            if record.phone_number and (not record.phone_number.isdigit() or len(record.phone_number) < 10):
                raise ValidationError(
                    "Phone number should contain only numeric values and have a maximum length of 10 digits!")

            duplicate_records = self.search(
                [('phone_number', '=', record.phone_number), ('id', '!=', record.id)])
            if duplicate_records:
                raise ValidationError(
                    "Phone number is already assigned to another student")
            
    def action_send_card(self):
        template_id= self.env.ref('school_management.mail_template_student').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
    
    def action_send_card_cron(self):
        recs = self.env['school.management.student'].search([])
        print(recs, "htwfetdfywefyfwe")
        for rec in recs:
            template_id= rec.env.ref('school_management.mail_template_student').id
            rec.env['mail.template'].browse(template_id).send_mail(rec.id, force_send=True)

    def unlink(self):
        if self.status == 'selected':
            raise ValidationError(
                "You cannot delete a student record with 'Selected' status")
        return super(SchoolManagement, self).unlink()

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.iima.ac.in/'
        }

    def action_url_to(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': 'https://online.2iim.com/CAT-question-paper/'
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

    def write(self, vals):
        for rec in self:
            rr = rec.env['school.management.library'].browse([14])
            rr.book_name = 'diuhifhgdfhg'
        super(SchoolManagement, self).write(vals)

    _sql_constraints = [
        ('unique_roll_number', 'unique (roll_number)',
         'Roll Number must be a unique.')
    ]

    # @api.model
    # def search(self, args, offset = 0, limit = None, order = None, count = False):
    #     args += ['|', ('payment_status', '=', 'paid'), ('status', '=', 'selected')]
    #     # offset, limit, order = 3,5, 'name ASC'
    #     return super(SchoolManagement, self).search(args, offset, limit, order, count)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict({})
        default['name'] = self.name + ' (Copy)'
        return super(SchoolManagement, self).copy(default)

    @api.constrains('parent_phone_number')
    def _check_parent_phone_number(self):
        for record in self:
            if record.parent_phone_number and (not record.parent_phone_number.isdigit() or len(record.parent_phone_number) < 10):
                raise ValidationError(
                    "Phone number should contain only numeric values and have a maximum length of 10 digits!")

    def name_get(self):
        students_list = []
        for record in self:
            name = record.name + ' ' + record.enrollment_number
            students_list.append((record.id, name))
        return students_list

    @api.model
    def name_search(self, name='', args=None, operator='like', limit=100):
        if args is None:
            args = []
        operator = 'like'
        print(operator, 'opppp')
        domain = args + ['|', '|', ('name', operator, name), ('enrollment_number',
                                                              operator, name), ('phone_number', operator, name)]
        return super(SchoolManagement, self).search(domain, limit=limit).name_get()

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                date_of_birth = fields.Date.from_string(record.date_of_birth)
                record.age = today.year - date_of_birth.year - \
                    ((today.month, today.day) <
                     (date_of_birth.month, date_of_birth.day))
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
        for records in self:
            if records.zip_code and not records.zip_code.isdigit() or len(records.zip_code) != 6:
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
                record.enrollment_number = 'ENR-' + str(record.id).zfill(6)
            else:
                record.enrollment_number = ''

    @api.constrains('email_address')
    def check_email_address(self):
        for record in self:
            if record.email_address and '@' not in record.email_address:
                raise ValidationError("Invalid email address.")

    @api.depends('standard_division', 'stream')
    def _onchange_standard_division(self):
        for rec in self:
            if rec.standard_division:
                if int(rec.standard_division.split(" ")[0]) < 11:
                    teacher = self.env['school.management.teacher'].search([
                        ('standard_division', '=', self.standard_division)
                    ], limit=1)
                    if teacher:
                        rec.class_teacher = teacher.id
                else:
                    if self.stream:
                        print(self.stream, self.standard_division)
                        teacher = self.env['school.management.teacher'].search([
                            ('stream', '=', self.stream.lower()), ('standard_division', '=', str(
                                self.standard_division))
                        ])
                        print(teacher)
                        if teacher:
                            self.class_teacher = teacher.id
            else:
                self.class_teacher = False


class SchoolManagementTeacher(models.Model):
    _name = 'school.management.teacher'
    _description = 'Teacher'

    name = fields.Char(string='Name', required=True)
    standard_division = fields.Char(string='Standard & Division')
    stream = fields.Selection(selection=[('science', 'Science'),
                                         ('commerce', 'Commerce'),
                                         ('arts', 'Arts')])
    student_id = fields.One2many(
        'school.management.student', 'class_teacher', string='students')


# class Partner (models.Model):
#     _inherit = "res.partner"

#     @api.model
#     def create(self, vals):
#         print("User Env.", self.env.context)
#         return super(Partner, self).create(vals)


class LibraryManagement(models.Model):
    _name = 'school.management.library'
    _description = 'Library Management'
    _rec_name = 'book_name'

    name_enrol = fields.Many2one('school.management.student', string='Name and Enroll')
    book_name = fields.Char(string='Book Name')
    book_id = fields.Char(string='Book ID')
    issue_date = fields.Date()
    return_date = fields.Date()


class SchoolSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    director_name= fields.Char(string='Director Name')

    def default_get(self, fields):
        res = super(SchoolSettings, self).default_get(fields)
        default_values = self.get_default_director_name(fields)
        res.update(default_values)
        return res

    def set_values(self):
        super(SchoolSettings, self).set_values()
        config_param = self.env['ir.config_parameter'].sudo()
        config_param.set_param('school_management.director_name', self.director_name or '')

    @api.model
    def get_default_director_name(self, fields):
        return {
            'director_name': self.env['ir.config_parameter'].sudo().get_param('school_management.director_name', default=''),
        }