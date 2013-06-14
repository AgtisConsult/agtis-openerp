# -*- encoding: utf-8 -*-

from osv import fields,osv
import pooler


class select_fo_to_return(osv.osv_memory):
    _name="account.inv.nfe.return.ind"
    _columns={
              'fiscal_operation_id': fields.many2one(
                'l10n_br_account.fiscal.operation',
                'Operacao fiscal de retorno',)
              }    
    def default_get(self, cr, uid, fields_list, context=None):
        cfop_obj = self.pool.get('l10n_br_account.cfop')
        cfop_id = cfop_obj.search(cr,uid,args=[('code','=','5902')])[0]
        
        obj_fo = self.pool.get('l10n_br_account.fiscal.operation')
        fo_id = obj_fo.search(cr,uid,args=[('cfop_id','=',cfop_id)])[0]
        return {'fiscal_operation_id':fo_id}
    
    def do_create_return_invoice(self,cr,uid,ids,context=None):
        data = self.browse(cr,uid,ids)
        fo_id = 0
        for wiz in data:
            fo_id = wiz.fiscal_operation_id.id
        ctx = {'fiscal_operation_id':fo_id}
        inv = self.pool.get('account.invoice').browse(cr,uid,context.get('active_id'),context=ctx)

        ret = inv.create_return_invoice()
        return ret
        
        
        
class create_charging_from_invoice(osv.osv_memory):
    _name="account.create.charging.from.invoice"
    _columns={
              'invoice_ids': fields.many2many('account.invoice',
                 'account_charging_wiz_rel',
                 'wizard_id',
                 'invoice_id',
                 'Faturas',readonly=True),
              'info': fields.text('Avisos',size=1024,readonly=True)
              }
    
    def default_get(self, cr, uid, fields_list, context=None):
        info = ''
        if context is None:
            context = {}
        inv_brw = self.pool.get('account.invoice').browse(cr, uid, context.get('active_ids',[]))
        charge_inv_ids = []
        partner_id = None
        if inv_brw:
            partner_id=inv_brw[0].partner_id.id
            
        for inv in inv_brw:
            
            if inv.partner_id.id != partner_id:
                raise osv.except_osv(u"Erro","Uma ou mais faturas selecionadas nao sao do mesmo cliente")
            
            if inv.state in ['open','paid']:
#                 charge_inv_ids.append(inv.id) 
                if inv.ind_is_return:
                    is_industrialization = False
                    for cfop in inv.cfop_ids:
                        if cfop.code == '5902':
                            is_industrialization = True
                            break
                    if is_industrialization:
                        
                        if inv.ind_charging_state == 'no_charge':
                            charge_inv_ids.append(inv.id)
                        else:
                            info += u'- NF %s ja teve nota de cobranca. Utilize o botao Gerar Cobranca diretamente na fatura para gerar nova nota de cobranca para esta nota.\n' % (inv.internal_number or 's/n')
                    else:
                        info += u'- NF %s nao e nota de retorno de industrialiacao ou e nota de retorno de mercadoria nao industrializada.\n' % (inv.internal_number or 's/n')                
                else:
                    info += u'- NF %s nao e nota de retorno.\n' % (inv.internal_number or 's/n')
            else:
                info += u'- NF %s esta com status que nao e nem Aberta nem Paga.\n' % (inv.internal_number or 's/n')
        return {'info':info,
                'invoice_ids':charge_inv_ids}
    
    
    def charge_multi_invoice(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get('account.invoice')
        data = self.read(cr,uid,ids,context=context)
        cids = data[0]['invoice_ids']
        return inv_obj.create_charging_invoice( cr, uid, cids, context=context)
    
    
    
