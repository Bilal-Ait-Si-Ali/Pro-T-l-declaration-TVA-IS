from odoo import fields, models, api


class LignesFacture(models.Model):
    _name = "lignes.facture"
    _description = "Lignes de Facture"

    num_ordre = fields.Integer("Num D'Ordre", required=True)
    num_facture = fields.Char("Num de Facture", required=True)
    date_facture = fields.Date("Date de la Facture")
    designation = fields.Char("Designation des Biens et Services", required=True)
    nom_fournisseur = fields.Char("Nom du Fournisseur", required=True)
    id_fiscal_fournisseur = fields.Integer("Identifiant Fiscal Fournisseur", required=True)
    ice = fields.Char("ICE", required=True)
    montant_ht = fields.Integer("Montant HT", required=True)
    taux = fields.Integer("Taux", required=True, default=20)
    montant_tva = fields.Integer("Montant TVA", required=True,
                                 compute='_compute_montant_tva')
    montant_ttc = fields.Integer("Montant TTC", required=True, compute='_compute_montant_ttc')
    mode_paiement = fields.Selection(
        [('1', 'Espèces'), ('2', 'Chèque'), ('3', 'Prélèvement'), ('4', 'Virement'), ('5', 'Effets'),
         ('6', 'Compensation'), ('7', 'Autres')], string="Mode de Paiement", required=True)

    date_paiement = fields.Date("Date de Paiement", required=True)
    declarer = fields.Boolean("A declarer")

    @api.depends('montant_ht', 'taux')
    def _compute_montant_tva(self):
        for rec in self:
            if rec.montant_ht:
                rec.montant_tva = rec.montant_ht * (rec.taux / 100)
            else:
                rec.montant_tva = 0

    @api.depends('montant_tva', 'montant_ht')
    def _compute_montant_ttc(self):
        for rec in self:
            if rec.montant_ht:
                rec.montant_ttc = rec.montant_ht + rec.montant_tva
            else:
                rec.montant_ttc = 0
