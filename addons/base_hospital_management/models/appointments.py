from odoo import models, fields, api
import requests
from datetime import datetime, timedelta, timezone
import pytz


class Appointments(models.TransientModel):
    """Class implements appointments"""
    _name = "appointments.list"

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    event_type = fields.Char(string="Event Type")
    location = fields.Char(string="Location")
    start_time = fields.Datetime(string="Start Time")
    status = fields.Char(string="Status")
    
    
    def events(self, response):
        """returns all events in last 7 days"""
        event_details = []

        for event in response["collection"]:
            uri = event["uri"]
            uri = uri.split("/")[4]
            location = event["location"].get("join_url", None)
            name = event["name"]
            start_time = event["start_time"]
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
            status = event["status"]
            event_details.append({"uri": uri, "location": location, "name": name, "start_time": start_time, "status": status})
        return(event_details)
    

    def invitees(self, all_events, headers):
        """Returns invitee details"""
        invitee_details = []

        for event in all_events:
            invitee_id = event.get("uri")
            if not invitee_id:
                continue

            invitee_url = f"https://api.calendly.com/scheduled_events/{invitee_id}/invitees"
            
            try:
                r = requests.get(invitee_url, headers=headers)
                r.raise_for_status()  # Raise an exception for HTTP errors
                invitee_data = r.json()
            except (requests.RequestException, ValueError) as e:
                print(f"Error fetching data for event {invitee_id}: {e}")
                continue  # Skip this event if there's an error
            
            if "collection" in invitee_data:
                collection = invitee_data.get("collection", [])
                if collection:
                    user_name = collection[0].get("name")
                    user_email = collection[0].get("email")
                    invitee_details.append({invitee_id: {"user_name": user_name, "user_email": user_email}})
                else:
                    print(f"No invitees found for event {invitee_id}")
            else:
                print(f"No collection found in the response for event {invitee_id}")
        
        print(invitee_details)
        return invitee_details
    

    def telemedicine(self):
        """Display appointments from calendly api"""
        access_token = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzEzMTg0Mzk2LCJqdGkiOiI0ZjI5ZDYyNi0xMWE0LTRmMmYtODg4OS0wMzgyMjgyYWJiMDQiLCJ1c2VyX3V1aWQiOiI1ZTBlMmQwYS04ZmVhLTRlZmEtOWExYi02NmZiMmU4N2RlZjAifQ.VyYXfg1k7HuLGdjgPEvHO-TAasyLWOFC1QEtUHl7-NabFxZrIMbTrda1cH1RlU8hcyejewXZUPIBWSz4EcgdSQ"
        endpoint = "https://api.calendly.com/scheduled_events"
            
        now = datetime.utcnow()
        min_start_time = now - timedelta(days=7)
        min_start_time_utc = min_start_time.replace(tzinfo=timezone.utc)
        min_start_time = min_start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        params = {"user": "https://api.calendly.com/users/5e0e2d0a-8fea-4efa-9a1b-66fb2e87def0"}

        response = requests.get(endpoint, headers=headers, params=params)
        response = response.json()
            
        all_events = self.events(response)
        all_invitees = self.invitees(all_events, headers)

        for event in all_events:
            for invitee in all_invitees:
                if event["uri"] in invitee:
                    event.update(invitee[event["uri"]])
                    
        
        self.create_appointments(all_events)
        print(all_events)
        return all_events

    def create_appointments(self, appointments_data):
        """Creates appointment records from events and stores them in the transient model"""
        self.env['appointments.list'].search([]).unlink()
        
        for appointment_data in appointments_data:
            self.env['appointments.list'].create({
                'event_type': appointment_data.get('name'),
                'name': appointment_data.get('user_name'),
                'location': appointment_data.get('location'),
                'start_time': appointment_data.get('start_time'),
                'status': appointment_data.get('status'),
                'email': appointment_data.get('user_email')

            })
    
    def execute_action(self):
        # Check if the 'telemedicine' flag is set in the context
        if self.env.context.get('telemedicine'):
            # Call the telemedicine method
            self.telemedicine()
        else:
            # Perform other actions based on the context
            pass  # You can replace 'pass' with your specific logic

    """def _compute_this_week_domain(self):
        one_week_ago =  fields.Datetime.now() - timedelta(days=7)
        for record in self:
            record.this_week_domain = one_week_ago
    
    this_week_domain = fields.Datetime(compute='_compute_this_week_domain', string="This Week's Domain")"""

    def see(self):
        for record in self:
            print(f"start time: {record.start_time}, domain: {record.this_week_domain}")
