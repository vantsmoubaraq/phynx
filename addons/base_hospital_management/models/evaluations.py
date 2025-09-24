from odoo import models, fields, api


class Evaluation(models.Model):
    _name = "evaluation.clinicalnotes"
    _description = "implements clinical notes"

    patient_id = fields.Many2one("res.partner", "Patient name")
    clinical_notes = fields.Text("Clinical Notes")
    treatment_plan = fields.Text("Treatment Plan")
    bp = fields.Char("Blood Pressure")
    heart_rate = fields.Char("Heart rate")
    temperature = fields.Char("Temperature")
    respiration_rate = fields.Char("Respiration rate")
    diagnosis = fields.Char("Diagnosis")
    date = fields.Datetime("Evaluation Date", default=fields.Datetime.now)
    attachment = fields.Many2many('ir.attachment', string='Attachments')
    evaluation_no = fields.Char(string='Evaluation#',
                              help='Sequence number of the patient evaluations', copy=False,
                              readonly=True, index=True,
                              default=lambda self: 'New')
    #orthopedics
    spine_conditions = fields.Selection([
        ('Lumbar hypolordosis', 'Lumbar hypolordosis'),
        ('Lumbar spondylitis', 'Lumbar spondylitis'),
        ('Ankylosing spondylitis', 'Ankylosing spondylitis'),
        ('Lumbar spondylolisthesis', 'Lumber spondylolisthesis'),
    ], string="Spine Conditions")

    injury_type = fields.Selection([
        ('fracture', 'Fracture'),
        ('dislocation', 'Dislocation'),
        ('sprain', 'Sprain'),
        ('strain', 'Strain'),
        ('arthritis', 'Arthritis'),
        ('other', 'Other'),
    ], string="Injury Type")

    affected_limb = fields.Selection([
        ('left_arm', 'Left Arm'),
        ('right_arm', 'Right Arm'),
        ('left_leg', 'Left Leg'),
        ('right_leg', 'Right Leg'),
        ('spine', 'Spine'),
        ('pelvis', 'Pelvis'),
        ('other', 'Other'),
    ], string="Affected Limb")

    mechanism_of_injury = fields.Text("Mechanism of Injury")
    range_of_motion = fields.Text("Range of Motion (ROM)")
    neurovascular_status = fields.Text("Neurovascular Status")
    

    

    @api.model
    def create(self, vals):
        """Includes sequence"""
        if vals.get('evaluation_no', 'New') == 'New':
            vals["evaluation_no"] = self.env["ir.sequence"].next_by_code("evaluations.sequence")
        return super(Evaluation, self).create(vals)
    
