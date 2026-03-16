#!/usr/bin/env python
# -*- coding= utf-8 -*-
from openerp.osv import fields, orm
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
import time
import logging
import swagger_client
from swagger_client import ApiClient
from swagger_client.rest import ApiException
from swagger_client.models import *
_logger = logging.getLogger(__name__)

class res_company(models.Model):
	_inherit = "res.company"

	host = fields.Selection([('test', 'Test'),('prod', 'Production'),], 'Etat', default="test")
	jeton = fields.Text('Jeton')
	test_jeton = fields.Selection([('valid','Valide'),('error','Erreur'),], 'Statut du test')

	@api.multi
	def verifier(self):
		host = self.host
		jeton = self.jeton.rstrip("\n")
		
		configuration = swagger_client.Configuration()
		configuration.api_key['Authorization'] = jeton
		if host == 'prod':
			configuration.host = 'https://sygmef.impots.bj/emcf'
		
		api_info_instance = swagger_client.SfeInfoApi(ApiClient(configuration=configuration))
		try:
			
			info_response_dto = api_info_instance.api_info_status_get()
			# self.test_jeton = 'valid'
			dgi_ifu = info_response_dto.ifu
			odoo_ifu = self.ifu
			# if not odoo_ifu:
			if dgi_ifu != odoo_ifu:
				raise orm.except_orm(('Attention'),("Les numéros IFU du système et du jeton ne correspondent pas. \n"
													" Veuillez corriger SVP sur l'onglet 'Informations générales' dans le champ 'N° IFU' "))
			else:
				raise orm.except_orm(('Information'),("Le jeton est correct et correspond à l'IFU renseigné dans le système."))

		except ApiException as e:

			_logger.warning('Exception: %s', e)
			raise orm.except_orm(('Attention'),("Le jeton est incorrect.\n Contactez votre administrateur système pour la configuration. Merci!!!"))

		return True

	@api.multi
	def factures_attente(self):
		host = self.host
		jeton = self.jeton.rstrip("\n")
		
		configuration = swagger_client.Configuration()
		configuration.api_key['Authorization'] = jeton
		if host == 'prod':
			configuration.host = 'https://sygmef.impots.bj/emcf'
		
		api_invoice_instance = swagger_client.SfeInvoiceApi(ApiClient(configuration=configuration))
		try:
			
			status_response_dto = api_invoice_instance.api_invoice_get()
			raise orm.except_orm(('Attention'),(status_response_dto))

		
		except ApiException as e:

			_logger.warning('Exception: %s', e)

		return True



class groupe_taxation(models.Model):
	_name = "e.mcf.groupe.taxation"

	reference = fields.Char('Référence', required=True)
	name = fields.Char('Libellé', required=True)


class type_paiement(models.Model):
	_name = "e.mcf.type.paiement"

	type = fields.Char('Type', required=True)
	name = fields.Char('Libellé', required=True)



class account_tax(models.Model):
	_inherit = "account.tax"

	groupe_taxation_id = fields.Many2one('e.mcf.groupe.taxation', string="Groupe de taxation associé")

	@api.v7
	def compute_all(self, cr, uid, taxes, price_unit, quantity, product=None, partner=None, force_excluded=False, taxe_specifique=None):
		"""
		:param force_excluded: boolean used to say that we don't want to consider the value of field price_include of
			tax. It's used in encoding by line where you don't matter if you encoded a tax with that boolean to True or
			False
		RETURN: {
				'total': 0.0,                # Total without taxes
				'total_included: 0.0,        # Total with taxes
				'taxes': []                  # List of taxes, see compute for the format
			}
		"""

		# By default, for each tax, tax amount will first be computed
		# and rounded at the 'Account' decimal precision for each
		# PO/SO/invoice line and then these rounded amounts will be
		# summed, leading to the total amount for that tax. But, if the
		# company has tax_calculation_rounding_method = round_globally,
		# we still follow the same method, but we use a much larger
		# precision when we round the tax amount for each line (we use
		# the 'Account' decimal precision + 5), and that way it's like
		# rounding after the sum of the tax amounts of each line
		precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
		tax_compute_precision = precision
		if taxes and taxes[0].company_id.tax_calculation_rounding_method == 'round_globally':
			tax_compute_precision += 5
		if taxe_specifique is None:
			totalin = totalex = round(price_unit * quantity, precision)
		else:
			totalin = totalex = round(price_unit * quantity + taxe_specifique, precision)
		tin = []
		tex = []
		for tax in taxes:
			if not tax.price_include or force_excluded:
				tex.append(tax)
			else:
				tin.append(tax)
		tin = self.compute_inv(cr, uid, tin, price_unit, quantity, product=product, partner=partner, precision=tax_compute_precision)
		for r in tin:
			totalex -= r.get('amount', 0.0)
		totlex_qty = 0.0
		try:
			totlex_qty = totalex/quantity
		except:
			pass
		tex = self._compute(cr, uid, tex, totlex_qty, quantity, product=product, partner=partner, precision=tax_compute_precision)
		for r in tex:
			totalin += r.get('amount', 0.0)
		return {
			'total': totalex,
			'total_included': totalin,
			'taxes': tin + tex
		}

	@api.v8
	def compute_all(self, price_unit, quantity, product=None, partner=None, force_excluded=False, taxe_specifique=None):
		return account_tax.compute_all(
			self._model, self._cr, self._uid, self, price_unit, quantity,
			product=product, partner=partner, force_excluded=force_excluded, taxe_specifique=taxe_specifique)

class account_payment_method(models.Model):
	_inherit = "account.payment.method"

	type_paiement_id = fields.Many2one('e.mcf.type.paiement', string="Type de paiement associé")