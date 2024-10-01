from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char('Tag', required=True)

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]
    