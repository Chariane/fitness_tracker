# -*- coding= utf-8 -*-

import time
from openerp.osv import osv, orm
from openerp import models, api
from openerp.report import report_sxw

class rapport_invoice_e_mcf(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context=None):
		super(rapport_invoice_e_mcf, self).__init__(cr, uid, name, context=context)
		
		self.localcontext.update({
			'time': time,
			'get_data': self.get_data,
			'check_if_norm': self.check_if_norm,
		})
		self.context = context

	def check_if_norm(self):
		imprimer = self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).imprimer
		etat_norm = self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).etat_norm

		if not imprimer and not etat_norm:
			raise orm.except_orm(('Erreur'), ('Veuillez d\'abord normaliser la facture avant impression'))

			
		if imprimer:
			raise orm.except_orm(('Erreur'), ('Facture normalisee avec la machine. Veuillez imprimer selon les regles prevues a cet effet'))
	

	def get_data(self, form):
		res = {
			'uid_e_mcf' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).uid_e_mcf,
			'type_fact' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).type_fact,
			'ta' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).ta,
			'tb' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).tb,
			'tc_norm' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).tc_norm,
			'td' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).td,
			'taa' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).taa,
			'tab' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).tab,
			'tac' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).tac,
			'tad' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).tad,
			'tae' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).tae,
			'taf' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).taf,
			'hab' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).hab,
			'had' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).had,
			'vab' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).vab,
			'vad' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).vad,
			'aib_norm' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).aib_norm,
			'ts' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).ts,
			'total' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).total,
			'etat_norm' : self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).etat_norm,
			'datetime_norm': self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).datetime_norm,
			'qrcode_norm': self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).qrcode_norm,
			'qrcode_path_norm': self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).qrcode_path_norm,
			'code_mecef_dgi_norm': self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).code_mecef_dgi_norm,
			'counters_norm': self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).counters_norm,
			'nim_norm': self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).nim_norm,
			'norm_by': self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).norm_by,
		}
		return res


class rapport_invoice_e_mcf_parser(osv.AbstractModel):
	_name = 'report.manodoo_e_mcf.report_invoice_e_mcf_template'
	_inherit = 'report.abstract_report'
	_template = 'manodoo_e_mcf.report_invoice_e_mcf_template'
	_wrapped_report_class = rapport_invoice_e_mcf
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
