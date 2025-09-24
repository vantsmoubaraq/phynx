from odoo import fields, models, api
from datetime import date, datetime

class Prescription_Orders(models.Model):
    """Class implements prescription orders"""
    _name = "prescription.orders"
    _description = "prescription orders"
    _rec_name = "patient_id"

    patient_id = fields.Many2one("res.partner", "Patient name")
    date = fields.Datetime("Prescription date", default=fields.Datetime.now)
    Indication = fields.Char("Indication")
    sold = fields.Boolean(default=False)
    prescription_lines = fields.One2many("prescription.lines", 'prescription_id', string="prescription line")
    prescription_no = fields.Char(string='Pres No.',
                              help='Sequence number of the prescription order', copy=False,
                              readonly=True, index=True,
                              default=lambda self: 'New')
    sale_order_id = fields.Many2one('sale.order',
                                    string='Sale Order',
                                    help='Sale order for the prescription line')

    def action_create_so(self):
        """Method for creating the sale order for vaccines"""
        products = []
        for item in self.prescription_lines:
            obj_dict = {}
            obj_dict["product_id"] = item.medicine_id.id
            obj_dict["name"] = item.medicine_id.name
            obj_dict["price_unit"] = item.medicine_id.list_price
            obj_dict['product_uom_qty'] = item.quantity
            print(item.read())
            products.append(obj_dict)
        #print("product ids", products)

        sale = self.env['sale.order'].search([
            ('partner_id.id', '=', self.patient_id.id),
            ('state', '=', 'draft')], limit=1)
        
        for item in products:
            if sale:
                sale.sudo().write({
                    'order_line': [(
                        0, 0, item
                    )]
                })
            else:
                sale = self.env['sale.order'].sudo().create({
                    'partner_id': self.patient_id.id,
                    'date_order': fields.Date.today(),
                    'order_line': [(0, 0, item)]
                })
            self.sold = True
            self.sale_order_id = sale.id
        
    def get_sale_order(self):
        """Smart button action for viewing corresponding sale orders"""
        return {
            'name': 'Sale order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_id': self.sale_order_id.id
        }
    
    @api.model
    def create(self, vals):
        """Includes sequence"""
        if vals.get('prescription_no', 'New') == 'New':
            vals["prescription_no"] = self.env["ir.sequence"].next_by_code("prescription.sequence")
        return super(Prescription_Orders, self).create(vals)
