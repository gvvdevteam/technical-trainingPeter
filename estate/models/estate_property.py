from odoo import fields, models

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
    garden_orientation = fields.Selection(string='Type', selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Type', selection=[('new', 'New'), ('offerreceived', 'Offer received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, default='new')