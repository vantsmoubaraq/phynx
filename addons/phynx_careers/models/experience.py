from odoo import models, fields

class Experience(models.Model):
    _name = 'phynx.experience'
    _description = 'Work Experience'

    phynx_recruitment_id = fields.Many2one('hr.applicant', string="CV", ondelete='cascade')
    job_title = fields.Char(string="Job Title")
    company = fields.Char(string="Company")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    responsibilities = fields.Text(string="Responsibilities / Achievements")