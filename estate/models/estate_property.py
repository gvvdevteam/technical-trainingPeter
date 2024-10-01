from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property application tutorial"

    name = fields.Char('Estate property', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('selling_price', readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garages = fields.Boolean('Has garage')
    garden = fields.Boolean('Has garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(string='Garden orientation', selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='State', selection=[('new', 'New'), ('offerreceived', 'Offer received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, default='new')
    type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", string="Total area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best offered price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_estate_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                error_msg = "It's not allowed to sell a cancelled property"
                raise UserError(error_msg)                   
            else:
                record.state = 'sold'

    def action_estate_property_cancelled(self):
        for record in self:
            if record.state == 'sold':
                error_msg = "It's not allowed to cancel a sold property"
                raise UserError(error_msg)    
            else:
                record.state = 'cancelled'

    @api.ondelete(at_uninstall=False)
    def _unlink_if_offer_not_new_or_cancelled(self):
        if self.state not in ('new', 'cancelled'):
            raise UserError("Cannot remove this offer, only new and cancelled can be removed")

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price can only be positive.')]

    _sql_constraints = [('check_selling_price', 'CHECK(selling_price >= 0)','The selling price can only be positive.')]
            