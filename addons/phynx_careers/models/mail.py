import requests
from odoo import models, fields, api

class ZohoToOdooCRM(models.Model):
    _name = "zoho.crm.sync"

    @api.model
    def fetch_zoho_emails(self):
        access_token = self._get_access_token()
        headers = {"Authorization": f"Zoho-oauthtoken 84dee7af89c4f6c1dd835336672f73281ee1438b23"}
        url = "https://mail.zoho.com/api/accounts/1000.G1K98NID1H5Q9U6VI2INNJ3M0RQG2L/messages/view"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for msg in response.json().get("data", []):
                subject = msg.get("subject")
                from_email = msg.get("from").get("address")
                
                # create lead in Odoo CRM
                self.env["crm.lead"].create({
                    "name": subject,
                    "email_from": from_email,
                    "type": "opportunity",
                })
