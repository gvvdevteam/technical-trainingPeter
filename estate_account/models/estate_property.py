from odoo import Command, fields, models
import openpyxl

class inherited_estate_property(models.Model):
    _inherit = "estate.property"

    def action_estate_property_sold(self):
        res = super().action_estate_property_sold()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        # Another way to get the journal:
        # journal = self.env["account.move"].with_context(default_move_type="out_invoice")._get_default_journal()
        for property in self:
            self.env["account.move"].create(
                {
                    "partner_id": property.buyer_id.id,
                    "move_type": "out_invoice", #https://github.com/odoo/odoo/blob/f1f48cdaab3dd7847e8546ad9887f24a9e2ed4c1/addons/account/models/account_move.py#L138-L147 possible values
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create({
                                "name": property.name + " 6% of the selling price",
                                "quantity": 1.0,
                                "price_unit": property.selling_price * 0.06,
                        }),
                        Command.create({
                                "name": "Administrative fee",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                        })
                    ]
                }
            )
        return res