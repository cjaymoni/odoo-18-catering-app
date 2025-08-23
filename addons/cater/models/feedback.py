from odoo import models, fields, api, _


class CateringFeedback(models.Model):
    _name = 'cater.feedback'
    _description = 'Customer Feedback'
    _inherit = ['mail.thread']
    _order = 'create_date desc'

    booking_id = fields.Many2one('cater.event.booking', 'Booking', required=True)
    partner_id = fields.Many2one('res.partner', related='booking_id.partner_id', store=True)
    rating = fields.Selection([
        ('1', '1 Star - Poor'),
        ('2', '2 Stars - Fair'),
        ('3', '3 Stars - Good'),
        ('4', '4 Stars - Very Good'),
        ('5', '5 Stars - Excellent')
    ], 'Rating', required=True, tracking=True)
    
    # Detailed ratings
    food_quality = fields.Integer('Food Quality (1-5)', default=5)
    service_quality = fields.Integer('Service Quality (1-5)', default=5)
    presentation = fields.Integer('Presentation (1-5)', default=5)
    timeliness = fields.Integer('Timeliness (1-5)', default=5)
    
    comments = fields.Text('Comments')
    would_recommend = fields.Boolean('Would Recommend', default=True)
    feedback_date = fields.Datetime('Feedback Date', default=fields.Datetime.now)
    source = fields.Selection([
        ('whatsapp', 'WhatsApp'),
        ('phone', 'Phone Call'),
        ('email', 'Email'),
        ('in_person', 'In Person')
    ], 'Feedback Source', default='whatsapp')
    
    @api.model
    def create_from_whatsapp(self, booking_id, rating, comments):
        """Create feedback from WhatsApp response"""
        return self.create({
            'booking_id': booking_id,
            'rating': str(rating),
            'comments': comments,
            'source': 'whatsapp'
        })
