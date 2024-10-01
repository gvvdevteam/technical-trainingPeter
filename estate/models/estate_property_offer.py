from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    property_id = fields.Many2one("estate.property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", required=True)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(compute="_computer_date_deadline", inverse="_inverse_date_deadline", string='Deadline')
    create_date = fields.Date(string='Creation date')

    @api.depends('create_date', 'validity')
    def _computer_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    def action_estate_property_offer_accept(self):
        self.status = 'accepted'            
        for offer in self:
            if offer.price < self.property_id.expected_price * 0.9:
                raise ValidationError("The offered price is too low considering the expected price!")
            else:
                self.property_id.selling_price = offer.price
                self.property_id.buyer_id = offer.partner_id
                self.property_id.state = 'offeraccepted'

    def action_estate_property_offer_refuse(self):
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if property.offer_ids:
                min_price = min(property.offer_ids.mapped("price"))
                if vals["price"] <= min_price:
                    raise UserError("We cannot accept an offer lower than existing one")
                property.state = 'offerreceived'
        return super().create(vals_list)

    _sql_constraints = [('check_price', 'CHECK(price >= 0)', 'The price on the offer can only be positive.')]        

            