from odoo import fields, models, api
from datetime import date, datetime, timedelta
from odoo.tools import html2plaintext

class ROP(models.Model):
    """Class implements prescription orders"""
    _name = "rop.evaluation"
    _description = "rop evaluations"

    patient_id = fields.Many2one("res.partner", "Patient name")
    date = fields.Datetime("Date of Exam", default=fields.Datetime.now)
    gestation_age = fields.Integer(string="Birth gestation age in weeks", related='patient_id.gestation_age')
    birth_weight = fields.Integer(string="Birth Weight(Grams)", related='patient_id.birth_weight')
    chronological_age = fields.Float(string="Chronological age(Weeks)", related='patient_id.weeks')
    nicu = fields.Boolean("Currently a NICU patient")
    pma = fields.Float(string="PMA in weeks(chronological age + Gestation age)", compute="_compute_pma", store=True)
    most_recent_weight = fields.Integer("Most recent weight(Grams)")
    blood_transfusion = fields.Boolean("Had a blood transfusion?")
    cpap = fields.Boolean("Been on CPAP?")
    oxygen = fields.Boolean("Been on oxygen for more than one week?")
    infection = fields.Boolean("Been treated for an infection for more than 2 days?")
    right_zone = fields.Selection(selection=[
        ("None", "None"),('1', '1'), ('2', '2'), ('3', '3'), ('1 and 2', '1 and 2') , ('1 and 3', '1 and 3'), ('2 and 3', '2 and 3'), ('1, 2 and 3', '1, 2 and 3')
    ], string='Zone', help='Select Zone',default="None")
    right_stage = fields.Selection(selection=[
        ("Normal", "Normal"),('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
    ], string='Stage', help='Select Stage',default="Normal")
    right_pre_plus = fields.Boolean("Pre-plus")
    right_plus = fields.Boolean("Plus")
    right_arop = fields.Boolean("AROP")
    left_zone = fields.Selection(selection=[
        ("None", "None"),('1', '1'), ('2', '2'), ('3', '3'), ('1 and 2', '1 and 2') , ('1 and 3', '1 and 3'), ('2 and 3', '2 and 3'), ('1, 2 and 3', '1, 2 and 3')
    ], string='Zone', help='Select Zone' ,default="None")
    left_stage = fields.Selection(selection=[
        ("Normal", "Normal"),('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
    ], string='Stage', help='Select Stage' ,default="Normal")
    left_pre_plus = fields.Boolean("Pre-plus")
    left_plus = fields.Boolean("Plus")
    left_arop = fields.Boolean("AROP")
    Comments = fields.Html(string='Comments', help='Comments',
                        sanitize_style=True)
    attachment = fields.Many2many('ir.attachment', string='Attachments')
    photo_saved = fields.Boolean("Photo saved?")
    Plan = fields.Selection(selection=[
        ('no_review', 'No review'), ('need_review', 'Need Review'), ('need_treatment', 'Need Treatment'), ('received_treatment', 'Received Treatment')
    ], string='Plan', help='Select Plan')
    review_date = fields.Datetime("Review Date")
    rop_no = fields.Char(string='Evaluation#',
                              help='Sequence number of the rop patient', copy=False,
                              readonly=True, index=True,
                              default=lambda self: 'New')
    in_charge = fields.Many2one('res.users', string='In Charge', default=lambda self: self.env.user)

    def remove_offset(self):
        """Removes offset"""
        self.patient_id.tz_offset = "+000"

    def generate_report(self):
        # Add your report generation logic here
        # For example, query data and prepare report content
        self.remove_offset()
        report_data = {
            "model": "rop.evaluation",
            "form": self.read()[0],
        }

        """Sanitize comments"""
        comments = report_data["form"]["Comments"]
        if comments is not False:
            report_data["form"]["Comments"] = html2plaintext(comments)
        else:
             report_data["form"]["Comments"] = ""

        """Plan Changes"""
        plan = report_data["form"]["Plan"]
        if plan == "no_review":
            report_data["form"]["Plan"] = "No review"
        elif plan == "need_review":
            report_data["form"]["Plan"] = "Need review"
        elif plan == "need_treatment":
            report_data["form"]["Plan"] = "Need Treatment"
        elif plan == "received_treatment":
            report_data["form"]["Plan"] = "Received Treatment"
        
        
        report_data["form"]["date"] = report_data["form"]["date"] + timedelta(hours=3)
        if self.Plan == "need_review":
            report_data["form"]["review_date"] = report_data["form"]["review_date"] + timedelta(hours=3)
        print(self.in_charge.read())
        report_data["form"]["gender"] = self.patient_id.gender
        
        return self.env.ref('base_hospital_management.report_rop_action').report_action(self, data=report_data)

    @api.depends('gestation_age', 'chronological_age')
    def _compute_pma(self):
        """Compute postmenstrual age."""
        for rec in self:
            rec.pma = rec.gestation_age + rec.chronological_age
    
    @api.model
    def create(self, vals):
        """Includes sequence"""
        if vals.get('rop_no', 'New') == 'New':
            vals["rop_no"] = self.env["ir.sequence"].next_by_code("rop.sequence")
        return super(ROP, self).create(vals)


    
