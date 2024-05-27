from odoo import fields, models, tools


class AccountReportSar(models.Model):
    _name = 'account.report.sar'
    _description = 'Reporte de libros contables SAR'
    _auto = False

    fecha = fields.Date(readonly=True)
    empresa = fields.Char(readonly=True)
    #sucursal = fields.Char(readonly=True)
    #branch_ids = fields.Char(readonly=True)
    rtn = fields.Char(readonly=True)
    state = fields.Selection([
        ('draft', 'Unposted'), ('posted', 'Posted'), ('cancel', 'Cancelled')], 'Status', readonly=True)
    factura = fields.Char(readonly=True)

    no_tax_def = fields.Monetary(readonly=True, string='Sin Ind. Impuesto', currency_field='company_currency_id')
    isvimp = fields.Monetary(readonly=True, string='isvimp', currency_field='company_currency_id')
    exeimp = fields.Monetary(readonly=True, string='', currency_field='company_currency_id')
    isvr10 = fields.Monetary(readonly=True, string='', currency_field='company_currency_id')
    exento = fields.Monetary(readonly=True, string='Importe Exento', currency_field='company_currency_id')
    exonerado = fields.Monetary(readonly=True, string='Importe Exonerado', currency_field='company_currency_id')
    gravado = fields.Monetary(readonly=True, currency_field='company_currency_id')
    gravado15 = fields.Monetary(readonly=True, string='Gravado 15%', currency_field='company_currency_id')
    gravado18 = fields.Monetary(readonly=True, string='Gravado 18%', currency_field='company_currency_id')
    impuesto15 = fields.Monetary(readonly=True, string='Impuesto 15%', currency_field='company_currency_id')
    impuesto18 = fields.Monetary(readonly=True, string='Impuesto 18%', currency_field='company_currency_id')
    impuesto = fields.Monetary(readonly=True, string='Impuesto Total', currency_field='company_currency_id')
    total = fields.Monetary(readonly=True, currency_field='company_currency_id')
    type = fields.Char(readonly=True)
    journal_id = fields.Many2one('account.journal', readonly=True, auto_join=True)
    company_id = fields.Many2one('res.company', readonly=True, auto_join=True)
    company_currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    move_id = fields.Many2one('account.move', string='Entry', auto_join=True)

    def init(self):
        cr = self._cr
        tools.drop_view_if_exists(cr, self._table)
        query = """ select A.id,
                A.id as move_id,
                A.type,
                A.fecha,
                A.factura,
                A.state,
                A.journal_id,
                A.company_id,
                A.currency_id,
                A.empresa,
                A.rtn,
                case when A.state != 'cancel' then A.exento else 0.00 end as exento,
                case when A.state != 'cancel' then A.exonerado else 0.00 end as exonerado,
                case when A.state != 'cancel' then A.gravado else 0.00 end as gravado,
                case when A.state != 'cancel' then A.gravado15 else 0.00 end as gravado15,
                case when A.state != 'cancel' then A.gravado18 else 0.00 end as gravado18,
                case when A.state != 'cancel' then A.isv15 else 0.00 end as impuesto15,
                case when A.state != 'cancel' then A.isv18 else 0.00 end as impuesto18,
                0 as no_tax_def,
                case when A.state != 'cancel' then A.isvimp else 0.00 end as isvimp,
                case when A.state != 'cancel' then A.exeimp else 0.00 end as exeimp,
                case when A.state != 'cancel' then A.exexport else 0.00 end as exexport,
                0 as isvr10,
                0 as impuesto,
                case when A.state != 'cancel' then A.montototal else 0.00 end as total
            from
            (select t1.id,
            t1.type ,
            t1.fecha,
            t1.factura,
            t1.state ,
            t1.journal_id,
            t1.company_id,
            t1.currency_id,
            t1.empresa,
            t1.rtn,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            t1.exento *(-1)
            else
            t1.exento end end as exento, 
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            case when t1.moneda_id = 1 then
            (t1.montototal - t1.Gravado15)*(-1)
            else
            (t1.Gravado15ISV - t1.Gravado15)*(-1)
            end
            else
            case when t1.moneda_id = 1 
            then (t1.montototal - t1.Gravado15)
            else
            t1.Gravado15ISV - t1.Gravado15 end end end as isv15,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.Gravado18ISV - t1.Gravado18)*(-1)
            else
            t1.Gravado18ISV - t1.Gravado18 end end as isv18,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.isvimportacion)*(-1)
            else
            t1.isvimportacion end end as isvimp,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.exeimportacion)*(-1)
            else 
            case when t1.moneda_id = 1
            then (t1.exeimportacion / t1.moneda)
            else
            t1.exeimportacion end end end as exeimp,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.exexportaciones)*(-1)
            else 
            case when t1.moneda_id = 1
            then (t1.exexportaciones / t1.moneda)
            else
            t1.exexportaciones end end end as exexport,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.Gravado15 + t1.Gravado18)*(-1)
            else
            t1.Gravado15 + t1.Gravado18 end end as gravado,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.Gravado15)*(-1)
            else
            t1.Gravado15 end end as gravado15,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.Gravado18)*(-1)
            else
            t1.Gravado18 end end as gravado18,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' then
            (t1.exonerado)*(-1)
            else
            t1.exonerado end end as exonerado,
            case when t1.state ='cancel' then 0
            else
            case when t1.type = 'out_refund' or (t1.type = 'in_invoice' and t1.exeimportacion > 0) then
            (t1.montototal)*(-1)
            else 
            t1.montototal end end as montototal
            from (select am.id,
                am.move_type as type,
                am.invoice_date as fecha,
                CASE WHEN am.move_type = 'in_invoice'
                        THEN am.ref
                        else am.name end AS factura,
                am.state,
                am.journal_id,
                am.company_id,
                rc.currency_id,
                rp.name AS empresa,
                rp.vat AS rtn,
                (select case when aml.currency_id = 2 then case when am.move_type='out_refund' or am.move_type = 'in_invoice' then sum(aml.debit) else sum(aml.credit) end  else sum(aml.price_subtotal)end as gravado15
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and (at2."name"->>'es_GT' = 'ISV 15%' or at2."name"->>'es_GT' = 'ISC 15%') group by aml.currency_id) as Gravado15 ,
                    (select sum(aml.price_total)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and (at2."name"->>'es_GT' = 'ISV 15%' or at2."name"->>'es_GT' = 'ISC 15%')) as Gravado15ISV,
                    (select sum(aml.price_subtotal)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and (at2."name"->>'es_GT' = 'ISV 18%' or at2."name"->>'es_GT' = 'ISC 18%')) as Gravado18 ,
                    (select sum(aml.price_total)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and (at2."name"->>'es_GT' = 'ISV 18%' or at2."name"->>'es_GT' = 'ISC 18%')) as Gravado18ISV,
                    (select sum(aml.price_total)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and (at2."name"->>'es_GT' = 'EXE' or at2."name"->>'es_GT' = 'EXEC')) as exento,
                    (select sum(aml.price_total)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and (at2."name"->>'es_GT' = 'EXO' or at2."name"->>'es_GT' = 'EXOC')) as exonerado,
                    (select sum(aml.price_total)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and at2.name->>'es_GT' = 'EXEIMP') as exeimportacion,
                    (select sum(aml.price_total)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and at2.name->>'es_GT' = 'EXEXPORT') as exexportaciones,
                    (select sum(aml.price_total)
                    from account_move_line aml
                    left join account_move_line_account_tax_rel amlatr on amlatr.account_move_line_id = aml.id
                    left join account_tax at2 on amlatr.account_tax_id  = at2.id 
                    where   aml.account_id <> '51' and aml.account_id <> '881' and aml.move_id  = am.id  and at2."name"->>'es_GT' = 'ISVIMP') as isvimportacion,
                    case when am.currency_id = 1
                    then 
                    case when am.move_type='out_refund' or am.move_type = 'in_invoice' then 
                    (am.amount_total_signed)*(-1)
                    else am.amount_total_signed
                    end
                    else 
                    am.amount_total end as montototal,
                    (select rcr.rate
                    from res_currency_rate rcr 
                    inner join account_move am2 on am2.currency_id = rcr.currency_id
                    where rcr.currency_id = am2.currency_id 
                    and to_date(to_char(rcr.name,'YYYY/MM/DD'),'YYYY/MM/DD')  = to_date(to_char(am2.date,'YYYY/MM/DD'),'YYYY/MM/DD') and am2."name" = am.name
                    limit 1) as moneda,
                    am.currency_id as moneda_id
            from account_move am 
            left join res_partner as rp on am.partner_id = rp.id
            left join res_company as rc on am.company_id = rc.id
            left join account_journal as aj on am.journal_id = aj.id
            where coalesce (am.l10n_latam_document_type_id,0) <> 24 and aj.incluido_en_libros is True
            and am.state in ('posted','cancel')) as t1) as A
        """ # noqa
        sql = """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, query)
        cr.execute(sql)
