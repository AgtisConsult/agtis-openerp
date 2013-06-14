# -*- encoding: utf-8 -*-
#################################################################################
#                                                                               #
# Copyright (C) 2013 Agtis Consultoria                                          #
#                                                                               #
#This program is free software: you can redistribute it and/or modify           #
#it under the terms of the GNU Affero General Public License as published by    #
#the Free Software Foundation, either version 3 of the License, or              #
#(at your option) any later version.                                            #
#                                                                               #
#This program is distributed in the hope that it will be useful,                #
#but WITHOUT ANY WARRANTY; without even the implied warranty of                 #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                  #
#GNU Affero General Public License for more details.                            #
#                                                                               #
#You should have received a copy of the GNU Affero General Public License       #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.          #
#################################################################################

{
    'name' : 'Integração com TecnoSpeed eDoc Manager',
    'description' : 'Faz integração do envio da NF-e com software eDocManager da TecnoSpeed',
    'category' : 'Localisation',
    'license': 'AGPL-3',
    'author' : 'Agtis Consultoria',
    'website' : 'http://www.agtis.inf.br',
    'version' : '0.1',
    'depends' : [
		        'account',
                'account_cancel',  
		        'l10n_br_account',
                'fetchmail', 
		        ],
    'init_xml' : [
		        #'l10n_br_account_payment_extension.csv',
		        ],
    'update_xml' : [
                    'company_view.xml',
                    'wizard/edoc_wizard.xml',
                    'account_nfe_data.xml',
		            'account_nfe_view.xml',
                    'security/ir.model.access.csv',
                    'security/security.xml',
                    'account_workflow.xml',
                    ],
    'demo_xml': [
                'account_nfe_demo.xml'
                ],
    'installable': True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
