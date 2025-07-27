import requests
import json
from odoo import models, fields, api, _


class WhatsAppService(models.Model):
    _name = 'cater.whatsapp.service'
    _description = 'WhatsApp Integration Service'

    name = fields.Char('Service Name', default='WhatsApp Service')
    api_url = fields.Char('API URL', default='https://api.twilio.com/2010-04-01/Accounts/')
    account_sid = fields.Char('Account SID', required=True)
    auth_token = fields.Char('Auth Token', required=True)
    from_number = fields.Char('From Number', required=True, help='Your WhatsApp Business number')
    active = fields.Boolean('Active', default=True)
    
    def send_message(self, to_number, message):
        """Send WhatsApp message via Twilio API"""
        if not self.active:
            return False
            
        try:
            url = f"{self.api_url}{self.account_sid}/Messages.json"
            
            data = {
                'From': f'whatsapp:{self.from_number}',
                'To': f'whatsapp:{to_number}',
                'Body': message
            }
            
            response = requests.post(
                url,
                data=data,
                auth=(self.account_sid, self.auth_token)
            )
            
            if response.status_code == 201:
                # Log successful message
                self.env['cater.whatsapp.log'].create({
                    'to_number': to_number,
                    'message': message,
                    'status': 'sent',
                    'response_data': response.text
                })
                return True
            else:
                # Log failed message
                self.env['cater.whatsapp.log'].create({
                    'to_number': to_number,
                    'message': message,
                    'status': 'failed',
                    'error_message': response.text
                })
                return False
                
        except Exception as e:
            # Log error
            self.env['cater.whatsapp.log'].create({
                'to_number': to_number,
                'message': message,
                'status': 'error',
                'error_message': str(e)
            })
            return False

class WhatsAppLog(models.Model):
    _name = 'cater.whatsapp.log'
    _description = 'WhatsApp Message Log'
    _order = 'create_date desc'

    to_number = fields.Char('To Number', required=True)
    message = fields.Text('Message', required=True)
    status = fields.Selection([
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('error', 'Error')
    ], 'Status', required=True)
    response_data = fields.Text('Response Data')
    error_message = fields.Text('Error Message')
    send_date = fields.Datetime('Send Date', default=fields.Datetime.now)
