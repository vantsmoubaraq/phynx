from odoo import models, api, fields
import re
from bs4 import BeautifulSoup
import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = "crm.lead"

    email =fields.Char("Email")
    

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        custom_values = dict(custom_values or {})

        # Get body (HTML or plain text)
        body = msg_dict.get('body', '')
        # Convert HTML to plain text if needed
        body_text = BeautifulSoup(body, "html.parser").get_text("\n")
        print(f"body text is {body_text}")
        print(f"type of body is {type(body)} and type of body text is {type(body_text)}")

        _logger.info("====== RAW MESSAGE RECEIVED ======")
        for key, value in msg_dict.items():
            _logger.info("%s => %s", key, value)
        _logger.info("==================================")

        # Extract fields using regex
        def extract(field_names):
            if isinstance(field_names, str):
                field_names = [field_names]
            for field in field_names:
                pattern = rf'^{field}:\s*(.+)$'
                match = re.search(pattern, body_text, re.MULTILINE)
                if match:
                    return match.group(1).strip()
            return False

        name = extract("Name")
        email = extract("Email")
        phone = extract(["Phone Number", "Phone"])
        message = extract("Message")

        if name:
            custom_values['contact_name'] = name
            custom_values['name'] = name

        if email:
            custom_values['email'] = email
        if phone:
            custom_values['phone'] = phone
        if message:
            custom_values['description'] = message
        
        custom_values['partner_id'] = False

        return super().message_new(msg_dict, custom_values)
    
    """def create_client(self):
        create a new phynx object from current crm lead fields
        self.env["phynx.career"].create(
            {
                "name": self.contact_name,
                "email": self.email,
            }
        )"""
    
    def action_create_client(self):
        """Open phynx.career form with defaults from the lead"""
        self.ensure_one()
        return {
            'name': 'Create Client',
            'type': 'ir.actions.act_window',
            'res_model': 'phynx.career',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_name': self.contact_name or None,
                'default_email': self.email or None,
                'default_phone': self.phone or None,
            },
        }

