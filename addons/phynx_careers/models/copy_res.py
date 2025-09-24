from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import *


class ResPartner(models.Model):
    _name = "phynx.career"
    _inherit = 'res.partner' 
    _description = "inherits from res.partner to extend functionality for phynx careers"
    
    name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner', string="Related Partner")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age in Years", compute='_compute_age', store=True)
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    image_128 = fields.Image("Image", max_width=128, max_height=128)

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

    @api.model
    def create(self, vals):
        """Create partner using the same name"""
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

        return res


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
            'default_partner_phone': self.phone,     
        },
        }

    def action_view_invoices(self):
        """Show all invoices associated with applicant"""
        self.ensure_one()
        return {
            'name': 'client_invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id), ('move_type', '=', 'out_invoice')],
            'context': {
                'create': True,
                'default_partner_id': self.id,
            }
        }