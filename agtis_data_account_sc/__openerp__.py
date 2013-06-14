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
    "name" : "Agtis Data Extension for Account SC",
    "description" : "Agtis Data Extension for Account SC",
    'license': 'AGPL-3',
    "author" : "Agits Consultoria",
    "version" : "0.1",
    "depends" : [
                 "l10n_br_account",
                 ],
    'init_xml': [
                
                'account_fiscal_position_rule_data.xml',
                
                ],
    "update_xml" : [

                   ],
    'demo_xml': [
                #'l10n_br_data_account_demo.xml'
                ],
    "category" : "Localisation",
    "active": False,
    "installable": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
