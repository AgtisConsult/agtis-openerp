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

#import time
#import netsvc
from osv import fields, osv
#import decimal_precision as dp
#import pooler
#from tools import config
#from tools.translate import _
#from datetime import datetime
#import httplib, urllib ,base64,requests
#import netsvc

#from inspect import getmembers
#from pprint import  pprint



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:



class company(osv.osv):
    _inherit="res.company"
    _columns = {
    'edoc_host':fields.char('Servidor eDoc', size=255),
	'edoc_port':fields.integer('Porta Servidor eDoc'),
	'edoc_group':fields.char('Grupo eDoc', size=20),
	'edoc_user':fields.char('Usuario eDoc', size=30),
	'edoc_password':fields.char('Senha eDoc', size=30),
	'edoc_nfe_prox_lote':fields.integer('Nr Prox Lote NF-e', size=30),
    'edoc_nfe_email_subject':fields.char('Assunto do email envio', size=255),
    'edoc_nfe_email_text_send':fields.char('Texto email envio', size=255),
    'edoc_nfe_email_subject_cancel':fields.char('Assunto do email canelamento', size=255),
    'edoc_nfe_email_text_cancel':fields.char('Texto email cancelamento', size=255),
    'edoc_nfe_environment':fields.boolean('Ambiente de Produção')
    }
company()


