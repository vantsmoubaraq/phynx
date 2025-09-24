from odoo import models, fields, api


class Pres_lines(models.Model):
    """Implements prescription lines"""
    _name = "prescription.lines"
    _description = "prescription line"

    prescription_id = fields.Many2one("prescription.orders", string="prescription", help="name of prescription",  invisible=True)
    medicine_id = fields.Many2one('product.template', domain=[
        '|', ('medicine_ok', '=', True), ('vaccine_ok', '=', True)],
                                  string='Medicine', required=True,
                                  help='Medicines or vaccines', create=False)
    quantity = fields.Integer(string='Quantity', required=True,
                              help="The number of medicines for the time "
                                   "period")
    no_intakes = fields.Float(string='Intakes', required=True,
                              help="How much medicine want to take")
    time = fields.Selection(
        [('once', 'Once in a day'), ('twice', 'Twice in a Day'),
         ('thrice', 'Thrice in a day'), ('morning', 'In Morning'),
         ('noon', 'In Noon'), ('evening', 'In Evening')], string='Time',
        required=True,
        help='The interval for medicine intake')
    note = fields.Selection(
        [('before', 'Before Food'), ('after', 'After Food')],
        string='Before/ After Food',
        help='Whether the medicine to be taken before or after food')
    duration = fields.Integer(string="Days")

