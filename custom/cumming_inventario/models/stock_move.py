# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, OrderedSet

import logging
_logger = logging.getLogger(__name__)
class StockMoveCummingInventario(models.Model):
	_inherit = 'stock.move'


	def product_price_update_before_done(self, forced_qty=None):
		_logger.info("ACTUALIZAR COSTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
		tmpl_dict = defaultdict(lambda: 0.0)
		# adapt standard price on incomming moves if the product cost_method is 'average'
		std_price_update = {}
		for move in self.filtered(lambda move: move._is_in() and move.with_company(move.company_id).product_id.cost_method == 'average'):
			product_tot_qty_available = move.product_id.sudo().with_company(move.company_id).quantity_svl + tmpl_dict[move.product_id.id]
			rounding = move.product_id.uom_id.rounding

			valued_move_lines = move._get_in_move_lines()
			qty_done = 0
			for valued_move_line in valued_move_lines:
				qty_done += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)

			qty = forced_qty or qty_done
			if float_is_zero(product_tot_qty_available, precision_rounding=rounding):
				new_std_price = move._get_price_unit()
			elif float_is_zero(product_tot_qty_available + move.product_qty, precision_rounding=rounding) or \
					float_is_zero(product_tot_qty_available + qty, precision_rounding=rounding):
				new_std_price = move._get_price_unit()
			else:
				# Get the standard price
				amount_unit = std_price_update.get((move.company_id.id, move.product_id.id)) or move.product_id.with_company(move.company_id).standard_price
				new_std_price = ((amount_unit * product_tot_qty_available) + (move._get_price_unit() * qty)) / (product_tot_qty_available + qty)

			tmpl_dict[move.product_id.id] += qty_done
			# Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
			move.product_id.with_company(move.company_id.id).with_context(disable_auto_svl=True).sudo().write({'standard_price': new_std_price})

			#asignar costo fob en product template
			move.product_id.product_tmpl_id.with_company(move.company_id.id).sudo().write({'fob_cost':new_std_price})

			_logger.info("product_price_update_before_done %s",move.product_id.product_tmpl_id)
			std_price_update[move.company_id.id, move.product_id.id] = new_std_price

		# adapt standard price on incomming moves if the product cost_method is 'fifo'
		for move in self.filtered(lambda move:
								  move.with_company(move.company_id).product_id.cost_method == 'fifo'
								  and float_is_zero(move.product_id.sudo().quantity_svl, precision_rounding=move.product_id.uom_id.rounding)):
			move.product_id.with_company(move.company_id.id).sudo().write({'standard_price': move._get_price_unit()})
			#asignar costo fob en product template
			move.product_id.product_tmpl_id.with_company(move.company_id.id).sudo().write({'fob_cost': move._get_price_unit()})
			
			_logger.info("product_price_update_before_done %s",move.product_id)