#!/usr/bin/env python
# -*- coding= utf-8 -*-
from openerp.osv import fields, orm
from openerp import models, fields, api
import qrcode
import base64
import cStringIO
# import sys
import os
import logging
_logger = logging.getLogger(__name__)

try:
    
	import swagger_client
	from swagger_client import ApiClient
	from swagger_client.rest import ApiException
	from swagger_client.models import *
except ImportError:
    _logger.warning("Libraire Python 'swagger_client' non trouvé. ")


class account_invoice(models.Model):
	_inherit = "account.invoice"


	# @api.multi
	# def check_fields(self):

	# 	if 'facture_exportation' not in self.env['account.invoice']._fields:
	# facture_exportation = fields.Boolean("Facture d'exportation", help="Cocher s'il s'agit d'une facture d'exportation", )
	# 	# 	raise orm.except_orm(('Ici'), ('ok'))
		
	# 	# return True

	# @api.one
	# @api.depends('invoice_line.price_subtotal', 'tax_line.amount', 'amount_tax','invoice_line', 'invoice_line.invoice_line_tax_id')
	# def _compute_amount(self):
	# 	# for line in self.invoice_line:

	# 	amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
	# 	self.amount_untaxed = round(amount_untaxed)
				
	# 	self.amount_tax = sum(round(line.amount) for line in self.tax_line) 
	# 	tva_ts = 0
	# 	aib_sup = 0
	# 	aiba = aibb = i = 0
	# 	for line in self.invoice_line:
	# 		i += 1
	# 		# ts 
	# 		tva_ts += round(line.taxe_specifique*0.18)
	# 		# raise orm.except_orm(('Erreur'),("Merci"))
	# 		for tax in line.invoice_line_tax_id:
	# 			if tax.groupe_taxation_id.reference == "AIBA":
	# 				aiba += 1
	# 				aib_sup += round(line.taxe_specifique * 0.01)
	# 			elif tax.groupe_taxation_id.reference == "AIBB":
	# 				aibb += 1
	# 				aib_sup += round(line.taxe_specifique * 0.05)
	# 			elif tax.groupe_taxation_id.reference in ('A', 'C', 'E', 'F'):
	# 				tva_ts = 0
	# 			# raise orm.except_orm(('Erreur'),(tax.groupe_taxation_id.reference))

	# 	if (aiba != 0 and aibb != 0):
	# 		raise orm.except_orm(('Erreur'),("Vous ne pouvez pas appliquer deux types d'AIB sur une même facture. Merci!!!"))
	# 	else:
	# 		if (aiba != 0 and aiba != i) or (aibb != 0 and aibb != i):
	# 			raise orm.except_orm(('Erreur'),("Vous devez appliquer l'AIB sur toutes les lignes d'articles. Merci!!!"))
					
			
	# 	# raise orm.except_orm(('TS'), (aib_sup))
	# 	# for line in self.invoice_line:
	# 	self.amount_tax = round(self.amount_tax + tva_ts + aib_sup)
	# 	self.amount_total = round(self.amount_untaxed + self.amount_tax)

	# client = fields.Boolean('Client')
	etat_norm = fields.Boolean('Normalisée?', copy=False)
	norm_by = fields.Many2one('res.users', 'Normalisée par', readonly=True, copy=False)
	uid_e_mcf = fields.Char('Identifiant de la transaction', readonly=True, copy=False)
	type_fact = fields.Char('Type de facture', readonly=True, copy=False)
	ta = fields.Float('Valeur du groupe de taxation A (en %)', copy=False)
	tb = fields.Float('Valeur du groupe de taxation B (en %)', copy=False)
	tc_norm = fields.Float('Valeur du groupe de taxation C (en %)', copy=False)
	td = fields.Float('Valeur du groupe de taxation D (en %)', copy=False)
	taa = fields.Float('Montant total groupe A', copy=False)
	tab = fields.Float('Montant total groupe B', copy=False)
	tac = fields.Float('Montant total groupe C', copy=False)
	tad = fields.Float('Montant total groupe D', copy=False)
	tae = fields.Float('Montant total groupe E', copy=False)
	taf = fields.Float('Montant total groupe F', copy=False)
	hab = fields.Float('Montant HT groupe B', copy=False)
	had = fields.Float('Montant HT groupe D', copy=False)
	vab = fields.Float('Montant de TVA groupe B', copy=False)
	vad = fields.Float('Montant de TVA groupe D', copy=False)
	aib_norm = fields.Float('Montant de l\'AIB', copy=False)
	ts = fields.Float('Montant de l\'impôt spécifique', copy=False)
	total = fields.Float('Montant total', copy=False)
	ft = fields.Char('Type de facture', copy=False)
	# datetime_norm = fields.Datetime('Date et heure', readonly=True)
	datetime_norm = fields.Char('Date et heure', readonly=True, copy=False)
	nim_norm = fields.Char('NIM', readonly=True, copy=False)
	code_mecef_dgi_norm = fields.Char('Code MECeF DGI', readonly=True, copy=False)
	qrcode_norm = fields.Char('Code QR', readonly=True, copy=False)
	qrcode_path_norm = fields.Char(copy=False)
	# qrcode_chemin = fields.Char('qrcode_chemin', copy=False)
	counters_norm = fields.Char('Compteur', readonly=True, copy=False)
	rn_norm = fields.Char('Numéro facture initiale', copy=False)
	errorCode = fields.Char('Code de l\'erreur', copy=False)
	errorDesc = fields.Char('Description de l\'erreur', copy=False)
	

	def init_parameters(self):

		params = []
		host = self.company_id.host
		jeton = self.company_id.jeton

		if (not host or not jeton):
			raise orm.except_orm(('Erreur'),("Contactez votre administrateur système pour la configuration. Merci!!!"))
		
		return host, jeton

	def check_api_operationnel(self):

		params = self.init_parameters()
			
		configuration = swagger_client.Configuration()
		configuration.api_key['Authorization'] = params[1].rstrip("\n")
		if params[0] == 'prod':
			configuration.host = 'https://sygmef.impots.bj/emcf'

		api_invoice_instance = swagger_client.SfeInvoiceApi(ApiClient(configuration=configuration))

		try:
		
			status_response_dto = api_invoice_instance.api_invoice_get()
			ifu = status_response_dto.ifu
			odoo_ifu = self.company_id.ifu
			if ifu != odoo_ifu:
				raise orm.except_orm(('Attention'),("Les numéros IFU du système et du jeton ne correspondent pas. \n"
													" Veuillez corriger SVP en suivant ce lien: \n"
													" Configuration->Sociétés->Sociétés->Informations générales->N° IFU \n"
													"Merci!!! "  ))

			if status_response_dto:
				if not status_response_dto.status:
					raise orm.except_orm(('Connexion'),("Code: api_invoice_status \n"
														"La plateforme des impôts n'est pas opérationnelle. Contactez votre administrateur système"))

		except ApiException as e:

			_logger.info('Exception: %s', e)
			raise orm.except_orm(('Erreur'),("Code: check_api_operationnel \n"
											"Contactez votre administrateur système pour la configuration. Merci!!!"))
		
		return api_invoice_instance, ifu


	@api.one
	def normaliser(self):
		
		if not self.etat_norm:

			datas = self.check_api_operationnel()

			api_invoice_instance = datas[0]

			try:

				invoice_request_data_dto = self.prepare_invoice(datas[1])

				success = self.soumettre_invoice(api_invoice_instance, invoice_request_data_dto)

				if success:
					
					norm = self.confirmer_invoice(api_invoice_instance)

			except ApiException as e:

				_logger.info('Exception: %s\n', e)
				# print("Exception when calling PosInvoiceApi->apiInvoiceGet: %s\n" % e)
				raise orm.except_orm(('Erreur'),("Contactez votre administrateur système. Merci"))

		else:

			raise orm.except_orm(('Attention'),("La facture a déjà été normalisée. Merci!!!"))
		
		return True

	def generate_qr_code(self, qrcode_string):

		db_id = self.env['ir.config_parameter'].search([('key', '=', 'database.uuid')]).value

		qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=20,border=4,)
		name = '_qr.png'#self.default_code+'_Product.png'
		qr.add_data(qrcode_string) #you can put here any attribute SKU in my case
		qr.make(fit=True)
		img = qr.make_image()
		buffer = cStringIO.StringIO()
		img.save(buffer, format="PNG")
		path = os.path.dirname(os.path.realpath(__file__))+"\\..\\report\\qrcode\\"+str(self.ids[0])+"_"+str(db_id)+"_qr.png"
		path = path.replace('\\', '/')
		#raise orm.except_orm(('MESSAGE!'),("Reponse : "+str(path)))

		img.save(path)
		img_str = base64.b64encode(buffer.getvalue())
		#self.write({'qrcode_string': path})
		return path

	def get_qr_code(self):
		if self.qrcode_path_norm:
			if not os.path.isfile(self.qrcode_path_norm):
				self.qrcode_path_norm = self.generate_qr_code(self.qrcode_norm)
		else:
			self.qrcode_path_norm = self.generate_qr_code(self.qrcode_norm)
		return self.qrcode_path_norm

	def prepare_invoice(self, ifu):

		# init all variables
		invoice_request_data_dto = InvoiceRequestDataDto()

		# IFU DU VENDEUR
		invoice_request_data_dto.ifu = ifu

		# OPERATEUR OU UTILISATEUR CONNECTE
		operator_dto = OperatorDto()
		operator_dto.id = self.env.user.id
		operator_dto.name = self.env.user.name
		invoice_request_data_dto.operator = operator_dto

		# TYPE DE FACTURE
		type_facture = self.type
		if type_facture == 'out_invoice':
			invoice_type = InvoiceTypeEnum.FV
			if self.facture_exportation:
				invoice_type = InvoiceTypeEnum.EV
		elif type_facture == 'out_refund':
			invoice_type = InvoiceTypeEnum.FA
			if self.facture_exportation:
				invoice_type = InvoiceTypeEnum.EA
		# raise orm.except_orm(('Erreur'), (invoice_type))
		invoice_request_data_dto.type = invoice_type

		# DONNEES DU CLIENT
		# if self.client == True:
		client = self.partner_id

			# ifu
		ifu_client = ""
		if client.ifu:
			ifu_client = client.ifu
		

			# contact
		contact_client = ""
		if client.phone:
			contact_client += "T: " + client.phone +"\n"
		if client.mobile:
			contact_client += "M: " + client.mobile +"\n"
		if client.email:
			contact_client += "C: " + client.email

			# adresse
		adresse_client = ""
		if client.street:
			adresse_client += client.street + "\n"
		if client.street2:
			adresse_client += client.street2 + "\n"
		if client.city:
			adresse_client += client.city
			if client.state_id:
				adresse_client += ", " + client.state_id.name
			if client.zip:
				adresse_client += ", " + client.zip
			adresse_client += "\n"
		if client.country_id:
			adresse_client += client.country_id.name

		# raise orm.except_orm(("Erreur"), (adresse_client))
		
		client_dto = ClientDto(ifu_client, client.name, contact_client, adresse_client)
		invoice_request_data_dto.client = client_dto

		# PAIEMENT
		invoice_request_data_dto.payment = []
		payment_dto = PaymentDto()
		mode_paiement = self.payment_method_id.type_paiement_id.type
		if mode_paiement:
			if mode_paiement == 'ESPECES':
				payment_dto_name = PaymentTypeEnum.ESPECES
			elif mode_paiement == 'VIREMENT':
				payment_dto_name = PaymentTypeEnum.VIREMENT
			elif mode_paiement == 'CARTEBANCAIRE':
				payment_dto_name = PaymentTypeEnum.CARTEBANCAIRE
			elif mode_paiement == 'MOBILEMONEY':
				payment_dto_name = PaymentTypeEnum.MOBILEMONEY
			elif mode_paiement == 'CHEQUES':
				payment_dto_name = PaymentTypeEnum.CHEQUES
			elif mode_paiement == 'CREDIT':
				payment_dto_name = PaymentTypeEnum.CREDIT
			elif mode_paiement == 'AUTRE':
				payment_dto_name = PaymentTypeEnum.AUTRE
		else:
			payment_dto_name = PaymentTypeEnum.ESPECES
		payment_dto.name = payment_dto_name
		payment_dto.amount = self.amount_total

		# raise orm.except_orm(('Erreur'), (payment_dto))

		# payment_dto = PaymentDto(payment_dto_name, self.amount_total)
		invoice_request_data_dto.payment.append(payment_dto)

		aib = False
		# ARTICLES
		invoice_request_data_dto.items = []
		invoice_lines = self.invoice_line
		if invoice_lines:
			i = 0
			aiba = aibb = 0
			for invoice_line in invoice_lines:
				i += 1
				invoice_line_taxes = invoice_line.invoice_line_tax_id
				tax_group = TaxGroupTypeEnum.A
				for invoice_line_taxe in invoice_line_taxes:
					groupe_taxation = invoice_line_taxe.groupe_taxation_id.reference
					if groupe_taxation == 'A':
						tax_group = TaxGroupTypeEnum.A
					elif groupe_taxation == 'B':
						tax_group = TaxGroupTypeEnum.B
					elif groupe_taxation == 'C':
						tax_group = TaxGroupTypeEnum.C
					elif groupe_taxation == 'D':
						tax_group = TaxGroupTypeEnum.D
					elif groupe_taxation == 'E':
						tax_group = TaxGroupTypeEnum.E
					elif groupe_taxation == 'F':
						tax_group = TaxGroupTypeEnum.F
					elif groupe_taxation == 'AIBA':
						aiba += 1
					elif groupe_taxation == 'AIBB':
						aibb += 1
					
				article = ItemDto()
				article.code = invoice_line.product_id.default_code
				article.name = invoice_line.name
				if invoice_line.remise_montant == 0.0:
					article.price = invoice_line.price_unit
				else:
					article.original_price = invoice_line.price_unit
					article.price_modification = "Remise " + str(invoice_line.discount) + "%"
					article.price = round(invoice_line.price_unit - invoice_line.remise_montant)
					
				article.quantity = invoice_line.quantity
				if invoice_line.taxe_specifique != 0.0:
					article.tax_specific = invoice_line.taxe_specifique
				article.tax_group = tax_group
				# article.tax_specific = tax_
				# article.original_price = 
				# article.price_modification = tax_group

				invoice_request_data_dto.items.append(article)

			if (aiba != 0 and aibb != 0):
				raise orm.except_orm(('Erreur'),("Vous ne pouvez pas appliquer deux types d'AIB sur une même facture. Merci!!!"))
			else:
				if (aiba != 0 and aiba != i) or (aibb != 0 and aibb != i):
					raise orm.except_orm(('Erreur'),("Vous devez appliquer l'AIB sur toutes les lignes d'articles. Merci!!!"))
				else:
					if aiba != 0:
						aib = AibGroupTypeEnum.A
					elif aibb != 0:
						aib = AibGroupTypeEnum.B
			
		else:

			raise orm.except_orm(('Erreur'),("Cette facture n\'a pas de lignes d'articles. Veuillez corriger SVP!!!"))

		# AIB
		if aib:
			invoice_request_data_dto.aib = aib
		
		# REFERENCE
		if type_facture == 'out_refund':
			original_invoice = self.env['account.invoice'].search([('type', '=', 'out_invoice'),('internal_number', '=', self.origin)])
			if len(original_invoice) == 0 :
				raise orm.except_orm(('Erreur'), ('Cette facture d\'avoir n\'a pas de facture originale.'))
			else:
				for invoice_origin in original_invoice:
					if invoice_origin.facture_exportation:
						if not self.facture_exportation:
							raise orm.except_orm(('Erreur'), ('La facture d\'origine est une facture d\'exportation. Veuillez donc marquer la facture d\'avoir comme facture d\'exportation. Merci'))
					if not invoice_origin.etat_norm:
						raise orm.except_orm(('Erreur'), ('Avant de normaliser une facture d\'avoir, vous devez d\'abord normaliser sa facture originale!\n'
						'Facture originale: %s' %(invoice_origin.internal_number)))
					else:
						invoice_request_data_dto.reference = invoice_origin.code_mecef_dgi_norm
						self.write({
							'rn_norm': invoice_origin.code_mecef_dgi_norm
						})
				
		return invoice_request_data_dto

	def soumettre_invoice(self, api_invoice_instance, invoice_request_data_dto):

		# Envoi de la facture pour demande
		invoice_response_data_dto = api_invoice_instance.api_invoice_post(body=invoice_request_data_dto)

		if invoice_response_data_dto.uid is not None:

			self.write({
				'uid_e_mcf' : invoice_response_data_dto.uid,
				'type_fact': invoice_request_data_dto.type,
				'ta' : invoice_response_data_dto.ta,
				'tb' : invoice_response_data_dto.tb,
				'tc_norm' : invoice_response_data_dto.tc,
				'td' : invoice_response_data_dto.td,
				'taa' : invoice_response_data_dto.taa,
				'tab' : invoice_response_data_dto.tab,
				'tac' : invoice_response_data_dto.tac,
				'tad' : invoice_response_data_dto.tad,
				'tae' : invoice_response_data_dto.tae,
				'taf' : invoice_response_data_dto.taf,
				'hab' : invoice_response_data_dto.hab,
				'had' : invoice_response_data_dto.had,
				'vab' : invoice_response_data_dto.vab,
				'vad' : invoice_response_data_dto.vad,
				'aib_norm' : invoice_response_data_dto.aib,
				'ts' : invoice_response_data_dto.ts,
				'total' : invoice_response_data_dto.total,
			})
		
		else:

			_logger.info('Erreur: Demande de facture \n'
							'Code erreur: %s \n'
							'Description erreur: %s', invoice_response_data_dto.error_code, invoice_response_data_dto.error_desc)
			
			raise orm.except_orm(('Erreur: Demande de facture'),("Code erreur: %s \n"
											"Description erreur: %s" %(invoice_response_data_dto.error_code, invoice_response_data_dto.error_desc)))

		return True

	def verifier_conformite(self):

		total_api = float(self.total)
		total_invoice = self.amount_total

		if total_api != total_invoice:
			raise orm.except_orm(('Processus de normalisation de la facture suspendue'),('Les totaux de l\'API et d\'ODOO ne correspondent pas. \n'
			' API : %s , ODOO : %s '% (total_api, total_invoice)))
		
		return True

	def confirmer_invoice(self, api_invoice_instance=None):

		if api_invoice_instance is None:
			datas = self.check_api_operationnel()
			api_invoice_instance = datas[0]

		transaction_id = self.uid_e_mcf

		success = self.verifier_conformite()

		if success:

			# Confirmation normalisation
			security_elements_dto = api_invoice_instance.api_invoice_uid_confirm_put(transaction_id)

			if security_elements_dto.code_me_ce_fdgi:

				# self.pool.get('account.invoice').browse(self.cr, self.uid, self.ids[0]).write(

				self.write({
					'etat_norm' : True,
					'datetime_norm': security_elements_dto.date_time,
					'qrcode_norm': security_elements_dto.qr_code,
					'qrcode_path_norm': self.generate_qr_code(security_elements_dto.qr_code),
					'code_mecef_dgi_norm': security_elements_dto.code_me_ce_fdgi,
					'counters_norm': security_elements_dto.counters,
					'nim_norm': security_elements_dto.nim,
					'norm_by': self.env.user.id,

				})
			
			else:

				_logger.info('Erreur: Confirmation facture \n'
								'Code erreur: %s \n'
								'Description erreur: %s', security_elements_dto.error_code, security_elements_dto.error_desc)
				
				raise orm.except_orm(('Erreur: Confirmation facture'),("Code erreur: %s \n"
													"Description erreur: %s" %(security_elements_dto.error_code, security_elements_dto.error_desc)))

		return True


