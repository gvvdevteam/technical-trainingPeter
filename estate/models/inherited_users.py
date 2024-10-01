from odoo import fields, models

class inherited_users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", string="Properties", domain=[("state", "in", ['offerreceived','offeraccepted','new'])])