from odoo import fields, models, api


class PosOrderLocation(models.Model):
    _inherit = "pos.order"

    location = fields.Many2one('pos.location')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrderLocation, self)._order_fields(ui_order)
        loc_id = ui_order.get('loc_selection')
        if loc_id:
            res['location'] = loc_id.get('id')
        return res

class Location(models.Model):
    _name = 'pos.location'
    _description = 'set location'
    _rec_name = 'location'

    location = fields.Char()

class LocationPos(models.Model):
    _inherit = 'pos.config'

    loc_selection = fields.Many2many('pos.location')


class LocationPOS(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_loc_sel = fields.Many2many(
        related='pos_config_id.loc_selection', readonly=False)