# class account_invoice_line(models.Model):
# 	_inherit = "account.invoice.line"

# 	taxe_specifique  = fields.Float(string ='Taxe spécifique (Pour Qte total)')
# 	desc_ts  = fields.Char(string ='Description TS')
# 	# pu_ht = fields.Float(string='PU HT')
# 	# lettretaxe  = fields.Char(string ='Lettre taxe')
# 	# montant_taxe  = fields.Float(string ='Montant taxes')
# 	remise_montant  = fields.Float(compute='_compute_price', string ='Remise')

# 	@api.one
# 	@api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity',
# 		'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'taxe_specifique')
# 	def _compute_price(self):

# 		price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
# 		# d_p = modf(price)
# 		# if self.discount == 0.0:
# 		# 	if d_p[0] <= 0.5:
# 		# 		price = d_p[1]
# 		# else:
# 		# 	price = round(price)

# 		# price_x = self.price_unit
# 		# d_p = modf(price_x)
# 		# if self.discount == 0.0:
# 		# 	if d_p[0] <= 0.5:
# 		# 		price_x = d_p[1]
			
# 		# else:
# 		# 	price_x = round(price_x)
# 		# self.price_unit = price_x

# 		taxes = self.invoice_line_tax_id.compute_all(price, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id, taxe_specifique=self.taxe_specifique)
# 		# ts = 0.0
# 		# if self.invoice_line_tax_id.name != False:
# 		# 	if "exception" in self.invoice_line_tax_id.name :
# 		# 		ts = round(self.taxe_specifique/1.18)
# 		# 	else:
# 		# 		ts = self.taxe_specifique
# 		# self.lol = "test"
# 		pu_ht = self.price_unit / 1.18
# 		if len(self.invoice_line_tax_id) != 0:
# 			self.pu_ht = round(pu_ht, 2)
# 		else:
# 			self.pu_ht = round(self.price_unit, 2)

# 		# raise orm.except_orm(('MESSAGE!'),(self.pu_ht, self.lol))

# 		# self.remise_montant = pu_ht * (self.discount / 100) 
# 		self.remise_montant = self.price_unit * (self.discount / 100) 
# 		self.price_subtotal = taxes['total']
# 		# self.price_subtotal = round(taxes['total'] + self.taxe_specifique)
# 		# raise orm.except_orm(('MESSAGE!'),("Reponse : "+str(taxes)))