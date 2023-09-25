from odoo import models,api


class StudentXLSXReport(models.AbstractModel):
    _name = 'report.school_management.report_student_detail_xls'
    _description = 'Student XLSX Report'
    _inherit= 'report.report_xlsx.abstract'

    @api.model
    def _get_report_data(self):
        students = self.env['school.management.student'].search([]) 
        return students

    def generate_xlsx_report(self, workbook, data, objs):
        worksheet = workbook.add_worksheet('students')
        header_format = workbook.add_format({'bold': True, 'bg_color': 'yellow'})

        headers = ['Name', 'Enrollment Number', 'Phone number', 'Gender', 'Age', 'Roll number', 'Fee Status', 'Parent Name']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        for row, student in enumerate(objs, start=1):
            worksheet.write(row, 0, student.name)
            worksheet.write(row, 1, student.enrollment_number)
            worksheet.write(row, 2, student.phone_number)
            worksheet.write(row, 3, student.gender)
            worksheet.write(row, 4, student.age)
            worksheet.write(row, 5, student.roll_number)
            worksheet.write(row, 6, student.fee_status)
            worksheet.write(row, 7, student.parent_name)

