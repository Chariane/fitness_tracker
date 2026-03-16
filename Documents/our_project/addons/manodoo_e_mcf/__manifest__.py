# -*- coding: utf-8 -*-
{
    'name': "MANODOO e-MCF",

    'summary': """
        Normalisation de factures """,

    'description': """
        Ajout de l'option de normalisation des factures de vente et d'avoir
    """,

    'author': "3D TECHLOGIS",
    'website': "http://www.3dtechlogis.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'sale',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/account_payment_method_view.xml',
        'views/account_tax_view.xml',
        'views/groupe_taxation_view.xml',
        'views/manodoo_e_mcf_view.xml',
        'views/type_paiement_view.xml',
        'data/groupes_taxation_data.xml',
        'data/types_paiement_data.xml',
        'report/facture_e_mcf_config.xml',
        'report/facture_e_mcf_template.xml',
        'report/situation_factures_norm_template.xml',
        'wizard/situation_norm_wizard_view.xml',
        # 'menu.xml',
    ],
    'installable':True,
    'application': True,
    
}