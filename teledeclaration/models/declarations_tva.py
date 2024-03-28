from odoo import fields, models, api


class DeclarationsTva(models.Model):
    _name = "declarations.tva"
    _description = "Declarations TVA"
    _rec_name = 'reference'

    reference = fields.Char("Reference", required=True)
    id_fiscal = fields.Integer("Identifiant Fiscal", required=True)
    regime = fields.Selection([('1', 'Mensuel'), ('2', 'Trimestriel')], string="Regime", required=True)
    date = fields.Date("Date", default=lambda self: fields.Datetime.today())
    annee = fields.Integer("Annee", required=True)
    type = fields.Selection([('encaissement', 'Encaissement'), ('debit', 'Debit'), ('credit', 'Credit')], string="Type",
                            required=True, default='debit')
    periode = fields.Char("Periode", required=True)
    lignes_facture_ids = fields.Many2many('lignes.facture')
    file_name = fields.Char()

    def filter(self):
        start_of_month = self.date.replace(day=1)
        end_of_month = self.date.replace(day=31)
        self.lignes_facture_ids = self.env['lignes.facture'].search([('date_paiement', '>=', start_of_month),
                                                                     ('date_paiement', '<=', end_of_month)])

    @api.onchange('date')
    def _onchange_date(self):
        self.reference = f"Declaration {self.date.strftime('%B %Y')}"
        self.file_name = f"{self.date.strftime('%B %Y')}.xml"
        self.periode = self.date.month
