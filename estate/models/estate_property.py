from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property application tutorial"

    name = fields.Char('Estate property', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('selling_price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garages = fields.Boolean('Has garage')
    garden = fields.Boolean('Has garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(string='Type', selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])