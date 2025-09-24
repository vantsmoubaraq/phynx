from odoo import models, fields, api, _

class Register(models.Model):
    _name = 'register.start'
    _rec_name = "reason"

    client_name = fields.Many2one('phynx.career')
    person = fields.Many2one("res.partner")
    clock_time = fields.Datetime("Clock In Time", readonly=True,
        default=fields.Datetime.now,)
    reason = fields.Selection(
        [("Applicant", "Applicant"),
         ("New Client", "New Client"),
         ("Supplier", "Supplier"),
         ("Partner", "Partner"),
         ("Personal", "Personal")]
    )
    other_reasons = fields.Text("Description")
    reg_no = fields.Char(string='Register#',
                              help='Sequence number of the register', copy=False,
                              readonly=True, index=True,
                              default=lambda self: 'New')
    display_time = fields.Char(string="Time", compute='_compute_display_time', store=False)

    def _compute_display_time(self):
        for record in self:
            if record.clock_time:
                # Format the datetime to a string showing only the time (e.g., "15:55:00")
                record.display_time = fields.Datetime.to_string(record.clock_time)[11:16]
            else:
                record.display_time = False

    @api.model
    def create(self, vals):
        """Includes sequence"""
        if vals.get('reg_no', 'New') == 'New':
            vals["reg_no"] = self.env["ir.sequence"].next_by_code("register.sequence")
        return super(Register, self).create(vals)
    
    @api.onchange('reason')
    def _onchange_reason(self):
        if self.reason in ['Applicant', 'New Client']:
            # Clear the person field if the reason matches
            self.person = False
        elif self.reason in ['Supplier', 'Partner', 'Personal']:
            # Clear the client_name field for other reasons
            self.client_name = False

    def action_view_record(self):
        """
        Opens the form view of the client_name or person record based on the reason.
        """
        self.ensure_one()
        
        # Determine the model and record ID based on the reason
        if self.reason in ['Applicant', 'New Client'] and self.client_name:
            model_name = 'phynx.career'
            record_id = self.client_name.id
        elif self.reason in ['Supplier', 'Partner', 'Personal'] and self.person:
            model_name = 'res.partner'
            record_id = self.person.id
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': _('No Record'),
                'res_model': 'ir.ui.view',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'target': 'new',
            }

        return {
            'type': 'ir.actions.act_window',
            'name': _('View Record'),
            'res_model': model_name,
            'res_id': record_id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
        }
    
    