from odoo import models, fields


class Recruitment(models.Model):
    _inherit = "hr.applicant"

    experience_ids = fields.One2many('phynx.experience', 'cv_id', string="Work Experience")
    education_ids = fields.One2many('phynx.education', 'cv_id', string="Education")
    certification_ids = fields.One2many('phynx.certification', 'cv_id', string="Certifications")
    project_ids = fields.One2many('phynx.project', 'cv_id', string="Projects")
    referee_ids = fields.One2many('phynx.referee', 'cv_id', string="Referees")
    application_id = fields.Many2one('phynx.career', string="Applicant id")

    partner = fields.Many2one("res.partner", "Partner")


    def print_cv_report(self):
        return self.env.ref('phynx_careers.action_report_cv').report_action(self)
    
    def copy(self, default=None):
        default = dict(default or {})
        
        # Override the application_id in the new record, for example, to clear it.
        # This is optional and depends on your business logic.
        # default['application_id'] = False

        # Duplicate the main hr.applicant record. The standard copy handles the Many2one.
        new_applicant = super(Recruitment, self).copy(default)
        
        # Duplicate the one2many records and link them to the new applicant.
        for line in self.experience_ids:
            line.copy({'cv_id': new_applicant.id})

        for line in self.education_ids:
            line.copy({'cv_id': new_applicant.id})

        for line in self.certification_ids:
            line.copy({'cv_id': new_applicant.id})

        for line in self.project_ids:
            line.copy({'cv_id': new_applicant.id})

        for line in self.referee_ids:
            line.copy({'cv_id': new_applicant.id})
            
        return new_applicant


class Experience(models.Model):
    _name = 'phynx.experience'
    _description = 'Work Experience'

    cv_id = fields.Many2one('hr.applicant', string="CV")
    job_title = fields.Char(string="Job Title")
    company = fields.Char(string="Company")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    responsibilities = fields.Text(string="Responsibilities / Achievements")

class Education(models.Model):
    _name = 'phynx.education'
    _description = 'Education Record'

    cv_id = fields.Many2one('hr.applicant', string="CV")
    degree = fields.Char(string="Qualification")
    institution = fields.Char(string="Institution")
    start_year = fields.Char(string="Start Year")
    end_year = fields.Char(string="End Year")
    honors = fields.Char(string="Honors / Notes")

class Certification(models.Model):
    _name = 'phynx.certification'
    _description = 'CV Certification'

    cv_id = fields.Many2one('hr.applicant', string="CV")
    name = fields.Char(string="Certification Name", required=True)
    institution = fields.Char(string="Issuing Institution")
    date_received = fields.Date(string="Date Received")
    certificate_file = fields.Binary(string="Certificate File", attachment=True)
    certificate_filename = fields.Char(string="Filename")
    

class Project(models.Model):
    _name = 'phynx.project'
    _description = 'CV Project'

    cv_id = fields.Many2one('hr.applicant', string="CV")
    title = fields.Char(string="Project Title", required=True)
    description = fields.Text(string="Description")
    tools_used = fields.Char(string="Tools/Technologies Used")
    link = fields.Char(string="Project Link", help="e.g. GitHub, portfolio site")

class Referee(models.Model):
    _name = 'phynx.referee'
    _description = 'CV Referee'

    cv_id = fields.Many2one('hr.applicant', string="CV")
    name = fields.Char(string="Referee Name", required=True)
    position = fields.Char(string="Position / Relationship")
    company = fields.Char(string="Organization")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone Number")
