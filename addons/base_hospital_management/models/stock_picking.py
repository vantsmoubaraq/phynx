from odoo import models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_picking_tree_ready(self):
        action = self.env.ref('stock.action_picking_tree_ready').read()[0]
        action['context'] = {'create': False}  # Disable creation of new records
        return action