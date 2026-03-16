#-*- coding: utf-8 -*-

import base64
from openerp import api, fields, models, _
from datetime import datetime
import calendar
import xlwt
from cStringIO import StringIO
from xlwt import easyxf
from openerp.exceptions import ValidationError

class situation_norm_wizard(models.TransientModel):
	_name = "situation_norm_wizard"
	# _inherit = "hr.livrepaye_new.wizard"
	_description = 'Situation Normalisation'
	
	@api.model
	def _current_date(self):
		date = datetime.now().today()
		return str(date)

	company_id = fields.Many2one("res.company", string="Société", default=lambda self: self.env.user.company_id, required="1")
	date_deb = fields.Date(string="Date de début", default=_current_date, required=True)
	date_fin = fields.Date(string="Date de fin", default=_current_date, required=True)
	date_impression = fields.Datetime(string="Date d'impression", default=_current_date, required=True)

	@api.multi
	def print_report(self):
		if self.date_fin < self.date_deb:
			raise except_orm(_('Attention !!!'), _(
				'La date de fin de période doit être postérieure à la date de début de période.'))
		if not self.check_invoices_open_at_this_range():
			raise ValidationError(_('Aucune facture à l\'état ouvert durant cette période !!!'))
		if not self.check_invoices_not_norm_at_this_range():
			raise ValidationError(_('Toutes les factures sont normalisées durant cette période !!!'))
		return self.env['report'].get_action(self, 'manodoo_e_mcf.situation_norm_template_id')
		

	@api.multi
	def check_invoices_not_norm_at_this_range(self):
		date_deb = self.date_deb
		date_fin = self.date_fin
		self.env.cr.execute("select id from account_invoice where date_invoice <= %s and date_invoice >= %s and state = 'open' and type in ('out_invoice','out_refund') and etat_norm = False", (date_fin, date_deb))
		results = self.env.cr.dictfetchall()
		invoices_ids = [invoice.get('id') for invoice in results]
		return invoices_ids


	@api.multi
	def check_invoices_open_at_this_range(self):
		date_deb = self.date_deb
		date_fin = self.date_fin
		self.env.cr.execute("select id from account_invoice where date_invoice <= %s and date_invoice >= %s and state = 'open' and type in ('out_invoice','out_refund')", (date_fin, date_deb))
		results = self.env.cr.dictfetchall()
		invoices_ids = [invoice.get('id') for invoice in results]
		return invoices_ids


	@api.multi
	def get_liste_invoices(self):
		date_deb = self.date_deb
		date_fin = self.date_fin
		# self.env['account_invoice'].search([''])
		self.env.cr.execute("	SELECT id \
							FROM account_invoice \
							WHERE date_invoice <= %s and date_invoice >= %s \
							AND type in ('out_invoice','out_refund') \
							AND state = 'open' \
							and etat_norm = False \
							ORDER BY date_invoice ASC", (date_fin, date_deb))
		results = self.env.cr.dictfetchall()
		invoice_lst = [invoice.get('id') for invoice in results]

		invoice_ids = self.env['account.invoice'].search([('id','in',invoice_lst)], order="date_invoice asc")
		
		return invoice_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
