from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import *


class ResPartner(models.Model):
    _name = "phynx.career"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    
    message_follower_ids = fields.One2many(related='partner_id.message_follower_ids', readonly=False)
    message_ids = fields.One2many(related='partner_id.message_ids', readonly=False)
    activity_ids = fields.One2many(related='partner_id.activity_ids', readonly=False)
    attachment_ids = fields.Many2many(
    'ir.attachment',
    'phynx_career_ir_attachments_rel',  # custom relation table name
    'career_id',                       # current model's key
    'attachment_id',                   # target model's key
    string='Attachments',
    )
    partner_id = fields.Many2one('res.partner', string="Related Partner", required=True, ondelete='cascade')
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age in Years", compute='_compute_age', store=True)
   
    image_1920 = fields.Image(related='partner_id.image_1920', readonly=False)
    applications = fields.One2many('hr.applicant', 'application_id', string="Applications")

    @api.depends("dob")
    def _compute_age(self):
        today = datetime.today().date()
        for rec in self:
            if rec.dob:
                dob = fields.Date.from_string(rec.dob)
                age = relativedelta(today, dob).years
                rec.age = age
            else:
                rec.age = 0

    """@api.model
    def create(self, vals):
        #Create partner using the same name
        if vals.get('name'):
            partner = self.env["res.partner"].create(
                {'name': vals['name'],
                'email': vals.get('email'),
                'phone': vals.get('phone'),
                'image_1920': vals.get('image_128'),
                }
            )
            vals['partner_id'] = partner.id
        return super(ResPartner, self).create(vals)
    
    def write(self, vals):
        res = super().write(vals)
        
        for record in self:
            if record.partner_id:
                partner_updates = {}

                if 'name' in vals:
                    partner_updates['name'] = vals['name']
                if 'email' in vals:
                    partner_updates['email'] = vals['email']
                if 'phone' in vals:
                    partner_updates['phone'] = vals['phone']
                if 'image_128' in vals:
                    partner_updates['image_1920'] = vals['image_128']

                if partner_updates:
                    record.partner_id.write(partner_updates)

        return res"""


    def action_view_applications(self):
        """Returns client applications"""
        self.ensure_one()
        return {
        'name': 'Client Applications',
        'type': 'ir.actions.act_window',
        'res_model': 'hr.applicant',
        'view_mode': 'tree,form',
        'domain': [('partner_id', '=', self.id)],
        'context': {
            'create': True,
            'default_partner_id': self.id,
            'default_partner_name': self.name,
            'default_name': f"Application - {self.name or ''}",
            'default_email_from': self.email,
            'default_email_cc': self.email,
            'default_partner_phone': self.phone,
            'default_image_1920': self.image_1920,
            'default_application_id': self.application_id,     
        },
        }

    def action_view_invoices(self):
        self.ensure_one()

        # Get the action definition from the original account module
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")

        # Use the partner_id field from delegated inheritance
        partner = self.partner_id
        all_child_partners = partner.with_context(active_test=False).search([('id', 'child_of', partner.id)])

        # Adjust domain to show only invoices related to this partner (and children, if any)
        action['domain'] = [
            ('move_type', 'in', ('out_invoice', 'out_refund')),
            ('partner_id', 'in', all_child_partners.ids),
        ]

        # Set context for invoice creation (optional but useful)
        action['context'] = {
            'default_partner_id': partner.id,
            'default_move_type': 'out_invoice',
            'move_type': 'out_invoice',
            'journal_type': 'sale',
            'search_default_unpaid': 1,
        }

        return action
    

    def schedule_meeting(self):
        self.ensure_one()
        
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")
        
        if self.partner_id:
            action['context'] = {
                # Set the default attendee for a NEW meeting
                'default_partner_ids': [(6, 0, [self.partner_id.id])],
                # Pre-filter the calendar view by this partner
                'search_default_partner_ids': self.partner_id.id,
            }
            # Set a domain to display only meetings with this specific partner
            action['domain'] = [('partner_ids', 'in', [self.partner_id.id])]
        else:
            # If no partner is available, show all meetings
            action['context'] = {}
            action['domain'] = []
        
        return action
