# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class WhatsAppWebhookController(http.Controller):
    @http.route('/whatsapp/webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def whatsapp_webhook(self, **kwargs):
        """Endpoint for Twilio to POST incoming WhatsApp messages.

        If the 'twilio' library is available, validates the X-Twilio-Signature
        header against the active service's Auth Token.
        """
        try:
            frm = request.httprequest.form
            # If this is a StatusCallback, update the log by MessageSid and return.
            message_sid = frm.get('MessageSid') or frm.get('SmsSid')
            if message_sid:
                message_status = (frm.get('MessageStatus') or '').lower()
                error_code = frm.get('ErrorCode')
                error_message = frm.get('ErrorMessage')
                Log = request.env['cater.whatsapp.log'].sudo()
                log = Log.search([('message_sid', '=', message_sid)], limit=1)
                if log:
                    vals = {}
                    allowed = {'queued', 'sending', 'sent', 'delivered', 'read', 'failed'}
                    if message_status in allowed:
                        vals['status'] = message_status
                    details = {k: frm.get(k) for k in frm.keys()}
                    vals['response_data'] = (log.response_data or '') + '\n' + str(details)
                    if message_status == 'failed' and (error_code or error_message):
                        vals['error_message'] = f"{error_code or ''} {error_message or ''}".strip()
                    log.write(vals)
                else:
                    request.env['cater.whatsapp.log'].sudo().create({
                        'to_number': 'unknown',
                        'message': '',
                        'status': message_status or 'sent',
                        'message_sid': message_sid,
                        'response_data': str({k: frm.get(k) for k in frm.keys()})
                    })
                return ''
            # Optional: Twilio signature validation
            try:
                from twilio.request_validator import RequestValidator  # type: ignore
                svc = request.env['cater.whatsapp.service'].sudo().search([('active', '=', True)], limit=1)
                signature = request.httprequest.headers.get('X-Twilio-Signature')
                if svc and signature:
                    validator = RequestValidator(svc.auth_token)
                    url = request.httprequest.url
                    params = {k: frm.get(k) for k in frm.keys()}
                    if not validator.validate(url, params, signature):
                        _logger.warning('Twilio signature validation failed for incoming webhook.')
                        return http.Response(status=403)
            except ImportError:
                _logger.info('twilio lib not installed; skipping signature validation.')
            from_number = frm.get('From')  # e.g., 'whatsapp:+233...'
            body = frm.get('Body')

            # Normalize 'From' to plain number if present
            if from_number and from_number.startswith('whatsapp:'):
                from_number = from_number.replace('whatsapp:', '')

            request.env['cater.whatsapp.log'].sudo().create({
                'to_number': from_number or 'unknown',
                'message': body or '',
                'status': 'received',
                'response_data': str({k: frm.get(k) for k in frm.keys()})
            })

            # Process feedback response if this is a feedback message
            if body and from_number:
                request.env['cater.event.booking'].sudo()._process_whatsapp_feedback_response(
                    from_number, body
                )

            # Minimal TwiML response (optional). Twilio accepts 200 with empty body.
            return ''
        except Exception as e:
            _logger.exception('Failed to process WhatsApp webhook: %s', e)
            return ''

    @http.route(['/whatsapp/status', '/whatsapp/status_callback'], type='http', auth='public', methods=['POST', 'GET'], csrf=False)
    def whatsapp_status(self, **kwargs):
        """Twilio StatusCallback webhook. Update message log status via MessageSid.

        Twilio posts fields like MessageSid and MessageStatus (queued, sending, sent, delivered, read, failed...).
        """
        try:
            frm = request.httprequest.form
            message_sid = frm.get('MessageSid') or frm.get('SmsSid')
            message_status = (frm.get('MessageStatus') or '').lower()
            error_code = frm.get('ErrorCode')
            error_message = frm.get('ErrorMessage')

            if not message_sid:
                _logger.warning('Status callback without MessageSid')
                return ''

            # Optional: validate signature like above (skip to keep it light)
            Log = request.env['cater.whatsapp.log'].sudo()
            log = Log.search([('message_sid', '=', message_sid)], limit=1)
            if log:
                vals = {}
                allowed = {'queued', 'sending', 'sent', 'delivered', 'read', 'failed'}
                if message_status in allowed:
                    vals['status'] = message_status
                # append/record details
                details = {k: frm.get(k) for k in frm.keys()}
                vals['response_data'] = (log.response_data or '') + '\n' + str(details)
                if message_status == 'failed' and (error_code or error_message):
                    vals['error_message'] = f"{error_code or ''} {error_message or ''}".strip()
                log.write(vals)
            else:
                # Create a minimal log if not found
                request.env['cater.whatsapp.log'].sudo().create({
                    'to_number': 'unknown',
                    'message': '',
                    'status': message_status or 'sent',
                    'message_sid': message_sid,
                    'response_data': str({k: frm.get(k) for k in frm.keys()})
                })
            return 'ok'
        except Exception as e:
            _logger.exception('Failed to process WhatsApp status callback: %s', e)
            return 'error'
