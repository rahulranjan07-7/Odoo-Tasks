from odoo import fields, models, api

class Session(models.Model):
    _inherit = "pos.session"

    loc_selection = fields.Many2many(
        'pos.location', related='config_id.loc_selection', string='Loc Session')

    @api.model
    def _pos_ui_models_to_load(self):
        models_to_load = super()._pos_ui_models_to_load()
        models_to_load.append('pos.location')
        return models_to_load

    def _loader_params_pos_location(self):
        return {
            'search_params': {
                'fields': [
                    'location'
                ],
            }
        }

    def _get_pos_ui_pos_location(self, params):
        result = list(self.env['pos.location'].search_read(
            **params['search_params']))
        return result