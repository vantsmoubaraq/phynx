from odoo import fields, api, models

class Register(models.Model):
    """class implements register"""
    _name = "register.start"
    _rec_name ="patient_id"
    
    patient_id = patient_id = fields.Many2one('res.partner', string="Patient",
                                 domain=[('patient_seq', 'not in',
                                          ['New', 'Employee', 'User'])],
                                 required=True, help='Choose the patient')
    patient_name_link = fields.Char(string="Patient File", compute='_compute_patient_name_link', readonly=True)
    reason = fields.Char(string="Reason for visit")
    type = fields.Selection([
        ('new', 'New Patient'),
        ('follow_up', 'Follow Up Visit'),
        ('old', 'Existing patient'),
    ], string='Patient Category')

    @api.depends('patient_id')
    def _compute_patient_name_link(self):
        for record in self:
            # Fetch the external ID of the action
            action_external_id = self.env.ref('base_hospital_management.res_partner_action').id
            # Construct the link with the external ID
            record.patient_name_link = "/web#id=%s&action=%s&model=res.partner&view_type=form" % (record.patient_id.id, action_external_id)

    def action_url(self):
        """Method redirects to patient record"""
        return {
            "type": "ir.actions.act_url",
            "url": self.patient_name_link,
            "target": "self",
        }