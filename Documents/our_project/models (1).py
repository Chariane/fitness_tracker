from typing import Optional
import datetime
import decimal

from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, JSON, LargeBinary, Numeric, PrimaryKeyConstraint, SmallInteger, String, Table, Text, Time, UniqueConstraint, text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass



#================================================Schemas Public========================================================

class Utilisateur(Base):
    __tablename__ = 'utilisateur'
    __table_args__ = (
        CheckConstraint("badge::text = ANY (ARRAY['Aucun'::character varying, 'Bronze'::character varying, 'Argent'::character varying, 'Or'::character varying, 'Platine'::character varying, 'Diamant'::character varying]::text[])", name='utilisateur_badge_check'),
        CheckConstraint("genre::text = ANY (ARRAY['Homme'::character varying, 'Femme'::character varying, 'Autre'::character varying]::text[])", name='utilisateur_genre_check'),
        CheckConstraint("length(email::text) <= 255 AND email::text ~* '^[A-Za-z0-9._%%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$'::text", name='utilisateur_constr_email_check'),
        CheckConstraint("statut::text = ANY (ARRAY['Actif'::character varying, 'Suspendu'::character varying, 'Supprimé'::character varying]::text[])", name='utilisateur_constr_statut'),
        PrimaryKeyConstraint('id', name='utilisateur_pk'),
        UniqueConstraint('email', name='utilisateur_constr_email'),
        {'comment': "Table pour tout utilisateur pouvant s'authentifier n'importe où "
                'sur toute la plateforme',
     'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    username: Mapped[str] = mapped_column(String(150), nullable=False, comment="Nom d'utilisateur, par defaut ce sera Nom+Prenoms si c'une personne physique sinon le nom de l'entreprise or entité")
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    statut: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'Actif'::character varying"), comment="in ( 'Actif', 'Suspendu',  'Supprimé')")
    is_utilisateur_verifie: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment="indicateur sur vérification supplémentaire d'identité d'utilisateur")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'), comment="date d'inscription")
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'), comment='date de modification')
    nom: Mapped[Optional[str]] = mapped_column(String(100))
    prenoms: Mapped[Optional[str]] = mapped_column(String(100))
    mot_de_passe: Mapped[Optional[str]] = mapped_column(String(255))
    email_verified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    is_enregistre_par_id_entreprise: Mapped[Optional[str]] = mapped_column(String(12))
    is_entreprise: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'), comment="Si c'est entreprise ou candidat")
    is_admin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    is_super_admin: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    badge: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'Aucun'::character varying"))
    token_confirmation_email: Mapped[Optional[str]] = mapped_column(String(255))
    date_exp_token_confirmation_email: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    genre: Mapped[Optional[str]] = mapped_column(String(10))
    photo: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    date_nais: Mapped[Optional[datetime.date]] = mapped_column(Date)
    pays: Mapped[Optional[str]] = mapped_column(String(100))
    ville: Mapped[Optional[str]] = mapped_column(String(100))
    telephone: Mapped[Optional[str]] = mapped_column(String(20))
    biographie: Mapped[Optional[str]] = mapped_column(Text)
    otp_code: Mapped[Optional[str]] = mapped_column(String(5))
    code_verification_email: Mapped[Optional[str]] = mapped_column(String(6))
    date_exp_code_verification_email: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    google_auth_secret: Mapped[Optional[str]] = mapped_column(String(64))
    is_2fa_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    google_auth_configured_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    delivery_address: Mapped[Optional[str]] = mapped_column(String(255))
    autres: Mapped[Optional[dict]] = mapped_column(JSONB, comment="Autres informations (supplémentaires) à stocker dans la variable JSON : {'attr1': 'val1', 'attr2': 'var2', ...}")
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Pour solf-delete')
    vu_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment="Date et heure de la dernière activité de l'utilisateur")

    #Relation
    mot_de_passe_oublie: Mapped[list['MotDePasseOublie']] = relationship('MotDePasseOublie', back_populates='utilisateur')
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', uselist=False, back_populates='utilisateur')
    abonnement_utilisateur: Mapped[list['AbonnementUtilisateur']] = relationship('AbonnementUtilisateur', back_populates='utilisateur')
    formateur: Mapped[list['Formateur']] = relationship('Formateur', back_populates='utilisateur')
    activite_soc_com_cv: Mapped[list['ActiviteSocComCv']] = relationship('ActiviteSocComCv', back_populates='utilisateur')
    atout_cv: Mapped[list['AtoutCv']] = relationship('AtoutCv', back_populates='utilisateur')
    autre_cv: Mapped[list['AutreCv']] = relationship('AutreCv', back_populates='utilisateur')
    centre_interet_cv: Mapped[list['CentreInteretCv']] = relationship('CentreInteretCv', back_populates='utilisateur')
    certificat_cv: Mapped[list['CertificatCv']] = relationship('CertificatCv', back_populates='utilisateur')
    experience_cv: Mapped[list['ExperienceCv']] = relationship('ExperienceCv', back_populates='utilisateur')
    formation_cv: Mapped[list['FormationCv']] = relationship('FormationCv', back_populates='utilisateur')
    reference_cv: Mapped[list['ReferenceCv']] = relationship('ReferenceCv', back_populates='utilisateur')
    reseau_soc_cv: Mapped[list['ReseauSocCv']] = relationship('ReseauSocCv', back_populates='utilisateur')
    resume_cv: Mapped[list['ResumeCv']] = relationship('ResumeCv', back_populates='utilisateur')
    contact: Mapped[list['Contact']] = relationship('Contact', foreign_keys='[Contact.addressee_id]', back_populates='addressee')
    contact_: Mapped[list['Contact']] = relationship('Contact', foreign_keys='[Contact.requester_id]', back_populates='requester')
    groupe: Mapped[list['Groupe']] = relationship('Groupe', back_populates='utilisateur')
    room: Mapped[list['Room']] = relationship('Room', foreign_keys='[Room.member1]', back_populates='utilisateur')
    room_: Mapped[list['Room']] = relationship('Room', foreign_keys='[Room.member2]', back_populates='Utilisateur_')
    workspace: Mapped[list['Workspace']] = relationship('Workspace', back_populates='utilisateur')
    audit_log: Mapped[list['AuditLog']] = relationship('AuditLog', back_populates='utilisateur')
    notification: Mapped[list['Notification']] = relationship('Notification', back_populates='utilisateur')
    cv: Mapped[list['Cv']] = relationship('Cv', back_populates='utilisateur')
    groupe_members: Mapped[list['GroupeMembers']] = relationship('GroupeMembers', back_populates='utilisateur')
    message: Mapped[list['Message']] = relationship('Message', back_populates='utilisateur')
    notification_: Mapped[list['Notification_']] = relationship('Notification_', back_populates='utilisateur')
    candidat: Mapped[Optional['Candidat']] = relationship('Candidat', uselist=False, back_populates='utilisateur')
    avis: Mapped[list['Avis']] = relationship('Avis', back_populates='utilisateur')
    inscription_formation: Mapped[list['InscriptionFormation']] = relationship('InscriptionFormation', back_populates='utilisateur')
    message_reaction: Mapped[list['MessageReaction']] = relationship('MessageReaction', back_populates='utilisateur')
    message_read_receipt: Mapped[list['MessageReadReceipt']] = relationship('MessageReadReceipt', back_populates='utilisateur')
    questionnaire: Mapped[list['Questionnaire']] = relationship('Questionnaire', back_populates='utilisateur')
    membre: Mapped[list['Membre']] = relationship('Membre', back_populates='utilisateur')
    evaluation_entretien: Mapped[list['EvaluationEntretien']] = relationship('EvaluationEntretien', back_populates='utilisateur')
    evaluation_evaluation: Mapped[list['EvaluationEvaluation']] = relationship('EvaluationEvaluation', back_populates='utilisateur')



class MotDePasseOublie(Base):
    __tablename__ = 'mot_de_passe_oublie'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='mot_de_passe_oublie_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='mdpo_pk'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    token_reinitialisation_mdp: Mapped[str] = mapped_column(String(255), nullable=False)
    date_exp_token_reinitialisation: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))

    #Relation
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='mot_de_passe_oublie')


class Entreprise(Base):
    __tablename__ = 'entreprise'
    __table_args__ = (
        ForeignKeyConstraint(['id_localite'], ['utilitaire.localite.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='entreprise_id_localite_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='entreprise_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='entreprise_pk'),
        UniqueConstraint('id_utilisateur', name='entreprise_id_utilisateur_key'),
        UniqueConstraint('numero_ifu', name='entreprise_constr_numero_ifu'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, comment="description de l'entreprise")
    telephone: Mapped[Optional[str]] = mapped_column(String(20))
    statut_juridique: Mapped[Optional[str]] = mapped_column(String(50), comment='SA, SARL ...')
    adresse: Mapped[Optional[str]] = mapped_column(String(255), comment='peut être une combinaison de departement, commune, arrondissement, quartier de ville ou village, maison')
    numero_ifu: Mapped[Optional[str]] = mapped_column(String(13))
    numero_rccm: Mapped[Optional[str]] = mapped_column(String(50), comment='numéro du régistre de commerce')
    date_creation_entreprise: Mapped[Optional[datetime.date]] = mapped_column(Date)
    nom_responsable_entreprise: Mapped[Optional[str]] = mapped_column(String(50), comment='Directeur général ou tout autre responsable')
    prenoms_responsable_entreprise: Mapped[Optional[str]] = mapped_column(String(255))
    telephone_responsable_entreprise: Mapped[Optional[str]] = mapped_column(String(20))
    logo: Mapped[Optional[str]] = mapped_column(String(255))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    site_web: Mapped[Optional[str]] = mapped_column(String(255), comment="Lien du site web de l'entreprise")
    id_localite: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.localite.id', ondelete='SET NULL'))

    #Relation
    localite: Mapped[Optional['Localite']] = relationship('Localite', back_populates='entreprise')
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='entreprise')
    questionnaire: Mapped[list['Questionnaire']] = relationship('Questionnaire', back_populates='entreprise')
    annexe_entreprise: Mapped[list['AnnexeEntreprise']] = relationship('AnnexeEntreprise', back_populates='entreprise')
    critere_evaluation: Mapped[list['CritereEvaluation']] = relationship('CritereEvaluation', back_populates='entreprise')
    secteurs_activite_entreprise: Mapped[list['SecteursActiviteEntreprise']] = relationship('SecteursActiviteEntreprise', back_populates='entreprise')
    departement_entreprise: Mapped[list['DepartementEntreprise']] = relationship('DepartementEntreprise', back_populates='entreprise')
    poste: Mapped[list['Poste']] = relationship('Poste', back_populates='entreprise')
    offre_emploi: Mapped[list['OffreEmploi']] = relationship('OffreEmploi', back_populates='entreprise')
    entretiens: Mapped[list['Entretiens']] = relationship('Entretiens', back_populates='entreprise')
    evaluations: Mapped[list['Evaluations']] = relationship('Evaluations', back_populates='entreprise')
    
    


class FichiersJoints(Base):
    __tablename__ = 'fichiers_joints'
    __table_args__ = (
        ForeignKeyConstraint(['id_candidature'], ['talent.candidature.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='fichiers_joints_id_candidature_fkey'),
        PrimaryKeyConstraint('id', name='fichiers_joints_pk'),
        {'schema': 'public'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nature_fichier: Mapped[str] = mapped_column(String(200), nullable=False, server_default=text("'CV'::character varying"), comment="CV, Lettre de motivation, Attestation de diplôme, Attestation de travail, Permis de conduite, Carte CIP, Carte d'Identité Nationale, Passport, Acte de naissance....")
    visible_au_recruteur: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    is_importe_via_plateforme_cv: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    nom_fichier: Mapped[Optional[str]] = mapped_column(String(255))
    fichier: Mapped[Optional[str]] = mapped_column(String(255), comment='chemin ou URL vers le fichier')
    type_fichier: Mapped[Optional[str]] = mapped_column(String(100))
    meta_donnees: Mapped[Optional[dict]] = mapped_column(JSONB)
    id_candidature: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.candidature.id', ondelete='SET NULL'))
    contenu_fichier_importe_via_plateforme_cv: Mapped[Optional[dict]] = mapped_column(JSONB, comment="Le contenu du fichier au format JSON.\nSi c'est un CV par exemple, on peut avoir l'id du cv et ses paramètres (modèle utilisé et ses configurations comme couleurs, polices), les informations concernant les formations, expériences, langues, compétences...")

    #Relation
    candidature: Mapped[Optional['Candidature']] = relationship('Candidature', back_populates='fichiers_joints')



#==============================================Schema Abonnement==================================

class PlanAbonnement(Base):
    __tablename__ = 'plan_abonnement'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='plan_abonnement_pk'),
        UniqueConstraint('nom_plan', 'type_utilisateur', name='plan_abonnement_unique'),
        {'comment': "Plans d'abonnement disponibles sur la plateforme",
     'schema': 'abonnement'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom_plan: Mapped[str] = mapped_column(String(100), nullable=False)
    type_utilisateur: Mapped[str] = mapped_column(String(50), nullable=False, comment='Candidat, Entreprise, Recruteur')
    statut: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'Actif'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    prix_mensuel: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    prix_annuel: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    duree_jours_essai: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    limite_offres: Mapped[Optional[int]] = mapped_column(SmallInteger, comment="Nombre maximum d'offres publiées (null = illimité)")
    limite_candidatures: Mapped[Optional[int]] = mapped_column(SmallInteger, comment='Nombre maximum de candidatures reçues/envoyées')
    limite_utilisateurs_entreprise: Mapped[Optional[int]] = mapped_column(SmallInteger, comment="Nombre maximum d'utilisateurs associés à l'entreprise")
    limite_entretiens: Mapped[Optional[int]] = mapped_column(SmallInteger)
    permet_branding_custom: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    permet_api_access: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    permet_export_donnees: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    #Relation
    abonnement_utilisateur: Mapped[list['AbonnementUtilisateur']] = relationship('AbonnementUtilisateur', back_populates='plan_abonnement')


class PromotionCode(Base):
    __tablename__ = 'promotion_code'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='promotion_code_pk'),
        UniqueConstraint('code', name='promotion_code_code_key'),
        Index('idx_promotion_code_code', 'code'),
        {'comment': "Codes promotionnels pour réductions d'abonnements",
     'schema': 'abonnement'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    type_reduction: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'Pourcentage'::character varying"), comment='Pourcentage, Montant fixe')
    valeur_reduction: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    date_debut: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    statut: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'Actif'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    limite_utilisations: Mapped[Optional[int]] = mapped_column(SmallInteger)
    nombre_utilisations_actuelles: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    plans_applicables: Mapped[Optional[str]] = mapped_column(String(255), comment='Noms des plans applicables, séparés par virgule (null = tous)')

    #Relation
    coupon_utilise: Mapped[list['CouponUtilise']] = relationship('CouponUtilise', back_populates='promotion_code')
    
class CouponUtilise(Base):
    __tablename__ = 'coupon_utilise'
    __table_args__ = (
        ForeignKeyConstraint(['id_paiement_abonnement'], ['abonnement.paiement_abonnement.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='coupon_utilise_id_paiement_abonnement_fkey'),
        ForeignKeyConstraint(['id_promotion_code'], ['abonnement.promotion_code.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='coupon_utilise_id_promotion_code_fkey'),
        PrimaryKeyConstraint('id', name='coupon_utilise_pk'),
        {'comment': "Historique d'utilisation des codes promotionnels",
     'schema': 'abonnement'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_promotion_code: Mapped[str] = mapped_column(String(12), ForeignKey('abonnement.promotion_code.id', ondelete='SET NULL'), nullable=False)
    id_paiement_abonnement: Mapped[str] = mapped_column(String(12), ForeignKey('abonnement.paiement_abonnement.id', ondelete='CASCADE'), nullable=False)
    date_utilisation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    reduction_appliquee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))

    #Relation
    paiement_abonnement: Mapped['PaiementAbonnement'] = relationship('PaiementAbonnement', back_populates='coupon_utilise')
    promotion_code: Mapped['PromotionCode'] = relationship('PromotionCode', back_populates='coupon_utilise')



class PaiementAbonnement(Base):
    __tablename__ = 'paiement_abonnement'
    __table_args__ = (
        ForeignKeyConstraint(['id_abonnement_utilisateur'], ['abonnement.abonnement_utilisateur.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='paiement_abonnement_id_abonnement_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='paiement_abonnement_pk'),
        Index('idx_paiement_abonnement_date', 'created_at'),
        Index('idx_paiement_abonnement_statut', 'statut_paiement'),
        {'comment': "Historique des paiements d'abonnements", 'schema': 'abonnement'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_abonnement_utilisateur: Mapped[str] = mapped_column(String(12), ForeignKey('abonnement.abonnement_utilisateur.id', ondelete='CASCADE'), nullable=False)
    montant: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    devise: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'XOF'::character varying"))
    statut_paiement: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'En attente'::character varying"), comment='En attente, Confirmé, Échoué, Remboursé')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    methode_paiement: Mapped[Optional[str]] = mapped_column(String(50), comment='Carte bancaire, Virement, PayPal, Momo, Autre')
    reference_paiement: Mapped[Optional[str]] = mapped_column(String(255))
    date_paiement: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_prochaine_facturation: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    description_paiement: Mapped[Optional[str]] = mapped_column(Text)
    recu_url: Mapped[Optional[str]] = mapped_column(String(255), comment='Lien vers le reçu ou facture PDF')

    #Relation
    abonnement_utilisateur: Mapped['AbonnementUtilisateur'] = relationship('AbonnementUtilisateur', back_populates='paiement_abonnement')
    coupon_utilise: Mapped[list['CouponUtilise']] = relationship('CouponUtilise', back_populates='paiement_abonnement')
    facture_abonnement: Mapped[list['FactureAbonnement']] = relationship('FactureAbonnement', back_populates='paiement_abonnement')

class FactureAbonnement(Base):
    __tablename__ = 'facture_abonnement'
    __table_args__ = (
        ForeignKeyConstraint(['id_abonnement_utilisateur'], ['abonnement.abonnement_utilisateur.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='facture_abonnement_id_abonnement_utilisateur_fkey'),
        ForeignKeyConstraint(['id_paiement_abonnement'], ['abonnement.paiement_abonnement.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='facture_abonnement_id_paiement_abonnement_fkey'),
        PrimaryKeyConstraint('id', name='facture_abonnement_pk'),
        UniqueConstraint('numero_facture', name='facture_abonnement_numero_facture_key'),
        Index('idx_facture_abonnement_numero', 'numero_facture'),
        Index('idx_facture_abonnement_statut', 'statut_facture'),
        {'comment': 'Factures générées pour les abonnements', 'schema': 'abonnement'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    numero_facture: Mapped[str] = mapped_column(String(50), nullable=False)
    id_abonnement_utilisateur: Mapped[str] = mapped_column(String(12), ForeignKey('abonnement.abonnement_utilisateur.id', ondelete='CASCADE'), nullable=False)
    date_emission: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    montant_ttc: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    statut_facture: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'Émise'::character varying"), comment='Émise, Envoyée, Payée, Partielle, Annulée, Incident')
    id_paiement_abonnement: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('abonnement.paiement_abonnement.id', ondelete='SET NULL'))
    date_echeance: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    montant_ht: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    montant_tva: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    notes_facture: Mapped[Optional[str]] = mapped_column(Text)
    fichier_url: Mapped[Optional[str]] = mapped_column(String(255))

    #Relation
    abonnement_utilisateur: Mapped['AbonnementUtilisateur'] = relationship('AbonnementUtilisateur', back_populates='facture_abonnement')
    paiement_abonnement: Mapped[Optional['PaiementAbonnement']] = relationship('PaiementAbonnement', back_populates='facture_abonnement')

class AbonnementUtilisateur(Base):
    __tablename__ = 'abonnement_utilisateur'
    __table_args__ = (
        ForeignKeyConstraint(['id_plan_abonnement'], ['abonnement.plan_abonnement.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='abonnement_utilisateur_id_plan_abonnement_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='abonnement_utilisateur_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='abonnement_utilisateur_pk'),
        Index('idx_abonnement_utilisateur_datedebut', 'date_debut'),
        Index('idx_abonnement_utilisateur_datefin', 'date_fin'),
        Index('idx_abonnement_utilisateur_statut', 'statut'),
        {'comment': 'Abonnements actifs de chaque utilisateur à un plan',
     'schema': 'abonnement'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    id_plan_abonnement: Mapped[str] = mapped_column(String(12), ForeignKey('abonnement.plan_abonnement.id', ondelete='SET NULL'), nullable=False)
    date_debut: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    est_essai: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment="Indique si c'est une période d'essai gratuite")
    statut: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'Actif'::character varying"), comment='Actif, En attente, Suspendu, Annulé, Expiré')
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_debut_essai: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_fin_essai: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_derniere_facture: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    mode_renouvellement: Mapped[Optional[str]] = mapped_column(String(50), comment='Manuel, Automatique, À la demande')

    #Relation
    plan_abonnement: Mapped['PlanAbonnement'] = relationship('PlanAbonnement', back_populates='abonnement_utilisateur')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='abonnement_utilisateur')
    paiement_abonnement: Mapped[list['PaiementAbonnement']] = relationship('PaiementAbonnement', back_populates='abonnement_utilisateur')
    facture_abonnement: Mapped[list['FactureAbonnement']] = relationship('FactureAbonnement', back_populates='abonnement_utilisateur')



#==============================================schemas Academy=====================================

class DomaineFormation(Base):
    __tablename__ = 'domaine_formation'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='domaine_formation_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    formation: Mapped[list['Formation']] = relationship('Formation', back_populates='domaine_formation')

class Formateur(Base):
    __tablename__ = 'formateur'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', name='formateur_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='formateur_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    denomination: Mapped[str] = mapped_column(String(150), nullable=False, comment="Nom du centre/atélier de formation ou dénomination qu'un formateur veut donner à son espace de formation ou simplement nom du formateur")
    is_entreprise: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment="Si c'est une entreprise offrant des formations ou un simple utilisateur formateur")
    image_profil: Mapped[str] = mapped_column(String(255), nullable=False, comment='Photo de profil ou le logo du formateur (entreprise ou personne physique)')
    description: Mapped[Optional[str]] = mapped_column(Text, comment="Description ou aperçu sur l'espace de formation")
    image_couverture: Mapped[Optional[str]] = mapped_column(String(255), comment="Image de couverture ou affiche de l'espace de formation")
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))

    #Relation
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='formateur')
    formation: Mapped[list['Formation']] = relationship('Formation', back_populates='formateur')


class Formation(Base):
    __tablename__ = 'formation'
    __table_args__ = (
        ForeignKeyConstraint(['id_domaine_formation'], ['academy.domaine_formation.id'], ondelete='SET NULL', onupdate='CASCADE', name='formation_id_domaine_formation_fkey'),
        ForeignKeyConstraint(['id_formateur'], ['academy.formateur.id'], ondelete='SET NULL', onupdate='CASCADE', name='formation_id_formateur_fkey'),
        PrimaryKeyConstraint('id', name='formation_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    titre: Mapped[str] = mapped_column(String(150), nullable=False)
    prix: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default=text('0.0'))
    mode: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'En ligne'::character varying"), comment="in ('En ligne', 'Présentiel', 'Mixte')")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    duree: Mapped[Optional[str]] = mapped_column(String(20), server_default=text('NULL::character varying'), comment='Si date_debut et date_fin ne sont pas bien definies. "2 mois", "3 semaines".')
    id_formateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.formateuur.id', ondelete='SET NULL'))
    id_domaine_formation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.domaine_formation.id', ondelete='SET NULL'))
    lieu_formation: Mapped[Optional[str]] = mapped_column(String(100))
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="Chemin de l'image d'affiche de la formation")
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    fichiers_joints: Mapped[Optional[dict]] = mapped_column(JSONB, comment='Une formation peut avoir certains fichiers joints')

    #Relation
    domaine_formation: Mapped[Optional['DomaineFormation']] = relationship('DomaineFormation', back_populates='formation')
    formateur: Mapped[Optional['Formateur']] = relationship('Formateur', back_populates='formation')
    avis: Mapped[list['Avis']] = relationship('Avis', back_populates='formation')
    inscription_formation: Mapped[list['InscriptionFormation']] = relationship('InscriptionFormation', back_populates='formation')
    module_cours: Mapped[list['ModuleCours']] = relationship('ModuleCours', back_populates='formation')
    evaluation: Mapped[list['Evaluation']] = relationship('Evaluation', back_populates='formation')

class Avis(Base):
    __tablename__ = 'avis'
    __table_args__ = (
        ForeignKeyConstraint(['id_commentateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', name='avis_id_commentateur_fkey'),
        ForeignKeyConstraint(['id_formation'], ['academy.formation.id'], ondelete='SET NULL', onupdate='CASCADE', name='avis_id_formation_fkey'),
        PrimaryKeyConstraint('id', name='avis_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    is_verifie: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment="comentaire vérifié provenant d'un utilisateur ayant fait la formation commentée")
    id_commentateur: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'), nullable=False, comment="Id de l'utilisateur ayant commenté")
    commentaire: Mapped[Optional[str]] = mapped_column(Text)
    note: Mapped[Optional[int]] = mapped_column(SmallInteger, comment='in (1,2,3,4,5)')
    nom_commentataire: Mapped[Optional[str]] = mapped_column(String(150))
    id_formation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.formation.id', ondelete='SET NULL'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='avis')
    formation: Mapped[Optional['Formation']] = relationship('Formation', back_populates='avis')

class InscriptionFormation(Base):
    __tablename__ = 'inscription_formation'
    __table_args__ = (
        ForeignKeyConstraint(['id_formation'], ['academy.formation.id'], ondelete='SET NULL', onupdate='CASCADE', name='inscription_formation_id_formation_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', name='inscription_formation_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='inscription_formation_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    date_inscription: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    statut: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'Inscrit'::character varying"), comment="in ('Inscrit', 'En cours', 'Terminé')")
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    type_paiement: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Paiement en bloc'::character varying"), comment="in ('Paiement en bloc', 'Paiement echelonné')")
    montant_paye: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default=text('0'))
    moyen_paiement: Mapped[Optional[str]] = mapped_column(String(50), comment="in ('Mobile Money', 'Espèces', 'Virement bancaire', 'Carte bancaire', 'Paypal')")
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))
    id_formation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.formation.id', ondelete='SET NULL'))

    #Relation
    formation: Mapped[Optional['Formation']] = relationship('Formation', back_populates='inscription_formation')
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='inscription_formation')
    suivi_module_cours: Mapped[list['SuiviModuleCours']] = relationship('SuiviModuleCours', back_populates='inscription_formation')
    reponse_evaluation: Mapped[list['ReponseEvaluation']] = relationship('ReponseEvaluation', back_populates='inscription_formation')


class ModuleCours(Base):
    __tablename__ = 'module_cours'
    __table_args__ = (
        ForeignKeyConstraint(['id_formation'], ['academy.formation.id'], ondelete='SET NULL', onupdate='CASCADE', name='module_cours_id_formation_fkey'),
        PrimaryKeyConstraint('id', name='module_cours_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    titre: Mapped[str] = mapped_column(String(150), nullable=False)
    ordre_de_sequence: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default=text('0'), comment='Ordre de deroulement des modules de la formation. 0 par défaut')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    id_module_cours: Mapped[Optional[str]] = mapped_column(String(12), comment='Si NULL, il s\'agit d\'un module sinon d\'un cours dans le module d\'id "id_module_cours"')
    description: Mapped[Optional[str]] = mapped_column(Text)
    duree: Mapped[Optional[datetime.time]] = mapped_column(Time)
    contenu_texte: Mapped[Optional[str]] = mapped_column(Text)
    contenu_fichier: Mapped[Optional[str]] = mapped_column(String(255))
    id_formation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.formation.id', ondelete='SET NULL'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    #Relation
    formation: Mapped[Optional['Formation']] = relationship('Formation', back_populates='module_cours')
    evaluation: Mapped[list['Evaluation']] = relationship('Evaluation', back_populates='module_cours')
    suivi_module_cours: Mapped[list['SuiviModuleCours']] = relationship('SuiviModuleCours', back_populates='module_cours')


class Evaluation(Base):
    __tablename__ = 'evaluation'
    __table_args__ = (
        ForeignKeyConstraint(['id_formation'], ['academy.formation.id'], ondelete='SET NULL', onupdate='CASCADE', name='evaluation_id_formation_fkey'),
        ForeignKeyConstraint(['id_module_cours'], ['academy.module_cours.id'], ondelete='SET NULL', onupdate='CASCADE', name='evaluation_id_module_cours_fkey'),
        PrimaryKeyConstraint('id', name='evaluation_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_questionnaire: Mapped[str] = mapped_column(String(12), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    autres: Mapped[Optional[dict]] = mapped_column(JSONB, comment='Toutes les informations possibles concernant une évaluation')
    id_formation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.formation.id', ondelete='SET NULL'))
    id_module_cours: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.module_cours.id', ondelete='SET NULL'))

    #Relation
    formation: Mapped[Optional['Formation']] = relationship('Formation', back_populates='evaluation')
    module_cours: Mapped[Optional['ModuleCours']] = relationship('ModuleCours', back_populates='evaluation')
    reponse_evaluation: Mapped[list['ReponseEvaluation']] = relationship('ReponseEvaluation', back_populates='evaluation')


class SuiviModuleCours(Base):
    __tablename__ = 'suivi_module_cours'
    __table_args__ = (
        ForeignKeyConstraint(['id_inscription_formation'], ['academy.inscription_formation.id'], ondelete='SET NULL', onupdate='CASCADE', name='suivi_module_cours_id_inscription_formation_fkey'),
        ForeignKeyConstraint(['id_module_cours'], ['academy.module_cours.id'], ondelete='SET NULL', onupdate='CASCADE', name='suivi_module_cours_id_module_cours_fkey'),
        PrimaryKeyConstraint('id', name='suivi_module_cours_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    statut: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'Non-demarré'::character varying"), comment='Restreint, Non-demarré, En cours, Terminé')
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'), comment='Date à laquelle on a le status actuel')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    autres: Mapped[Optional[dict]] = mapped_column(JSONB)
    id_inscription_formation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.inscription_formation.id', ondelete='SET NULL'))
    id_module_cours: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.module_cours.id', ondelete='SET NULL'))

    #Relation
    inscription_formation: Mapped[Optional['InscriptionFormation']] = relationship('InscriptionFormation', back_populates='suivi_module_cours')
    module_cours: Mapped[Optional['ModuleCours']] = relationship('ModuleCours', back_populates='suivi_module_cours')

class ReponseEvaluation(Base):
    __tablename__ = 'reponse_evaluation'
    __table_args__ = (
        ForeignKeyConstraint(['id_evaluation'], ['academy.evaluation.id'], ondelete='SET NULL', onupdate='CASCADE', name='reponse_evaluation_id_evaluation_fkey'),
        ForeignKeyConstraint(['id_inscription_formation'], ['academy.inscription_formation.id'], ondelete='SET NULL', onupdate='CASCADE', name='reponse_evaluation_id_inscription_formation_fkey'),
        PrimaryKeyConstraint('id', name='reponse_evaluation_pkey'),
        {'schema': 'academy'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_reponse_questionnaire: Mapped[str] = mapped_column(String(12), nullable=False, comment='id dans la table reponse_questionnaire du schema survey (de questionnaire)')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    note: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2))
    id_inscription_formation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.inscription_formation.id', ondelete='SET NULL'))
    id_evaluation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('academy.evaluation.id', ondelete='SET NULL'))

    #Relation
    evaluation: Mapped[Optional['Evaluation']] = relationship('Evaluation', back_populates='reponse_evaluation')
    inscription_formation: Mapped[Optional['InscriptionFormation']] = relationship('InscriptionFormation', back_populates='reponse_evaluation')


#==============================================Schemas Cv========================================

class TemplateCv(Base):
    __tablename__ = 'template_cv'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='template_cv_pk'),
        Index('idx_template_cv_actif', 'actif'),
        Index('idx_template_cv_nom', 'nom'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    contenu_html: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    actif: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    
    #Relation
    cv: Mapped[list['Cv']] = relationship('Cv', back_populates='template_cv')


class ActiviteSocComCv(Base):
    __tablename__ = 'activite_soc_com_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='activite_soc_com_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='activite_soc_com_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    organisme: Mapped[str] = mapped_column(String(100), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    duree_consacre: Mapped[Optional[str]] = mapped_column(String(10))
    lien_att_ou_certif: Mapped[Optional[str]] = mapped_column(String(255))
    fichier_url: Mapped[Optional[str]] = mapped_column(String(255))
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='activite_soc_com_cv')
    cv_activite_soc_com_assoc: Mapped[list['CvActiviteSocComAssoc']] = relationship('CvActiviteSocComAssoc', back_populates='activite_soc_com_cv')


class AtoutCv(Base):
    __tablename__ = 'atout_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='atout_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='atout_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    organisme: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    duree_consacre: Mapped[Optional[str]] = mapped_column(String(10))
    lien_att_ou_certif: Mapped[Optional[str]] = mapped_column(String(255))
    fichier_url: Mapped[Optional[str]] = mapped_column(String(255))
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='atout_cv')
    cv_atout_assoc: Mapped[list['CvAtoutAssoc']] = relationship('CvAtoutAssoc', back_populates='atout_cv')


class AutreCv(Base):
    __tablename__ = 'autre_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='autre_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='autre_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    organisme: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    duree_consacre: Mapped[Optional[str]] = mapped_column(String(10))
    lien_att_ou_certif: Mapped[Optional[str]] = mapped_column(String(255))
    fichier_url: Mapped[Optional[str]] = mapped_column(String(255))
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='autre_cv')
    cv_autre_assoc: Mapped[list['CvAutreAssoc']] = relationship('CvAutreAssoc', back_populates='autre_cv')


class CentreInteretCv(Base):
    __tablename__ = 'centre_interet_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='centre_interet_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='centre_interet_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    libelle: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Football'::character varying"))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    duree_consacree: Mapped[Optional[str]] = mapped_column(String(10))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='centre_interet_cv')
    cv_centre_interet_assoc: Mapped[list['CvCentreInteretAssoc']] = relationship('CvCentreInteretAssoc', back_populates='centre_interet_cv')


class CertificatCv(Base):
    __tablename__ = 'certificat_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='certificat_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='certificat_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)
    organisme: Mapped[str] = mapped_column(String(100), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    duree_consacre: Mapped[Optional[str]] = mapped_column(String(10))
    lien_att_ou_certif: Mapped[Optional[str]] = mapped_column(String(255))
    fichier_url: Mapped[Optional[str]] = mapped_column(String(255))
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='certificat_cv')
    cv_certificat_assoc: Mapped[list['CvCertificatAssoc']] = relationship('CvCertificatAssoc', back_populates='certificat_cv')


class ExperienceCv(Base):
    __tablename__ = 'experience_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='experience_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='experience_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    type_experience: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Stage_academique'::character varying"))
    titre_du_poste: Mapped[str] = mapped_column(String(255), nullable=False)
    structure: Mapped[str] = mapped_column(String(255), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    lien_att_ou_certif: Mapped[Optional[str]] = mapped_column(String(255))
    fichier_url: Mapped[Optional[str]] = mapped_column(String(255))
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    en_cours: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='experience_cv')
    cv_experience_assoc: Mapped[list['CvExperienceAssoc']] = relationship('CvExperienceAssoc', back_populates='experience_cv')


class FormationCv(Base):
    __tablename__ = 'formation_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='formation_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='formation_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    niveau: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'BAC D'::character varying"))
    filiere_ou_domaine: Mapped[str] = mapped_column(String(255), nullable=False)
    ecole_ou_institut: Mapped[str] = mapped_column(String(255), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    lien_att_ou_certif: Mapped[Optional[str]] = mapped_column(String(255))
    fichier_url: Mapped[Optional[str]] = mapped_column(String(255))
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    en_cours: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    niveau_cec: Mapped[Optional[str]] = mapped_column(String(12))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='formation_cv')
    cv_formation_assoc: Mapped[list['CvFormationAssoc']] = relationship('CvFormationAssoc', back_populates='formation_cv')


class ReferenceCv(Base):
    __tablename__ = 'reference_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='reference_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='reference_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(20), nullable=False)
    prenoms: Mapped[str] = mapped_column(String(100), nullable=False)
    poste_position: Mapped[str] = mapped_column(String(100), nullable=False)
    organisme: Mapped[str] = mapped_column(String(100), nullable=False)
    mail: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    description: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='reference_cv')
    cv_reference_assoc: Mapped[list['CvReferenceAssoc']] = relationship('CvReferenceAssoc', back_populates='reference_cv')


class ReseauSocCv(Base):
    __tablename__ = 'reseau_soc_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='reseau_soc_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='reseau_soc_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom_reseau_social: Mapped[str] = mapped_column(String(100), nullable=False)
    lien_profil: Mapped[str] = mapped_column(String(255), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='reseau_soc_cv')
    cv_reseau_soc_assoc: Mapped[list['CvReseauSocAssoc']] = relationship('CvReseauSocAssoc', back_populates='reseau_soc_cv')


class ResumeCv(Base):
    __tablename__ = 'resume_cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='resume_cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='resume_cv_pk'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    contenu: Mapped[str] = mapped_column(Text, nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='resume_cv')
    cv: Mapped[list['Cv']] = relationship('Cv', back_populates='resume_cv')


class Cv(Base):
    __tablename__ = 'cv'
    __table_args__ = (
        ForeignKeyConstraint(['id_resume_cv'], ['cv.resume_cv.id'], ondelete='SET NULL', name='cv_id_resume_cv_fkey'),
        ForeignKeyConstraint(['id_template_cv'], ['cv.template_cv.id'], ondelete='SET NULL', name='cv_id_template_cv_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', name='cv_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='cv_pk'),
        Index('idx_cv_id_resume_cv', 'id_resume_cv'),
        Index('idx_cv_id_template_cv', 'id_template_cv'),
        Index('idx_cv_id_utilisateur', 'id_utilisateur'),
        {'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    id_resume_cv: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('cv.resume_cv.id', ondelete='SET NULL'))
    id_template_cv: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('cv.template_cv.id', ondelete='SET NULL'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    #Relation
    resume_cv: Mapped[Optional['ResumeCv']] = relationship('ResumeCv', back_populates='cv')
    template_cv: Mapped[Optional['TemplateCv']] = relationship('TemplateCv', back_populates='cv')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='cv')
    cv_activite_soc_com_assoc: Mapped[list['CvActiviteSocComAssoc']] = relationship('CvActiviteSocComAssoc', back_populates='cv')
    cv_atout_assoc: Mapped[list['CvAtoutAssoc']] = relationship('CvAtoutAssoc', back_populates='cv')
    cv_autre_assoc: Mapped[list['CvAutreAssoc']] = relationship('CvAutreAssoc', back_populates='cv')
    cv_centre_interet_assoc: Mapped[list['CvCentreInteretAssoc']] = relationship('CvCentreInteretAssoc', back_populates='cv')
    cv_certificat_assoc: Mapped[list['CvCertificatAssoc']] = relationship('CvCertificatAssoc', back_populates='cv')
    cv_experience_assoc: Mapped[list['CvExperienceAssoc']] = relationship('CvExperienceAssoc', back_populates='cv')
    cv_formation_assoc: Mapped[list['CvFormationAssoc']] = relationship('CvFormationAssoc', back_populates='cv')
    cv_reference_assoc: Mapped[list['CvReferenceAssoc']] = relationship('CvReferenceAssoc', back_populates='cv')
    cv_reseau_soc_assoc: Mapped[list['CvReseauSocAssoc']] = relationship('CvReseauSocAssoc', back_populates='cv')
    cv_competence_assoc: Mapped[list['CvCompetenceAssoc']] = relationship('CvCompetenceAssoc', back_populates='cv')


class CandidatCompetence(Base):
    __tablename__ = 'candidat_competence'
    __table_args__ = (
        ForeignKeyConstraint(['id_candidat'], ['talent.candidat.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='candidat_competence_id_candidat_fkey'),
        ForeignKeyConstraint(['id_competence'], ['utilitaire.competence.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='candidat_competence_id_competence_fkey'),
        PrimaryKeyConstraint('id', name='candidat_competence_pk'),
        UniqueConstraint('id_candidat', 'id_competence', name='candidat_competence_unique'),
        {'comment': 'Compétences maîtrisées par un candidat avec niveau et expérience',
     'schema': 'cv'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_candidat: Mapped[str] = mapped_column(String(12), ForeignKey('talent.candidat.id', ondelete='CASCADE'), nullable=False)
    id_competence: Mapped[str] = mapped_column(String(12), ForeignKey('utilitaire.competence.id', ondelete='CASCADE'), nullable=False)
    niveau_maitrise: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Intermédiaire'::character varying"), comment='Débutant, Intermédiaire, Avancé, Expert')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    annees_experience: Mapped[Optional[int]] = mapped_column(SmallInteger)
    description_experience: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    candidat: Mapped['Candidat'] = relationship('Candidat', back_populates='candidat_competence')
    competence: Mapped['Competence'] = relationship('Competence', back_populates='candidat_competence')
    cv_competence_assoc: Mapped[list['CvCompetenceAssoc']] = relationship('CvCompetenceAssoc', back_populates='candidat_competence')


class CvActiviteSocComAssoc(Base):
    __tablename__ = 'cv_activite_soc_com_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_activite_soc_com_cv'], ['cv.activite_soc_com_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_activite_soc_com_assoc_id_activite_soc_com_cv_fkey'),
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_activite_soc_com_assoc_id_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_activite_soc_com_cv', name='cv_activite_soc_com_assoc_pkey'),
        Index('idx_cv_activite_soc_com_assoc_id_activite_soc_com_cv', 'id_activite_soc_com_cv'),
        Index('idx_cv_activite_soc_com_assoc_id_cv', 'id_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_activite_soc_com_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    activite_soc_com_cv: Mapped['ActiviteSocComCv'] = relationship('ActiviteSocComCv', back_populates='cv_activite_soc_com_assoc')
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_activite_soc_com_assoc')


class CvAtoutAssoc(Base):
    __tablename__ = 'cv_atout_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_atout_cv'], ['cv.atout_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_atout_assoc_id_atout_cv_fkey'),
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_atout_assoc_id_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_atout_cv', name='cv_atout_assoc_pkey'),
        Index('idx_cv_atout_assoc_id_atout_cv', 'id_atout_cv'),
        Index('idx_cv_atout_assoc_id_cv', 'id_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_atout_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    atout_cv: Mapped['AtoutCv'] = relationship('AtoutCv', back_populates='cv_atout_assoc')
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_atout_assoc')


class CvAutreAssoc(Base):
    __tablename__ = 'cv_autre_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_autre_cv'], ['cv.autre_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_autre_assoc_id_autre_cv_fkey'),
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_autre_assoc_id_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_autre_cv', name='cv_autre_assoc_pkey'),
        Index('idx_cv_autre_assoc_id_autre_cv', 'id_autre_cv'),
        Index('idx_cv_autre_assoc_id_cv', 'id_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_autre_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    autre_cv: Mapped['AutreCv'] = relationship('AutreCv', back_populates='cv_autre_assoc')
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_autre_assoc')


class CvCentreInteretAssoc(Base):
    __tablename__ = 'cv_centre_interet_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_centre_interet_cv'], ['cv.centre_interet_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_centre_interet_assoc_id_centre_interet_cv_fkey'),
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_centre_interet_assoc_id_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_centre_interet_cv', name='cv_centre_interet_assoc_pkey'),
        Index('idx_cv_centre_interet_assoc_id_centre_interet_cv', 'id_centre_interet_cv'),
        Index('idx_cv_centre_interet_assoc_id_cv', 'id_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_centre_interet_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    centre_interet_cv: Mapped['CentreInteretCv'] = relationship('CentreInteretCv', back_populates='cv_centre_interet_assoc')
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_centre_interet_assoc')


class CvCertificatAssoc(Base):
    __tablename__ = 'cv_certificat_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_certificat_cv'], ['cv.certificat_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_certificat_assoc_id_certificat_cv_fkey'),
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_certificat_assoc_id_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_certificat_cv', name='cv_certificat_assoc_pkey'),
        Index('idx_cv_certificat_assoc_id_certificat_cv', 'id_certificat_cv'),
        Index('idx_cv_certificat_assoc_id_cv', 'id_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_certificat_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    certificat_cv: Mapped['CertificatCv'] = relationship('CertificatCv', back_populates='cv_certificat_assoc')
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_certificat_assoc')


class CvExperienceAssoc(Base):
    __tablename__ = 'cv_experience_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_experience_assoc_id_cv_fkey'),
        ForeignKeyConstraint(['id_experience_cv'], ['cv.experience_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_experience_assoc_id_experience_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_experience_cv', name='cv_experience_assoc_pkey'),
        Index('idx_cv_experience_assoc_id_cv', 'id_cv'),
        Index('idx_cv_experience_assoc_id_experience_cv', 'id_experience_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_experience_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_experience_assoc')
    experience_cv: Mapped['ExperienceCv'] = relationship('ExperienceCv', back_populates='cv_experience_assoc')


class CvFormationAssoc(Base):
    __tablename__ = 'cv_formation_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_formation_assoc_id_cv_fkey'),
        ForeignKeyConstraint(['id_formation_cv'], ['cv.formation_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_formation_assoc_id_formation_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_formation_cv', name='cv_formation_assoc_pkey'),
        Index('idx_cv_formation_assoc_id_cv', 'id_cv'),
        Index('idx_cv_formation_assoc_id_formation_cv', 'id_formation_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_formation_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_formation_assoc')
    formation_cv: Mapped['FormationCv'] = relationship('FormationCv', back_populates='cv_formation_assoc')


class CvReferenceAssoc(Base):
    __tablename__ = 'cv_reference_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_reference_assoc_id_cv_fkey'),
        ForeignKeyConstraint(['id_reference_cv'], ['cv.reference_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_reference_assoc_id_reference_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_reference_cv', name='cv_reference_assoc_pkey'),
        Index('idx_cv_reference_assoc_id_cv', 'id_cv'),
        Index('idx_cv_reference_assoc_id_reference_cv', 'id_reference_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_reference_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_reference_assoc')
    reference_cv: Mapped['ReferenceCv'] = relationship('ReferenceCv', back_populates='cv_reference_assoc')


class CvReseauSocAssoc(Base):
    __tablename__ = 'cv_reseau_soc_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_reseau_soc_assoc_id_cv_fkey'),
        ForeignKeyConstraint(['id_reseau_soc_cv'], ['cv.reseau_soc_cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_reseau_soc_assoc_id_reseau_soc_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_reseau_soc_cv', name='cv_reseau_soc_assoc_pkey'),
        Index('idx_cv_reseau_soc_assoc_id_cv', 'id_cv'),
        Index('idx_cv_reseau_soc_assoc_id_reseau_soc_cv', 'id_reseau_soc_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_reseau_soc_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_reseau_soc_assoc')
    reseau_soc_cv: Mapped['ReseauSocCv'] = relationship('ReseauSocCv', back_populates='cv_reseau_soc_assoc')


class CvCompetenceAssoc(Base):
    __tablename__ = 'cv_competence_assoc'
    __table_args__ = (
        ForeignKeyConstraint(['id_competence'], ['cv.candidat_competence.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_competence_assoc_id_competence_fkey'),
        ForeignKeyConstraint(['id_cv'], ['cv.cv.id'], ondelete='CASCADE', onupdate='CASCADE', name='cv_competence_assoc_id_cv_fkey'),
        PrimaryKeyConstraint('id_cv', 'id_competence', name='cv_competence_assoc_pkey'),
        Index('idx_cv_competence_assoc_id_competence', 'id_competence'),
        Index('idx_cv_competence_assoc_id_cv', 'id_cv'),
        {'schema': 'cv'}
    )

    id_cv: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_competence: Mapped[str] = mapped_column(String(12), primary_key=True)
    ordre: Mapped[Optional[int]] = mapped_column(SmallInteger)

    #Relation
    candidat_competence: Mapped['CandidatCompetence'] = relationship('CandidatCompetence', back_populates='cv_competence_assoc')
    cv: Mapped['Cv'] = relationship('Cv', back_populates='cv_competence_assoc')



#========================================Schemas Planer==============================================

class AuditLogs(Base):
    __tablename__ = 'audit_logs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='audit_logs_pkey'),
        Index('idx_audit_logs_action', 'action'),
        Index('idx_audit_logs_espace', 'espace_id'),
        Index('idx_audit_logs_resource', 'resource_type', 'resource_id'),
        Index('idx_audit_logs_timestamp', 'timestamp'),
        Index('idx_audit_logs_user', 'user_id'),
        Index('idx_audit_logs_workspace', 'workspace_id'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'SUCCESS'::character varying"))
    user_id: Mapped[Optional[str]] = mapped_column(String(255))
    user_name: Mapped[Optional[str]] = mapped_column(String(255))
    user_email: Mapped[Optional[str]] = mapped_column(String(255))
    resource_id: Mapped[Optional[str]] = mapped_column(String(255))
    resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    workspace_id: Mapped[Optional[str]] = mapped_column(String(255))
    espace_id: Mapped[Optional[str]] = mapped_column(String(255))
    ip_address: Mapped[Optional[str]] = mapped_column(String(100))
    details: Mapped[Optional[str]] = mapped_column(Text)


class Workspace(Base):
    __tablename__ = 'workspace'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', name='workspace_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='workspace_pkey'),
        Index('idx_workspace_utilisateur', 'id_utilisateur'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))

    #Relation
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='workspace')
    espace: Mapped[list['Espace']] = relationship('Espace', back_populates='workspace')
    liste: Mapped[list['Liste']] = relationship('Liste', back_populates='workspace')
    membre: Mapped[list['Membre']] = relationship('Membre', back_populates='workspace')


class Espace(Base):
    __tablename__ = 'espace'
    __table_args__ = (
        ForeignKeyConstraint(['id_espace_parent'], ['planer.espace.id'], ondelete='SET NULL', name='espace_id_espace_parent_fkey'),
        ForeignKeyConstraint(['id_workspace'], ['planer.workspace.id'], ondelete='SET NULL', name='espace_id_workspace_fkey'),
        PrimaryKeyConstraint('id', name='espace_pkey'),
        Index('idx_espace_parent', 'id_espace_parent'),
        Index('idx_espace_workspace', 'id_workspace'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    id_espace_parent: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.espace.id', ondelete='SET NULL'))
    id_workspace: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.workspace.id', ondelete='SET NULL'))

    #Relation
    espace: Mapped[Optional['Espace']] = relationship('Espace', remote_side=[id], back_populates='espace_reverse')
    espace_reverse: Mapped[list['Espace']] = relationship('Espace', remote_side=[id_espace_parent], back_populates='espace')
    workspace: Mapped[Optional['Workspace']] = relationship('Workspace', back_populates='espace')
    liste: Mapped[list['Liste']] = relationship('Liste', back_populates='espace')
    membre: Mapped[list['Membre']] = relationship('Membre', back_populates='espace')

class Liste(Base):
    __tablename__ = 'liste'
    __table_args__ = (
        ForeignKeyConstraint(['id_espace'], ['planer.espace.id'], ondelete='SET NULL', name='liste_id_espace_fkey'),
        ForeignKeyConstraint(['id_workspace'], ['planer.workspace.id'], ondelete='SET NULL', name='liste_id_workspace_fkey'),
        PrimaryKeyConstraint('id', name='liste_pkey'),
        Index('idx_liste_espace', 'id_espace'),
        Index('idx_liste_workspace', 'id_workspace'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    id_espace: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.espace.id', ondelete='SET NULL'))
    id_workspace: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.workspace.id', ondelete='SET NULL'))

    #Relation
    espace: Mapped[Optional['Espace']] = relationship('Espace', back_populates='liste')
    workspace: Mapped[Optional['Workspace']] = relationship('Workspace', back_populates='liste')
    canevas: Mapped[Optional['Canevas']] = relationship('Canevas', uselist=False, back_populates='liste')
    tache: Mapped[list['Tache']] = relationship('Tache', back_populates='liste')
    membre: Mapped[list['Membre']] = relationship('Membre', back_populates='liste')


class Canevas(Base):
    __tablename__ = 'canevas'
    __table_args__ = (
        ForeignKeyConstraint(['id_liste'], ['planer.liste.id'], ondelete='SET NULL', name='canevas_id_liste_fkey'),
        PrimaryKeyConstraint('id', name='canevas_pkey'),
        UniqueConstraint('id_liste', name='canevas_id_liste_key'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    is_verrouille: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_liste: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.liste.id', ondelete='SET NULL'))

    #Relation
    liste: Mapped[Optional['Liste']] = relationship('Liste', back_populates='canevas')
    section: Mapped[list['Section']] = relationship('Section', back_populates='canevas')


class Tache(Base):
    __tablename__ = 'tache'
    __table_args__ = (
        ForeignKeyConstraint(['id_liste'], ['planer.liste.id'], ondelete='SET NULL', name='tache_id_liste_fkey'),
        ForeignKeyConstraint(['id_tache_parent'], ['planer.tache.id'], ondelete='CASCADE', name='tache_id_tache_parent_fkey'),
        PrimaryKeyConstraint('id', name='tache_pkey'),
        Index('idx_tache_date_fin_prevue', 'date_fin_prevue'),
        Index('idx_tache_liste', 'id_liste'),
        Index('idx_tache_parent', 'id_tache_parent'),
        Index('idx_tache_priorite', 'priorite'),
        Index('idx_tache_statut', 'statut'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    statut: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'En Attente'::character varying"))
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    date_fin_prevue: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    priorite: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'Normale'::character varying"))
    ordre_affichage: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    id_liste: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.liste.id', ondelete='SET NULL'))
    id_tache_parent: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.tache.id', ondelete='SET NULL'))

    #Relation
    liste: Mapped[Optional['Liste']] = relationship('Liste', back_populates='tache')
    tache: Mapped[Optional['Tache']] = relationship('Tache', remote_side=[id], back_populates='tache_reverse')
    tache_reverse: Mapped[list['Tache']] = relationship('Tache', remote_side=[id_tache_parent], back_populates='tache')
    membre: Mapped[list['Membre']] = relationship('Membre', back_populates='tache')
    checklist: Mapped[list['Checklist']] = relationship('Checklist', back_populates='tache')


class Membre(Base):
    __tablename__ = 'membre'
    __table_args__ = (
        CheckConstraint('num_nonnulls(id_workspace, id_espace, id_liste, id_tache) = 1', name='membre_cible_unique_check'),
        CheckConstraint("role::text = ANY (ARRAY['Créateur'::character varying, 'Administrateur'::character varying, 'Membre'::character varying, 'Invité'::character varying]::text[])", name='membre_role_check'),
        CheckConstraint("statut::text = ANY (ARRAY['Actif'::character varying, 'En attente'::character varying, 'Suspendu'::character varying, 'Quitté'::character varying]::text[])", name='membre_statut_check'),
        ForeignKeyConstraint(['id_espace'], ['planer.espace.id'], ondelete='SET NULL', name='membre_id_espace_fkey'),
        ForeignKeyConstraint(['id_liste'], ['planer.liste.id'], ondelete='SET NULL', name='membre_id_liste_fkey'),
        ForeignKeyConstraint(['id_tache'], ['planer.tache.id'], ondelete='SET NULL', name='membre_id_tache_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['.public.utilisateur.id'], ondelete='SET NULL', name='membre_id_utilisateur_fkey'),
        ForeignKeyConstraint(['id_workspace'], ['planer.workspace.id'], ondelete='SET NULL', name='membre_id_workspace_fkey'),
        PrimaryKeyConstraint('id', name='membre_pkey'),
        Index('idx_membre_espace', 'id_espace'),
        Index('idx_membre_espace_unique', 'id_utilisateur', 'id_espace', unique=True),
        Index('idx_membre_liste', 'id_liste'),
        Index('idx_membre_liste_unique', 'id_utilisateur', 'id_liste', unique=True),
        Index('idx_membre_role', 'role'),
        Index('idx_membre_statut', 'statut'),
        Index('idx_membre_tache', 'id_tache'),
        Index('idx_membre_tache_unique', 'id_utilisateur', 'id_tache', unique=True),
        Index('idx_membre_utilisateur', 'id_utilisateur'),
        Index('idx_membre_workspace', 'id_workspace'),
        Index('idx_membre_workspace_unique', 'id_utilisateur', 'id_workspace', unique=True),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    role: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'Membre'::character varying"))
    statut: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'Actif'::character varying"))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='ST NULL'))
    id_workspace: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.workspace.id', ondelete='SET NULL'))
    id_espace: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.espace.id', ondelete='SET NULL'))
    id_liste: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.liste.id', ondelete='SET NULL'))
    id_tache: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.tache.id', ondelete='SET NULL'))

    #Relation
    espace: Mapped[Optional['Espace']] = relationship('Espace', back_populates='membre')
    liste: Mapped[Optional['Liste']] = relationship('Liste', back_populates='membre')
    tache: Mapped[Optional['Tache']] = relationship('Tache', back_populates='membre')
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='membre')
    workspace: Mapped[Optional['Workspace']] = relationship('Workspace', back_populates='membre')
    absence_et_conge: Mapped[list['AbsenceEtConge']] = relationship('AbsenceEtConge', back_populates='membre')
    fichier: Mapped[list['Fichier']] = relationship('Fichier', back_populates='membre')
    rapport: Mapped[list['Rapport']] = relationship('Rapport', back_populates='membre')


class Section(Base):
    __tablename__ = 'section'
    __table_args__ = (
        ForeignKeyConstraint(['id_canevas'], ['planer.canevas.id'], ondelete='SET NULL', name='section_id_canevas_fkey'),
        PrimaryKeyConstraint('id', name='section_pkey'),
        Index('idx_section_canevas', 'id_canevas'),
        Index('idx_section_titre', 'titre'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    titre: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_canevas: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.canevas.id', ondelete='SET NULL'))

    #Relation
    canevas: Mapped[Optional['Canevas']] = relationship('Canevas', back_populates='section')
    checklist: Mapped[list['Checklist']] = relationship('Checklist', back_populates='section')


class AbsenceEtConge(Base):
    __tablename__ = 'absence_et_conge'
    __table_args__ = (
        CheckConstraint('date_fin IS NULL OR date_fin >= date_debut', name='absence_et_conge_date_fin_check'),
        CheckConstraint('duree_demandee_en_jours IS NULL OR duree_demandee_en_jours >= 0', name='absence_et_conge_duree_check'),
        CheckConstraint("statut::text = ANY (ARRAY['en_attente'::text, 'approuvee'::text, 'rejetee'::text, 'annulee'::text, 'terminee'::text])", name='absence_et_conge_statut_check'),
        ForeignKeyConstraint(['id_membre'], ['planer.membre.id'], ondelete='SET NULL', name='absence_et_conge_id_membre_fkey'),
        PrimaryKeyConstraint('id', name='absence_et_conge_pkey'),
        Index('idx_absence_et_conge_date_debut', 'date_debut'),
        Index('idx_absence_et_conge_membre', 'id_membre'),
        Index('idx_absence_et_conge_statut', 'statut'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    is_absence: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    date_debut: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    statut: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'en_attente'::character varying"))
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    is_conge_planifie: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    date_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    motif: Mapped[Optional[str]] = mapped_column(String(255))
    duree_demandee_en_jours: Mapped[Optional[int]] = mapped_column(Integer)
    decision_commentaire: Mapped[Optional[str]] = mapped_column(Text)
    id_membre: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.membre.id', ondelete='SET NULL'))

    #Relation
    membre: Mapped[Optional['Membre']] = relationship('Membre', back_populates='absence_et_conge')


class Checklist(Base):
    __tablename__ = 'checklist'
    __table_args__ = (
        ForeignKeyConstraint(['id_section'], ['planer.section.id'], ondelete='SET NULL', name='checklist_id_section_fkey'),
        ForeignKeyConstraint(['id_tache'], ['planer.tache.id'], ondelete='SET NULL', name='checklist_id_tache_fkey'),
        PrimaryKeyConstraint('id', name='checklist_pkey'),
        Index('idx_checklist_is_checked', 'is_checked'),
        Index('idx_checklist_section', 'id_section'),
        Index('idx_checklist_tache', 'id_tache'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    texte: Mapped[str] = mapped_column(String(255), nullable=False)
    is_checked: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id_section: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.section.id', ondelete='SET NULL'))
    id_tache: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.tache.id', ondelete='SET NULL'))

    #Relation
    section: Mapped[Optional['Section']] = relationship('Section', back_populates='checklist')
    tache: Mapped[Optional['Tache']] = relationship('Tache', back_populates='checklist')


class Fichier(Base):
    __tablename__ = 'fichier'
    __table_args__ = (
        ForeignKeyConstraint(['id_membre'], ['planer.membre.id'], ondelete='SET NULL', name='fichier_id_membre_fkey'),
        PrimaryKeyConstraint('id', name='fichier_pkey'),
        Index('idx_fichier_membre', 'id_membre'),
        Index('idx_fichier_type_fichier', 'type_fichier'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    url_fichier: Mapped[Optional[str]] = mapped_column(String(255))
    type_fichier: Mapped[Optional[str]] = mapped_column(String(20))
    meta_donnees: Mapped[Optional[dict]] = mapped_column(JSON)
    id_membre: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.membre.id', ondelete='SET NULL'))

    #Relation
    membre: Mapped[Optional['Membre']] = relationship('Membre', back_populates='fichier')


class Rapport(Base):
    __tablename__ = 'rapport'
    __table_args__ = (
        ForeignKeyConstraint(['id_membre'], ['planer.membre.id'], ondelete='SET NULL', name='rapport_id_membre_fkey'),
        PrimaryKeyConstraint('id', name='rapport_pkey'),
        Index('idx_rapport_membre', 'id_membre'),
        Index('idx_rapport_periode_debut', 'periode_debut'),
        Index('idx_rapport_periode_fin', 'periode_fin'),
        {'schema': 'planer'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    titre: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    realisations: Mapped[Optional[str]] = mapped_column(Text)
    difficultes_et_solutions: Mapped[Optional[str]] = mapped_column(Text)
    commentaire: Mapped[Optional[str]] = mapped_column(Text)
    fichier_joint: Mapped[Optional[str]] = mapped_column(String(255))
    periode_debut: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    periode_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_membre: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('planer.membre.id', ondelete='SET NULL'))

    #Relation
    membre: Mapped[Optional['Membre']] = relationship('Membre', back_populates='rapport')



#================================================Schemas Plateforme===============================================

class Plateforme(Base):
    __tablename__ = 'plateforme'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='plateforme_pk'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom_plateforme: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    logo_plateforme: Mapped[Optional[str]] = mapped_column(String(255))
    url_plateforme: Mapped[Optional[str]] = mapped_column(String(255))
    date_creation: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    adresse_plateforme: Mapped[list['AdressePlateforme']] = relationship('AdressePlateforme', foreign_keys='[AdressePlateforme.plateforme_id]', back_populates='plateforme')
    contact_plateforme: Mapped[list['ContactPlateforme']] = relationship('ContactPlateforme', foreign_keys='[ContactPlateforme.plateforme_id]', back_populates='plateforme')
    information_plateforme: Mapped[list['InformationPlateforme']] = relationship('InformationPlateforme', foreign_keys='[InformationPlateforme.plateforme_id]', back_populates='plateforme')
    partenaire_plateforme: Mapped[list['PartenairePlateforme']] = relationship('PartenairePlateforme', back_populates='plateforme')
    reseaux_sociaux_plateforme: Mapped[list['ReseauxSociauxPlateforme']] = relationship('ReseauxSociauxPlateforme', foreign_keys='[ReseauxSociauxPlateforme.plateforme_id]', back_populates='plateforme')
    service_plateforme: Mapped[list['ServicePlateforme']] = relationship('ServicePlateforme', foreign_keys='[ServicePlateforme.plateforme_id]', back_populates='plateforme')


class AdressePlateforme(Base):
    __tablename__ = 'adresse_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='adresse_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id', name='adresse_plateforme_pk'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    adresse_ligne1: Mapped[str] = mapped_column(String(255), nullable=False)
    ville: Mapped[str] = mapped_column(String(100), nullable=False)
    code_postal: Mapped[str] = mapped_column(String(20), nullable=False)
    pays: Mapped[str] = mapped_column(String(100), nullable=False)
    adresse_ligne2: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='adresse_plateforme')


class ContactPlateforme(Base):
    __tablename__ = 'contact_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='contact_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id', name='contact_plateforme_pk'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    nom_contact: Mapped[str] = mapped_column(String(255), nullable=False)
    email_contact: Mapped[str] = mapped_column(String(255), nullable=False)
    telephone_contact: Mapped[Optional[str]] = mapped_column(String(50))
    mobile_contact: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='contact_plateforme')



class InformationPlateforme(Base):
    __tablename__ = 'information_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='information_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id', name='information_plateforme_pk'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    copyright_info: Mapped[Optional[str]] = mapped_column(Text)
    termes_conditions_utilisation: Mapped[Optional[str]] = mapped_column(Text)
    politique_confidentialite: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='information_plateforme')


class PartenairePlateforme(Base):
    __tablename__ = 'partenaire_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['id_plateforme'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='partenaire_plateforme_id_plateforme_fkey'),
        PrimaryKeyConstraint('id', name='partenaire_plateforme_pk'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    id_plateforme: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    secteur_activite: Mapped[Optional[str]] = mapped_column(String(255))
    site_web: Mapped[Optional[str]] = mapped_column(String(255))
    logo_url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    #Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='partenaire_plateforme')


class ReseauxSociauxPlateforme(Base):
    __tablename__ = 'reseaux_sociaux_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='reseaux_sociaux_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id', name='reseaux_sociaux_plateforme_pk'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    nom_reseau_social: Mapped[str] = mapped_column(String(100), nullable=False)
    url_reseau_social: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_reseau_social: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='reseaux_sociaux_plateforme')


class ServicePlateforme(Base):
    __tablename__ = 'service_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='service_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id', name='service_plateforme_pk'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    nom_service: Mapped[str] = mapped_column(String(255), nullable=False)
    description_service: Mapped[Optional[str]] = mapped_column(Text)
    tarif_service: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    media_service: Mapped[Optional[str]] = mapped_column(String(255))
    type_media_service: Mapped[Optional[str]] = mapped_column(String(25))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='service_plateforme')


class AnnoncePlateforme(Base):
    __tablename__ = 'annonce_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='annonce_plateforme_plateforme_id_fkey'),
        ForeignKeyConstraint(['type_annonce_id'], ['utilitaire.type_annonce.id'], ondelete='CASCADE',onupdate='CASCADE', name='annonce_plateforme_type_annonce_id_fkey'),
        PrimaryKeyConstraint('id'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    type_annonce_id: Mapped[str] = mapped_column(String(12), ForeignKey('utilitaire.type_annonce.id', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
    titre_annonce: Mapped[str] = mapped_column(String(255), nullable=False)
    media_annonce: Mapped[Optional[str]] = mapped_column(String(255))
    type_media_annonce: Mapped[Optional[str]] = mapped_column(String(25))
    logo_annonce: Mapped[Optional[str]] = mapped_column(String(255))
    duree: Mapped[Optional[str]] = mapped_column(String(10))
    description_annonce: Mapped[Optional[str]] = mapped_column(Text)
    date_publication: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    date_expiration: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    # Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='annonce_plateforme')
    type_annonce: Mapped['TypeAnnonce'] = relationship('TypeAnnonce', back_populates='annonce_plateforme')


class TutorielPlateforme(Base):
    __tablename__ = 'tutoriel_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='tutoriel_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    titre_tutoriel: Mapped[str] = mapped_column(String(255), nullable=False)
    media_tutoriel: Mapped[Optional[str]] = mapped_column(String(255))
    type_media_tutoriel: Mapped[Optional[str]] = mapped_column(String(25))
    url_tutoriel: Mapped[Optional[str]] = mapped_column(String(255))
    description_tutoriel: Mapped[Optional[str]] = mapped_column(Text)
    date_publication: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    # Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='tutoriel_plateforme')


class AboutPlateforme(Base):
    __tablename__ = 'about_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='about_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    nos_valeurs: Mapped[Optional[str]] = mapped_column(Text)
    nos_objectifs: Mapped[Optional[str]] = mapped_column(Text)
    notre_vision: Mapped[Optional[str]] = mapped_column(Text)
    description_about: Mapped[Optional[str]] = mapped_column(Text)
    nom: Mapped[Optional[str]] = mapped_column(String(25))
    prenoms: Mapped[Optional[str]] = mapped_column(String(100))
    poste: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    # Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='about_plateforme')


class FaqPlateforme(Base):
    __tablename__ = 'faq_plateforme'
    __table_args__ = (
        ForeignKeyConstraint(['plateforme_id'], ['plateforme.plateforme.id'], ondelete='CASCADE', name='faq_plateforme_plateforme_id_fkey'),
        PrimaryKeyConstraint('id'),
        {'schema': 'plateforme'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    plateforme_id: Mapped[str] = mapped_column(String(12), ForeignKey('plateforme.plateforme.id', ondelete='CASCADE'), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    reponse: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    # Relation
    plateforme: Mapped['Plateforme'] = relationship('Plateforme', back_populates='faq_plateforme')



#===============================================Schemas Utilitaire============================================================

class Competence(Base):
    __tablename__ = 'competence'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='competence_pk'),
        UniqueConstraint('nom', name='competence_unique'),
        {'comment': 'Référentiel des compétences disponibles dans le système',
     'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    categorie: Mapped[Optional[str]] = mapped_column(String(100), comment='Ex: Technique, Comportementale, Linguistique, Outils, etc.')
    niveau_reference: Mapped[Optional[str]] = mapped_column(String(50), comment='Ex: Débutant, Intermédiaire, Avancé, Expert')

    #Relation
    candidat_competence: Mapped[list['CandidatCompetence']] = relationship('CandidatCompetence', back_populates='competence')
    offre_emploi_competence_requise: Mapped[list['OffreEmploiCompetenceRequise']] = relationship('OffreEmploiCompetenceRequise', back_populates='competence')


class Domaine(Base):
    __tablename__ = 'domaine'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='domaine_pk'),
        {'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    candidat: Mapped[list['Candidat']] = relationship('Candidat', back_populates='domaine')
    secteurs_activite_entreprise: Mapped[list['SecteursActiviteEntreprise']] = relationship('SecteursActiviteEntreprise', back_populates='domaine')
    offre_emploi: Mapped[list['OffreEmploi']] = relationship('OffreEmploi', back_populates='domaine')


class Pays(Base):
    __tablename__ = 'pays'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pays_pk'),
        {'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False, server_default=text("'Bénin'::character varying"))
    langue: Mapped[Optional[str]] = mapped_column(String(100))
    monnaie: Mapped[Optional[str]] = mapped_column(String(50))

    #Relation
    localite: Mapped[list['Localite']] = relationship('Localite', back_populates='pays')


class ProcessusDeCandidature(Base):
    __tablename__ = 'processus_de_candidature'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pdc_pk'),
        {'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    type_processus: Mapped[Optional[str]] = mapped_column(String(200), comment='Candidature en ligne via la plateforme, Candidature en ligne via Email, Candidature en ligne via Whasapp, Candidature en ligne via un autre site web, Candidature hors ligne')

    #Relation
    processus_offre_emploi: Mapped[list['ProcessusOffreEmploi']] = relationship('ProcessusOffreEmploi', back_populates='processus_de_candidature')


class TypeAnnonce(Base):
    __tablename__ = 'type_annonce'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='type_annonce_pk'),
        {'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(35), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TypeEvaluationEntretien(Base):
    __tablename__ = 'type_evaluation_entretien'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='type_evaluation_entretien_pk'),
        {'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom_type_evaluation: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    entretiens: Mapped[list['Entretiens']] = relationship('Entretiens', back_populates='type_evaluation_entretien')
    evaluations: Mapped[list['Evaluations']] = relationship('Evaluations', back_populates='type_evaluation_entretien')


class TypeOffre(Base):
    __tablename__ = 'type_offre'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='type_offre_pk'),
        {'comment': 'Travail, Freelance, Job/Service', 'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False, comment="'Travail', 'Freelance', 'Job/Service'")

    #Relation
    offre_emploi: Mapped[list['OffreEmploi']] = relationship('OffreEmploi', back_populates='type_offre')

class Localite(Base):
    __tablename__ = 'localite'
    __table_args__ = (
        ForeignKeyConstraint(['id_pays'], ['utilitaire.pays.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='localite_id_pays_fkey'),
        PrimaryKeyConstraint('id', name='localite_pk'),
        {'schema': 'utilitaire'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False, comment='Indéfini, Cotonou, Abomey-Calavi, Parakou...')
    id_pays: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.pays.id', ondelete='SET NULL'))

    #Relation
    pays: Mapped[Optional['Pays']] = relationship('Pays', back_populates='localite')
    entreprise: Mapped[list['Entreprise']] = relationship('Entreprise', back_populates='localite')
    candidat: Mapped[list['Candidat']] = relationship('Candidat', back_populates='localite')
    annexe_entreprise: Mapped[list['AnnexeEntreprise']] = relationship('AnnexeEntreprise', back_populates='localite')
    offre_emploi: Mapped[list['OffreEmploi']] = relationship('OffreEmploi', back_populates='localite')


#=============================================Schemas Messenger=========================================================

class Contact(Base):
    __tablename__ = 'contact'
    __table_args__ = (
        CheckConstraint('requester_id::text <> addressee_id::text', name='contact_distinct_users_check'),
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'accepted'::character varying, 'blocked'::character varying]::text[])", name='contact_status_check'),
        ForeignKeyConstraint(['addressee_id'], ['public.utilisateur.id'], ondelete='SET NULL', name='contact_addressee_id_fkey'),
        ForeignKeyConstraint(['requester_id'], ['public.utilisateur.id'], ondelete='SET NULL', name='contact_requester_id_fkey'),
        PrimaryKeyConstraint('id', name='contact_pkey'),
        UniqueConstraint('requester_id', 'addressee_id', name='contact_request_unique'),
        {'schema': 'messenger'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    requester_id: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'), nullable=False)
    addressee_id: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pending'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    addressee: Mapped['Utilisateur'] = relationship('Utilisateur', foreign_keys=[addressee_id], back_populates='contact')
    requester: Mapped['Utilisateur'] = relationship('Utilisateur', foreign_keys=[requester_id], back_populates='contact')


class Groupe(Base):
    __tablename__ = 'groupe'
    __table_args__ = (
        ForeignKeyConstraint(['creator'], ['public.utilisateur.id'], ondelete='SET NULL', name='groupe_creator_fkey'),
        PrimaryKeyConstraint('id', name='groupe_pkey'),
        {'schema': 'messenger'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    creator: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    photo_url: Mapped[Optional[str]] = mapped_column(String(512))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='groupe')
    groupe_members: Mapped[list['GroupeMembers']] = relationship('GroupeMembers', back_populates='groupe')
    message: Mapped[list['Message']] = relationship('Message', back_populates='groupe')
    notification: Mapped[list['Notification']] = relationship('Notification_', back_populates='groupe')


class Room(Base):
    __tablename__ = 'room'
    __table_args__ = (
        CheckConstraint('member1::text < member2::text', name='room_members_order_check'),
        CheckConstraint('member1::text <> member2::text', name='room_members_distinct_check'),
        ForeignKeyConstraint(['member1'], ['public.utilisateur.id'], ondelete='RESTRICT', name='room_member1_fkey'),
        ForeignKeyConstraint(['member2'], ['public.utilisateur.id'], ondelete='RESTRICT', name='room_member2_fkey'),
        PrimaryKeyConstraint('id', name='room_pkey'),
        UniqueConstraint('member1', 'member2', name='room_members_unique'),
        {'schema': 'messenger'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    member1: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='RESTRICT'), nullable=False)
    member2: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='RESTRICT'), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', foreign_keys=[member1], back_populates='room')
    utilisateur_: Mapped['Utilisateur'] = relationship('Utilisateur', foreign_keys=[member2], back_populates='room_')
    message: Mapped[list['Message']] = relationship('Message', back_populates='room')


class UserPresence(Utilisateur):
    __tablename__ = 'user_presence'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', name='user_presence_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id_utilisateur', name='user_presence_pkey'),
        {'schema': 'messenger'}
    )

    id_utilisateur: Mapped[str] = mapped_column(String(12), primary_key=True)
    is_online: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    last_seen: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    do_not_disturb: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    custom_status: Mapped[Optional[str]] = mapped_column(String(255))


class GroupeMembers(Base):
    __tablename__ = 'groupe_members'
    __table_args__ = (
        CheckConstraint("role::text = ANY (ARRAY['admin'::character varying, 'member'::character varying, 'guest'::character varying]::text[])", name='groupe_members_role_check'),
        ForeignKeyConstraint(['id_groupe'], ['messenger.groupe.id'], ondelete='SET NULL', name='groupe_members_id_groupe_fkey'),
        ForeignKeyConstraint(['member'], ['public.utilisateur.id'], ondelete='SET NULL', name='groupe_members_member_fkey'),
        PrimaryKeyConstraint('id_groupe', 'member', name='groupe_members_pkey'),
        {'schema': 'messenger'}
    )

    id_groupe: Mapped[str] = mapped_column(String(12), primary_key=True)
    member: Mapped[str] = mapped_column(String(12), primary_key=True)
    role: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'member'::character varying"))
    joined_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    groupe: Mapped['Groupe'] = relationship('Groupe', back_populates='groupe_members')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='groupe_members')


class Message(Base):
    __tablename__ = 'message'
    __table_args__ = (
        CheckConstraint('id_room IS NOT NULL AND id_groupe IS NULL OR id_room IS NULL AND id_groupe IS NOT NULL', name='message_target_check'),
        ForeignKeyConstraint(['id_groupe'], ['messenger.groupe.id'], ondelete='SET NULL', name='message_id_groupe_fkey'),
        ForeignKeyConstraint(['id_room'], ['messenger.room.id'], ondelete='SET NULL', name='message_id_room_fkey'),
        ForeignKeyConstraint(['reply_to_id'], ['messenger.message.id'], ondelete='SET NULL', name='message_reply_to_id_fkey'),
        ForeignKeyConstraint(['sender'], ['public.utilisateur.id'], ondelete='RESTRICT', name='message_sender_fkey'),
        PrimaryKeyConstraint('id', name='message_pkey'),
        {'schema': 'messenger'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    sender: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='RESTRICT'), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'text'::character varying"))
    message: Mapped[Optional[str]] = mapped_column(Text)
    audio: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    file: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    image: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    video: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    date_modif: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    date_sup: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    seen: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    id_room: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('messenger.room.id', ondelete='SET NULL'))
    id_groupe: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('messenger.groupe.id', ondelete='SET NULL'))
    reply_to_id: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('messenger.message.id', ondelete='SET NULL'))
    is_pinned: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    is_edited: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    #Relation
    groupe: Mapped[Optional['Groupe']] = relationship('Groupe', back_populates='message')
    room: Mapped[Optional['Room']] = relationship('Room', back_populates='message')
    reply_to: Mapped[Optional['Message']] = relationship('Message', remote_side=[id], back_populates='reply_to_reverse')
    reply_to_reverse: Mapped[list['Message']] = relationship('Message', remote_side=[reply_to_id], back_populates='reply_to')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='message')
    attachment: Mapped[list['Attachment']] = relationship('Attachment', back_populates='message')
    message_reaction: Mapped[list['MessageReaction']] = relationship('MessageReaction', back_populates='message')
    message_read_receipt: Mapped[list['MessageReadReceipt']] = relationship('MessageReadReceipt', back_populates='message')


class Notification_(Base):
    __tablename__ = 'notification'
    __table_args__ = (
        ForeignKeyConstraint(['id_groupe'], ['messenger.groupe.id'], ondelete='SET NULL', name='notification_id_groupe_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', name='notification_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='notification_pkey'),
        {'schema': 'messenger'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    id_groupe: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('messenger.groupe.id', ondelete='SET NULL'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    est_lu: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    #Relation
    groupe: Mapped[Optional['Groupe']] = relationship('Groupe', back_populates='notification')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='notification_')

class Attachment(Base):
    __tablename__ = 'attachment'
    __table_args__ = (
        ForeignKeyConstraint(['id_message'], ['messenger.message.id'], ondelete='SET NULL', name='attachment_id_message_fkey'),
        PrimaryKeyConstraint('id', name='attachment_pkey'),
        {'schema': 'messenger'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_message: Mapped[str] = mapped_column(String(12), ForeignKey('messenger.message.id', ondelete='SET NULL'), nullable=False)
    file_url: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[Optional[str]] = mapped_column(String(100))
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    original_name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    message: Mapped['Message'] = relationship('Message', back_populates='attachment')


class MessageReaction(Base):
    __tablename__ = 'message_reaction'
    __table_args__ = (
        ForeignKeyConstraint(['id_message'], ['messenger.message.id'], ondelete='SET NULL', name='message_reaction_id_message_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', name='message_reaction_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='message_reaction_pkey'),
        UniqueConstraint('id_message', 'id_utilisateur', 'emoji', name='message_reaction_id_message_id_utilisateur_emoji_key'),
        {'schema': 'messenger'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_message: Mapped[str] = mapped_column(String(12), ForeignKey('messenger.message.id', ondelete='SET NULL'), nullable=False)
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))
    emoji: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    message: Mapped['Message'] = relationship('Message', back_populates='message_reaction')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='message_reaction')


class MessageReadReceipt(Base):
    __tablename__ = 'message_read_receipt'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['delivered'::character varying, 'read'::character varying]::text[])", name='message_read_receipt_status_check'),
        ForeignKeyConstraint(['id_message'], ['messenger.message.id'], ondelete='SET NULL', name='message_read_receipt_id_message_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', name='message_read_receipt_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id_message', 'id_utilisateur', name='message_read_receipt_pkey'),
        {'schema': 'messenger'}
    )

    id_message: Mapped[str] = mapped_column(String(12), primary_key=True)
    id_utilisateur: Mapped[str] = mapped_column(String(12), primary_key=True)
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'delivered'::character varying"))
    status_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    #Relation
    message: Mapped['Message'] = relationship('Message', back_populates='message_read_receipt')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='message_read_receipt')


#====================================================Schemas Talent=======================================================

class AuditLog(Base):
    __tablename__ = 'audit_log'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='audit_log_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='audit_log_pk'),
        Index('idx_audit_log_created', 'created_at'),
        Index('idx_audit_log_table', 'table_affectee'),
        Index('idx_audit_log_utilisateur', 'id_utilisateur'),
        {'comment': "Journalisation d'audit pour tracer toutes les modifications de "
                'données',
     'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    operation: Mapped[str] = mapped_column(String(20), nullable=False, comment='CREATE, READ, UPDATE, DELETE')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))
    table_affectee: Mapped[Optional[str]] = mapped_column(String(100), comment='Nom de la table modifiée')
    id_enregistrement: Mapped[Optional[str]] = mapped_column(String(12), comment="ID de l'enregistrement modifié")
    ancienne_valeur: Mapped[Optional[dict]] = mapped_column(JSONB, comment='Valeur avant modification (au format JSON)')
    nouvelle_valeur: Mapped[Optional[dict]] = mapped_column(JSONB, comment='Valeur après modification (au format JSON)')
    adresse_ip: Mapped[Optional[str]] = mapped_column(String(50))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='audit_log')


class Notification(Base):
    __tablename__ = 'notification'
    __table_args__ = (
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='notification_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='notification_pk'),
        {'comment': 'Notifications destinées aux utilisateurs', 'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='CASCADE'))
    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    est_lue: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    message: Mapped[Optional[str]] = mapped_column(Text)
    type_notification: Mapped[Optional[str]] = mapped_column(String(50), comment='Candidature, Entretien, Offre, Statut, Message, Autre')
    lien_action: Mapped[Optional[str]] = mapped_column(String(255))
    lu_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='notification')


class Candidat(Base):
    __tablename__ = 'candidat'
    __table_args__ = (
        CheckConstraint("situation_matrimoniale::text = ANY (ARRAY['Célibataire'::character varying, 'Concubin(e)'::character varying, 'Marié(e)'::character varying, 'Divorcé(e)'::character varying, 'Veuf(ve)'::character varying]::text[])", name='iu_situation_matrimoniale_check'),
        ForeignKeyConstraint(['id_domaine'], ['utilitaire.domaine.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='candidat_id_domaine_fkey'),
        ForeignKeyConstraint(['id_localite'], ['utilitaire.localite.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='candidat_id_localite_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='candidat_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='iu_pk'),
        UniqueConstraint('id_utilisateur', name='candidat_id_utilisateur_key'),
        UniqueConstraint('numero_ifu', name='iu_constr_numero_ifu'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    prenoms: Mapped[str] = mapped_column(String(100), nullable=False, comment='Les prénoms separés par espaces')
    date_naissance: Mapped[Optional[datetime.date]] = mapped_column(Date)
    lieu_naissance: Mapped[Optional[str]] = mapped_column(String(100))
    adresse: Mapped[Optional[str]] = mapped_column(String(255), comment='Adresse complet (combinaison peut-être de departement, commune, arr, quartier, maison...)')
    situation_matrimoniale: Mapped[Optional[str]] = mapped_column(String(50), comment="in ('Célibataire', 'Concubin(e)', 'Marié(e)', 'Divorcé(e)', 'Veuf(ve)')")
    telephone: Mapped[Optional[str]] = mapped_column(String(20))
    numero_ifu: Mapped[Optional[str]] = mapped_column(String(13))
    photo: Mapped[Optional[str]] = mapped_column(String(255))
    titre_professionnel: Mapped[Optional[str]] = mapped_column(String(255), comment='Titre ou résumé professionnel du candidat')
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'))
    genre: Mapped[Optional[str]] = mapped_column(String(15), comment="'Masculin', 'Féminin'")
    plus_grand_diplome: Mapped[Optional[str]] = mapped_column(String(150), comment='CEP, BEPC, BAC, LICENCE, BACHELOR, MASTER, DOCTORAT...')
    id_domaine: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.domaine.id', ondelete='SET NULL'))
    lien_portfolio: Mapped[Optional[str]] = mapped_column(String(255))
    id_localite: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.localite.id', ondelete='SET NULL'))

    #Relation
    domaine: Mapped[Optional['Domaine']] = relationship('Domaine', back_populates='candidat')
    localite: Mapped[Optional['Localite']] = relationship('Localite', back_populates='candidat')
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='candidat')
    candidat_competence: Mapped[list['CandidatCompetence']] = relationship('CandidatCompetence', back_populates='candidat')
    fichiers_importes: Mapped[list['FichiersImportes']] = relationship('FichiersImportes', back_populates='candidat')
    candidature: Mapped[list['Candidature']] = relationship('Candidature', back_populates='candidat')
    entretiens: Mapped[list['Entretiens']] = relationship('Entretiens', back_populates='candidat')
    evaluations: Mapped[list['Evaluations']] = relationship('Evaluations', back_populates='candidat')


class AnnexeEntreprise(Base):
    __tablename__ = 'annexe_entreprise'
    __table_args__ = (
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='annexe_entreprise_id_entreprise_fkey'),
        ForeignKeyConstraint(['id_localite'], ['utilitaire.localite.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='annexe_entreprise_id_localite_fkey'),
        PrimaryKeyConstraint('id', name='annexe_entreprise_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom_annexe: Mapped[str] = mapped_column(String(100), nullable=False, comment='exemple Orabank Abomey-Calavi')
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'))
    id_localite: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.localite.id', ondelete='SET NULL'))
    adresse: Mapped[Optional[str]] = mapped_column(String(255))
    telephone: Mapped[Optional[str]] = mapped_column(String(20))

    #Relation
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='annexe_entreprise')
    localite: Mapped[Optional['Localite']] = relationship('Localite', back_populates='annexe_entreprise')
    departement_entreprise: Mapped[list['DepartementEntreprise']] = relationship('DepartementEntreprise', back_populates='annexe_entreprise')
    poste: Mapped[list['Poste']] = relationship('Poste', back_populates='annexe_entreprise')


class CritereEvaluation(Base):
    __tablename__ = 'critere_evaluation'
    __table_args__ = (
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='critere_evaluation_id_entreprise_fkey'),
        PrimaryKeyConstraint('id', name='critere_evaluation_pk'),
        {'comment': "Critères d'évaluation réutilisables dans les questionnaires",
     'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    type_critere: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Technique'::character varying"), comment='Technique, Comportemental, Communication, Leadership, etc.')
    poids_score: Mapped[decimal.Decimal] = mapped_column(Numeric(4, 2), nullable=False, server_default=text('1.0'), comment='Poids dans le calcul du score global (1.0 = normal, 2.0 = double, etc.)')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'), comment='Entreprise propriétaire du critère (null = générique)')

    #Relation
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='critere_evaluation')
    note_candidat: Mapped[list['NoteCandidat']] = relationship('NoteCandidat', back_populates='critere_evaluation')


class FichiersImportes(Base):
    __tablename__ = 'fichiers_importes'
    __table_args__ = (
        ForeignKeyConstraint(['id_candidat'], ['talent.candidat.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='fichiers_importes_id_candidat_fkey'),
        PrimaryKeyConstraint('id', name='fichiers_importes_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom_fichier: Mapped[str] = mapped_column(String(255), nullable=False)
    fichier: Mapped[str] = mapped_column(String(255), nullable=False, comment='Chemin ou URL du fichier')
    nature_fichier: Mapped[str] = mapped_column(String(200), nullable=False, server_default=text("'CV'::character varying"), comment="CV, Lettre de motivation, Attestation de diplôme, Attestation de travail, Permis de conduite, Carte CIP, Carte d'Identité Nationale, Passport, Acte de naissance....")
    visible_au_recruteur: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    date_ajout: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    type_fichier: Mapped[Optional[str]] = mapped_column(String(100))
    meta_donnees: Mapped[Optional[dict]] = mapped_column(JSONB)
    id_candidat: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.candidat.id', ondelete='SET NULL'))

    #Relation
    candidat: Mapped[Optional['Candidat']] = relationship('Candidat', back_populates='fichiers_importes')
    fichier_candidature: Mapped[list['FichierCandidature']] = relationship('FichierCandidature', back_populates='fichier_importe')


class SecteursActiviteEntreprise(Base):
    __tablename__ = 'secteurs_activite_entreprise'
    __table_args__ = (
        ForeignKeyConstraint(['id_domaine'], ['utilitaire.domaine.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='secteurs_activite_entreprise_id_domaine_fkey'),
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='secteurs_activite_entreprise_id_entreprise_fkey'),
        PrimaryKeyConstraint('id', name='sae_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'))
    id_domaine: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.domaine.id', ondelete='SET NULL'))

    #Relation
    domaine: Mapped[Optional['Domaine']] = relationship('Domaine', back_populates='secteurs_activite_entreprise')
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='secteurs_activite_entreprise')


class DepartementEntreprise(Base):
    __tablename__ = 'departement_entreprise'
    __table_args__ = (
        ForeignKeyConstraint(['id_annexe_entreprise'], ['talent.annexe_entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='departement_entreprise_id_annexe_entreprise_fkey'),
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='departement_entreprise_id_entreprise_fkey'),
        PrimaryKeyConstraint('id', name='departement_entreprise_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom_departement: Mapped[str] = mapped_column(String(100), nullable=False, comment='Exemple: Ressources Humaines, Informatique, Comptabilité...')
    description: Mapped[Optional[str]] = mapped_column(Text)
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'))
    id_annexe_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.annexe_entreprise.id', ondelete='SET NULL'))

    #Relation
    annexe_entreprise: Mapped[Optional['AnnexeEntreprise']] = relationship('AnnexeEntreprise', back_populates='departement_entreprise')
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='departement_entreprise')
    poste: Mapped[list['Poste']] = relationship('Poste', back_populates='departement_entreprise')


class Poste(Base):
    __tablename__ = 'poste'
    __table_args__ = (
        ForeignKeyConstraint(['id_annexe_entreprise'], ['talent.annexe_entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='poste_id_annexe_entreprise_fkey'),
        ForeignKeyConstraint(['id_departement'], ['talent.departement_entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='poste_id_departement_fkey'),
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='poste_id_entreprise_fkey'),
        PrimaryKeyConstraint('id', name='poste_pk'),
        {'comment': "Table pour gérer les postes prédéfinis dans l'hiérarchie "
                "organisationnelle de l'entreprise",
     'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    nom: Mapped[str] = mapped_column(String(150), nullable=False, comment='Intitulé du poste (ex: Développeur Senior, Chef de projet, etc.)')
    statut: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'Actif'::character varying"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    id_departement: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.departement_entreprise.id', ondelete='SET NULL'), comment='Référence au département/service si la structure existe')
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'), comment='Entreprise propriétaire du poste')
    id_annexe_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.annexe_entreprise.id', ondelete='SET NULL'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    #Relation
    annexe_entreprise: Mapped[Optional['AnnexeEntreprise']] = relationship('AnnexeEntreprise', back_populates='poste')
    departement_entreprise: Mapped[Optional['DepartementEntreprise']] = relationship('DepartementEntreprise', back_populates='poste')
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='poste')
    offre_emploi: Mapped[list['OffreEmploi']] = relationship('OffreEmploi', back_populates='poste')




class OffreEmploi(Base):
    __tablename__ = 'offre_emploi'
    __table_args__ = (
        ForeignKeyConstraint(['id_domaine'], ['utilitaire.domaine.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='offre_emploi_id_domaine_fkey'),
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='offre_emploi_id_entreprise_fkey'),
        ForeignKeyConstraint(['id_localite'], ['utilitaire.localite.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='offre_emploi_id_localite_fkey'),
        ForeignKeyConstraint(['id_poste_associe'], ['talent.poste.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='offre_emploi_id_poste_associe_fkey'),
        ForeignKeyConstraint(['id_type_offre'], ['utilitaire.type_offre.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='offre_emploi_id_type_offre_fkey'),
        PrimaryKeyConstraint('id', name='offre_emploi_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    titre_poste: Mapped[str] = mapped_column(String(100), nullable=False, comment="A coller automaitiquement dans le champ de formulaire associé et l'utilisateur peut modifier (offre étant associé à un poste)")
    description: Mapped[str] = mapped_column(Text, nullable=False, comment='responsablités specifiques, compétences requises, qualifications ou exigences requises')
    date_limite_candidature: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    date_pour_publier: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    nombre_poste: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default=text('1'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    statut: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'En attente'::character varying"), comment='En attente, En cours, Terminée, Annulée')
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    resume_poste: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    image: Mapped[Optional[str]] = mapped_column(String(255), comment='Une image peut être associée à une offre')
    fichiers_joints: Mapped[Optional[dict]] = mapped_column(JSONB, comment="Des fichiers (pdf ou autres) peuvent être joints à une offre d'emploi")
    horaires_de_travail: Mapped[Optional[str]] = mapped_column(String(255))
    slug: Mapped[Optional[str]] = mapped_column(String(255), comment='Pour URL plus significatif')
    id_poste_associe: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.poste.id', ondelete='SET NULL'), comment="Si cette offre d'emploi est associée à un poste (pré-enregistré dans l'hiérarchie organisationnelle --departements&postes) de l'entreprise, id_poste_associe est non-null et égal à id du poste en question")
    id_domaine: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.domaine.id', ondelete='SET NULL'))
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'))
    id_type_offre: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.type_offre.id', ondelete='SET NULL'))
    id_localite: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.localite.id', ondelete='SET NULL'))

    #Relation
    domaine: Mapped[Optional['Domaine']] = relationship('Domaine', back_populates='offre_emploi')
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='offre_emploi')
    localite: Mapped[Optional['Localite']] = relationship('Localite', back_populates='offre_emploi')
    poste: Mapped[Optional['Poste']] = relationship('Poste', back_populates='offre_emploi')
    type_offre: Mapped[Optional['TypeOffre']] = relationship('TypeOffre', back_populates='offre_emploi')
    candidature: Mapped[list['Candidature']] = relationship('Candidature', back_populates='offre_emploi')
    conditions_emploi: Mapped[list['ConditionsEmploi']] = relationship('ConditionsEmploi', back_populates='offre_emploi')
    offre_emploi_competence_requise: Mapped[list['OffreEmploiCompetenceRequise']] = relationship('OffreEmploiCompetenceRequise', back_populates='offre_emploi')
    processus_offre_emploi: Mapped[list['ProcessusOffreEmploi']] = relationship('ProcessusOffreEmploi', back_populates='offre_emploi')


class Candidature(Base):
    __tablename__ = 'candidature'
    __table_args__ = (
        ForeignKeyConstraint(['id_candidat'], ['talent.candidat.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='candidature_id_candidat_fkey'),
        ForeignKeyConstraint(['id_offre_emploi'], ['talent.offre_emploi.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='candidature_id_offre_emploi_fkey'),
        PrimaryKeyConstraint('id', name='candidature_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    date_candidature: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    statut: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'En attente'::character varying"), comment="in ('En attente', 'En cours', 'Refusée', 'Retenue')")
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'), comment='Date à laquelle le statut a changé')
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_offre_emploi: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.offre_emploi.id', ondelete='SET NULL'))
    id_candidat: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.candidat.id', ondelete='SET NULL'))

    #Relation
    candidat: Mapped[Optional['Candidat']] = relationship('Candidat', back_populates='candidature')
    offre_emploi: Mapped[Optional['OffreEmploi']] = relationship('OffreEmploi', back_populates='candidature')
    fichiers_joints: Mapped[list['FichiersJoints']] = relationship('FichiersJoints', back_populates='candidature')
    entretiens: Mapped[list['Entretiens']] = relationship('Entretiens', back_populates='candidature')
    evaluations: Mapped[list['Evaluations']] = relationship('Evaluations', back_populates='candidature')
    fichier_candidature: Mapped[list['FichierCandidature']] = relationship('FichierCandidature', back_populates='candidature')


class ConditionsEmploi(Base):
    __tablename__ = 'conditions_emploi'
    __table_args__ = (
        ForeignKeyConstraint(['id_offre_emploi'], ['talent.offre_emploi.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='conditions_emploi_id_offre_emploi_fkey'),
        PrimaryKeyConstraint('id', name='conditions_emploi_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    type_contrat: Mapped[Optional[str]] = mapped_column(String(50), comment='CDD, CDI, Stage, Autre')
    Temporalite: Mapped[Optional[str]] = mapped_column(String(100), comment='Temps plein, Temps partiel')
    disponibilite: Mapped[Optional[str]] = mapped_column(String(50), comment='Immédiat, Non-immédiat, Flexible')
    renumeration: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), comment='Le montant rénuméré ou Salaire (par heure, par jour, par semaine, mois, année)')
    renumeration_max: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), comment='Rénumération maximale dans le cas où on on veut spécifier un intervalle de rénumération (renumeration==renumeration_min)')
    periode_renumeration: Mapped[Optional[str]] = mapped_column(String(50), comment='Période rénumérée ou de paiement du salaire : Heure, Jour, Semaine, Mois, Année')
    type_renumeration: Mapped[Optional[str]] = mapped_column(String(50), comment='Nette, Brut, Minimum Nette,')
    diplome_minimum: Mapped[Optional[str]] = mapped_column(String(200), comment='Tout, CEP, BEPC, BAC, LICENCE, MASTER, DOCTORAT')
    nbre_annee_experiences: Mapped[Optional[int]] = mapped_column(SmallInteger)
    id_offre_emploi: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.offre_emploi.id', ondelete='SET NULL'))

    #Relation
    offre_emploi: Mapped[Optional['OffreEmploi']] = relationship('OffreEmploi', back_populates='conditions_emploi')


class OffreEmploiCompetenceRequise(Base):
    __tablename__ = 'offre_emploi_competence_requise'
    __table_args__ = (
        ForeignKeyConstraint(['id_competence'], ['utilitaire.competence.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='offre_emploi_competence_requise_id_competence_fkey'),
        ForeignKeyConstraint(['id_offre_emploi'], ['talent.offre_emploi.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='offre_emploi_competence_requise_id_offre_emploi_fkey'),
        PrimaryKeyConstraint('id', name='offre_emploi_competence_pk'),
        UniqueConstraint('id_offre_emploi', 'id_competence', name='offre_emploi_competence_unique'),
        {'comment': "Compétences requises pour une offre d'emploi", 'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_offre_emploi: Mapped[str] = mapped_column(String(12), ForeignKey('talent.offre_emploi.id', ondelete='CASCADE'), nullable=False)
    id_competence: Mapped[str] = mapped_column(String(12), ForeignKey('utilitaire.competence.id', ondelete='CASCADE'), nullable=False)
    niveau_requis: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Intermédiaire'::character varying"))
    est_obligatoire: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='Indique si la compétence est obligatoire ou souhaitable')

    #Relation
    competence: Mapped['Competence'] = relationship('Competence', back_populates='offre_emploi_competence_requise')
    offre_emploi: Mapped['OffreEmploi'] = relationship('OffreEmploi', back_populates='offre_emploi_competence_requise')


class ProcessusOffreEmploi(Base):
    __tablename__ = 'processus_offre_emploi'
    __table_args__ = (
        ForeignKeyConstraint(['id_offre_emploi'], ['talent.offre_emploi.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='processus_offre_emploi_id_offre_emploi_fkey'),
        ForeignKeyConstraint(['id_processus_de_candidature'], ['utilitaire.processus_de_candidature.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='processus_offre_emploi_id_processus_de_candidature_fkey'),
        PrimaryKeyConstraint('id', name='poe_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_offre_emploi: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.offre_emploi.id', ondelete='SET NULL'))
    id_processus_de_candidature: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.processus_de_candidature.id', ondelete='SET NULL'))
    coordonnee_candidature: Mapped[Optional[str]] = mapped_column(String(255), comment='Information ou coordonnée (comme adresse email, numéro whasapp, lieu de dépot de dossier) à utiliser par le candidat pour le dépot de candidature avec ce processus de candidature')
    nota_bene: Mapped[Optional[str]] = mapped_column(String(255), comment='Autres informations utiles à communiquer aux candidants pour ce processus de candidature')

    #Relation
    offre_emploi: Mapped[Optional['OffreEmploi']] = relationship('OffreEmploi', back_populates='processus_offre_emploi')
    processus_de_candidature: Mapped[Optional['ProcessusDeCandidature']] = relationship('ProcessusDeCandidature', back_populates='processus_offre_emploi')



class Entretiens(Base):
    __tablename__ = 'entretiens'
    __table_args__ = (
        ForeignKeyConstraint(['id_candidat'], ['talent.candidat.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='entretiens_id_candidat_fkey'),
        ForeignKeyConstraint(['id_candidature'], ['talent.candidature.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='entretiens_id_candidature_fkey'),
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='entretiens_id_entreprise_fkey'),
        ForeignKeyConstraint(['id_type_evaluation_entretien'], ['utilitaire.type_evaluation_entretien.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='entretiens_id_type_evaluation_entretien_fkey'),
        PrimaryKeyConstraint('id', name='entretien_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    date_entretien: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    statut: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'En attente'::character varying"), comment="in ('En attente', 'Effectué', 'Validé', 'Non Validé')")
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    commentaires_entretien: Mapped[Optional[str]] = mapped_column(Text, comment="Les observations issues de l'entretien")
    lieu_entretien: Mapped[Optional[str]] = mapped_column(String(255))
    localisation_maps_lieu_entretien: Mapped[Optional[str]] = mapped_column(String(255))
    url_externe_entretien: Mapped[Optional[str]] = mapped_column(String(255))
    note_questionnaires: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2), server_default=text('NULL::numeric'), comment='Note issue des questionnaires soumis au candidat')
    note_entretien_oral: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2), comment="Note d'entretien oral ou via vidéo conférence")
    note_autre: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2), server_default=text('NULL::numeric'), comment="Note issue d'autres évaluations d'entretien (questions oralement posées, présentation de forme et de fond du candidat)")
    duree: Mapped[Optional[int]] = mapped_column(Integer)
    id_candidature: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.candidature.id', ondelete='SET NULL'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_type_evaluation_entretien: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.type_evaluation_entretien.id', ondelete='SET NULL'))
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'), comment='id_entreprise important ici dans le cas où on ne passe forcement pas par la plateforme pour la candidature (entreprise peut créer un entretien et lui associer un candidat via son id)')
    id_candidat: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.candidat.id', ondelete='SET NULL'), comment='id_candidat important ici dans le cas où on ne passe forcement pas par la plateforme pour la candidature')

    #Relation
    candidat: Mapped[Optional['Candidat']] = relationship('Candidat', back_populates='entretiens')
    candidature: Mapped[Optional['Candidature']] = relationship('Candidature', back_populates='entretiens')
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='entretiens')
    type_evaluation_entretien: Mapped[Optional['TypeEvaluationEntretien']] = relationship('TypeEvaluationEntretien', back_populates='entretiens')
    evaluation_entretien: Mapped[list['EvaluationEntretien']] = relationship('EvaluationEntretien', back_populates='entretiens')
    questionnaire_entretien: Mapped[list['QuestionnaireEntretien']] = relationship('QuestionnaireEntretien', back_populates='entretiens')


class Evaluations(Base):
    __tablename__ = 'evaluations'
    __table_args__ = (
        ForeignKeyConstraint(['id_candidat'], ['talent.candidat.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='evaluations_id_candidat_fkey'),
        ForeignKeyConstraint(['id_candidature'], ['talent.candidature.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='evaluations_id_candidature_fkey'),
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='evaluations_id_entreprise_fkey'),
        ForeignKeyConstraint(['id_type_evaluation_entretien'], ['utilitaire.type_evaluation_entretien.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='evaluations_id_type_evaluation_entretien_fkey'),
        PrimaryKeyConstraint('id', name='evaluation_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    date_evaluation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    statut: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'En attente'::character varying"), comment="in ('En attente', 'Effectué', 'Validé', 'Non Validé')")
    statut_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    commentaires_evaluation: Mapped[Optional[str]] = mapped_column(Text, comment="Les observations issues de l'évaluation")
    lieu_evaluation: Mapped[Optional[str]] = mapped_column(String(255))
    localisation_maps_lieu_evaluation: Mapped[Optional[str]] = mapped_column(String(255))
    url_externe_evaluation: Mapped[Optional[str]] = mapped_column(String(255))
    note_questionnaires: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2), server_default=text('NULL::numeric'), comment='Note issue des questionnaires soumis au candidat')
    note_evaluation_oral: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2), comment="Note d'entretien oral ou via vidéo conférence")
    note_autre: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2), server_default=text('NULL::numeric'), comment="Note issue d'autres évaluations d'entretien (questions oralement posées, présentation de forme et de fond du candidat)")
    duree: Mapped[Optional[int]] = mapped_column(Integer)
    id_candidature: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.candidature.id', ondelete='SET NULL'))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'), comment='id_entreprise important ici dans le cas où on ne passe forcement pas par la plateforme pour la candidature (entreprise peut créer un entretien et lui associer un candidat via son id)')
    id_candidat: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.candidat.id', ondelete='SET NULL'), comment='id_candidat important ici dans le cas où on ne passe forcement pas par la plateforme pour la candidature')
    id_type_evaluation_entretien: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('utilitaire.type_evaluation_entretien.id', ondelete='SET NULL'))

    #Relation
    candidat: Mapped[Optional['Candidat']] = relationship('Candidat', back_populates='evaluations')
    candidature: Mapped[Optional['Candidature']] = relationship('Candidature', back_populates='evaluations')
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='evaluations')
    type_evaluation_entretien: Mapped[Optional['TypeEvaluationEntretien']] = relationship('TypeEvaluationEntretien', back_populates='evaluations')
    evaluation_evaluation: Mapped[list['EvaluationEvaluation']] = relationship('EvaluationEvaluation', back_populates='evaluations')
    questionnaire_evaluation: Mapped[list['QuestionnaireEvaluation']] = relationship('QuestionnaireEvaluation', back_populates='evaluations')


class FichierCandidature(Base):
    __tablename__ = 'fichier_candidature'
    __table_args__ = (
        ForeignKeyConstraint(['fichier_importe_id'], ['talent.fichiers_importes.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='fichier_candidature_fichier_importe_id_fkey'),
        ForeignKeyConstraint(['id_candidature'], ['talent.candidature.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='fichier_candidature_id_candidature_fkey'),
        PrimaryKeyConstraint('id', name='fichier_candidature_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    fichier_importe_id: Mapped[str] = mapped_column(String(12), ForeignKey('talent.fichiers_importes.id'), nullable=False)
    visible_au_recruteur: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    id_candidature: Mapped[str] = mapped_column(String(12), ForeignKey('talent.candidature.id', ondelete='CASCADE'), nullable=False)
    date_ajout: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    #Relation
    fichier_importe: Mapped['FichiersImportes'] = relationship('FichiersImportes', back_populates='fichier_candidature')
    candidature: Mapped['Candidature'] = relationship('Candidature', back_populates='fichier_candidature')


class EvaluationEntretien(Base):
    __tablename__ = 'evaluation_entretien'
    __table_args__ = (
        ForeignKeyConstraint(['id_entretien'], ['talent.entretiens.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='evaluation_entretien_id_entretien_fkey'),
        ForeignKeyConstraint(['id_evaluateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='evaluation_entretien_id_evaluateur_fkey'),
        PrimaryKeyConstraint('id', name='evaluation_entretien_pk'),
        Index('idx_evaluation_entretien_date', 'date_evaluation'),
        Index('idx_evaluation_entretien_evaluateur', 'id_evaluateur'),
        {'comment': "Synthèse de l'évaluation d'un entretien avec calculs de scores "
                'globaux',
     'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_entretien: Mapped[str] = mapped_column(String(12), ForeignKey('talent.entretiens.id', ondelete='CASCADE'), nullable=False)
    id_evaluateur: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'), nullable=False, comment="ID de l'utilisateur (recruteur/admin) qui évalue")
    date_evaluation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    statut_evaluation: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Brouillon'::character varying"), comment='Brouillon, En cours, Validée, Rejetée')
    score_total: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2), comment='Moyenne pondérée : (note_questionnaires + note_entretien_oral + note_autre) / 3')
    nombre_questions_repondues: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    nombre_questions_total: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    pourcentage_reussite: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2), comment='Pourcentage de réussite : (questions répondues / total) * 100')
    commentaire_evaluation: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    entretiens: Mapped['Entretiens'] = relationship('Entretiens', back_populates='evaluation_entretien')
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='evaluation_entretien')
    note_candidat: Mapped[list['NoteCandidat']] = relationship('NoteCandidat', back_populates='evaluation_entretien')


class EvaluationEvaluation(Base):
    __tablename__ = 'evaluation_evaluation'
    __table_args__ = (
        ForeignKeyConstraint(['id_evaluateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='evaluation_evaluation_id_evaluateur_fkey'),
        ForeignKeyConstraint(['id_evaluation'], ['talent.evaluations.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='evaluation_evaluation_id_evaluation_fkey'),
        PrimaryKeyConstraint('id', name='evaluation_evaluation_pk'),
        {'comment': "Synthèse de l'évaluation d'une évaluation avec calculs de scores "
                'globaux',
     'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_evaluation: Mapped[str] = mapped_column(String(12), ForeignKey('talent.evaluations.id', ondelete='CASCADE'), nullable=False)
    id_evaluateur: Mapped[str] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'), nullable=False, comment="ID de l'utilisateur (recruteur/admin) qui évalue")
    date_evaluation: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    statut_evaluation: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Brouillon'::character varying"), comment='Brouillon, En cours, Validée, Rejetée')
    score_total: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2), comment='Moyenne pondérée : (note_questionnaires + note_evaluation_oral + note_autre) / 3')
    nombre_questions_repondues: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    nombre_questions_total: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    pourcentage_reussite: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2), comment='Pourcentage de réussite : (questions répondues / total) * 100')
    commentaire_evaluation: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    utilisateur: Mapped['Utilisateur'] = relationship('Utilisateur', back_populates='evaluation_evaluation')
    evaluations: Mapped['Evaluations'] = relationship('Evaluations', back_populates='evaluation_evaluation')
    note_candidat: Mapped[list['NoteCandidat']] = relationship('NoteCandidat', back_populates='evaluation_evaluation')


class QuestionnaireEntretien(Base):
    __tablename__ = 'questionnaire_entretien'
    __table_args__ = (
        ForeignKeyConstraint(['id_entretiens'], ['talent.entretiens.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='questionnaire_entretien_id_entretiens_fkey'),
        ForeignKeyConstraint(['id_questionnaire'], ['survey.questionnaire.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='questionnaire_entretien_id_questionnaire_fkey'),
        PrimaryKeyConstraint('id', name='qee_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_questionnaire: Mapped[str] = mapped_column(String(12), ForeignKey('survey.questionnaire.id', ondelete='SET NULL'), nullable=False)
    id_entretiens: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.entretiens.id', ondelete='SET NULL'))
    ordre_questionnaire: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'), comment='Ordre dans lequel les questionnaires sont soumis')

    #Relation
    entretiens: Mapped[Optional['Entretiens']] = relationship('Entretiens', back_populates='questionnaire_entretien')
    questionnaire: Mapped['Questionnaire'] = relationship('Questionnaire', back_populates='questionnaire_entretien')
    reponse: Mapped[list['Reponse']] = relationship('Reponse', back_populates='questionnaire_entretien')


class QuestionnaireEvaluation(Base):
    __tablename__ = 'questionnaire_evaluation'
    __table_args__ = (
        ForeignKeyConstraint(['id_evaluations'], ['talent.evaluations.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='questionnaire_evaluation_id_evaluations_fkey'),
        ForeignKeyConstraint(['id_questionnaire'], ['survey.questionnaire.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='questionnaire_evaluation_id_questionnaire_fkey'),
        PrimaryKeyConstraint('id', name='qev_pk'),
        {'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_questionnaire: Mapped[str] = mapped_column(String(12), ForeignKey('survey.questionnaire.id', ondelete='SET NULL'), nullable=False)
    id_evaluations: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.evaluations.id', ondelete='SET NULL'))
    ordre_questionnaire: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'), comment='Ordre dans lequel les questionnaires sont soumis')

    #Relation
    evaluations: Mapped[Optional['Evaluations']] = relationship('Evaluations', back_populates='questionnaire_evaluation')
    questionnaire: Mapped['Questionnaire'] = relationship('Questionnaire', back_populates='questionnaire_evaluation')
    reponse: Mapped[list['Reponse']] = relationship('Reponse', back_populates='questionnaire_evaluation')


class NoteCandidat(Base):
    __tablename__ = 'note_candidat'
    __table_args__ = (
        ForeignKeyConstraint(['id_critere_evaluation'], ['talent.critere_evaluation.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='note_candidat_id_critere_evaluation_fkey'),
        ForeignKeyConstraint(['id_evaluation_entretien'], ['talent.evaluation_entretien.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='note_candidat_id_evaluation_entretien_fkey'),
        ForeignKeyConstraint(['id_evaluation_evaluation'], ['talent.evaluation_evaluation.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='note_candidat_id_evaluation_evaluation_fkey'),
        PrimaryKeyConstraint('id', name='note_candidat_pk'),
        UniqueConstraint('id_evaluation_entretien', 'id_critere_evaluation', name='note_candidat_unique'),
        {'comment': "Notes détaillées par critère d'évaluation pour un entretien",
     'schema': 'talent'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    id_evaluation_entretien: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.evaluation_entretien.id', ondelete='CASCADE'))
    id_evaluation_evaluation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.evaluation_evaluation.id', ondelete='CASCADE'))
    id_critere_evaluation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.critere_evaluation.id', ondelete='CASCADE'))
    note: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2), comment='Note sur 20 (ou autre échelle)')
    justification_note: Mapped[Optional[str]] = mapped_column(Text)

    #Relation
    critere_evaluation: Mapped[Optional['CritereEvaluation']] = relationship('CritereEvaluation', back_populates='note_candidat')
    evaluation_entretien: Mapped[Optional['EvaluationEntretien']] = relationship('EvaluationEntretien', back_populates='note_candidat')
    evaluation_evaluation: Mapped[Optional['EvaluationEvaluation']] = relationship('EvaluationEvaluation', back_populates='note_candidat')


#================================================Schemas Survey=================================================

class Questionnaire(Base):
    __tablename__ = 'questionnaire'
    __table_args__ = (
        ForeignKeyConstraint(['id_entreprise'], ['public.entreprise.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='questionnaire_id_entreprise_fkey'),
        ForeignKeyConstraint(['id_utilisateur'], ['public.utilisateur.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='questionnaire_id_utilisateur_fkey'),
        PrimaryKeyConstraint('id', name='questionnaire_pk'),
        {'comment': 'Table pour stocker les questionnaires destinés aux entretiens',
     'schema': 'survey'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    titre: Mapped[str] = mapped_column(String(255), nullable=False, comment='Titre du questionnaire')
    type_questionnaire: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Technique'::character varying"), comment='Technique, Comportemental, Aptitude, Connaissance métier, Autre')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    id_entreprise: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.entreprise.id', ondelete='SET NULL'), comment='Entreprise propriétaire du questionnaire (null = questionnaire générique)')
    id_utilisateur: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('public.utilisateur.id', ondelete='SET NULL'), comment='Utilisateur propriétaire du questionnaire (null = questionnaire générique)')
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    #Relation
    entreprise: Mapped[Optional['Entreprise']] = relationship('Entreprise', back_populates='questionnaire')
    utilisateur: Mapped[Optional['Utilisateur']] = relationship('Utilisateur', back_populates='questionnaire')
    question: Mapped[list['Question']] = relationship('Question', back_populates='questionnaire')
    questionnaire_entretien: Mapped[list['QuestionnaireEntretien']] = relationship('QuestionnaireEntretien', back_populates='questionnaire')
    questionnaire_evaluation: Mapped[list['QuestionnaireEvaluation']] = relationship('QuestionnaireEvaluation', back_populates='questionnaire')
    reponse: Mapped[list['Reponse']] = relationship('Reponse', back_populates='questionnaire')


class Question(Base):
    __tablename__ = 'question'
    __table_args__ = (
        ForeignKeyConstraint(['id_questionnaire'], ['survey.questionnaire.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='question_id_questionnaire_fkey'),
        PrimaryKeyConstraint('id', name='question_pk'),
        {'comment': "Table pour stocker les questions individuelles d'un questionnaire",
     'schema': 'survey'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_questionnaire: Mapped[str] = mapped_column(String(12), ForeignKey('survey.questionnaire.id', ondelete='CASCADE'), nullable=False)
    numero_question: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    libelle_question: Mapped[str] = mapped_column(Text, nullable=False)
    type_question: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'Texte'::character varying"), comment='Texte, Choix unique, Choix multiples, Oui/Non, Note (1-5), Fichier')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    options_possibles: Mapped[Optional[dict]] = mapped_column(JSONB, comment="Options au format JSON si le type est 'Choix unique' ou 'Choix multiples'")
    reponse_attendue: Mapped[Optional[str]] = mapped_column(Text)

    #Relations
    questionnaire: Mapped['Questionnaire'] = relationship('Questionnaire', back_populates='question')
    reponse: Mapped[list['Reponse']] = relationship('Reponse', back_populates='question')


class Reponse(Base):
    __tablename__ = 'reponse'
    __table_args__ = (
        ForeignKeyConstraint(['id_question'], ['survey.question.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='reponse_id_question_fkey'),
        ForeignKeyConstraint(['id_questionnaire'], ['survey.questionnaire.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='reponse_id_questionnaire_fkey'),
        ForeignKeyConstraint(['id_questionnaire_entretien'], ['talent.questionnaire_entretien.id'], ondelete='CASCADE', onupdate='CASCADE', match='FULL', name='reponse_id_questionnaire_entretien_fkey'),
        ForeignKeyConstraint(['id_questionnaire_evaluation'], ['talent.questionnaire_evaluation.id'], ondelete='SET NULL', onupdate='CASCADE', match='FULL', name='reponse_id_questionnaire_evaluation_fkey'),
        PrimaryKeyConstraint('id', name='reponse_pk'),
        {'comment': 'Table pour stocker les réponses du candidat aux questions du '
                'questionnaire',
     'schema': 'survey'}
    )

    id: Mapped[str] = mapped_column(String(12), primary_key=True, server_default=text("encode(gen_random_bytes(6), 'hex'::text)"))
    id_question: Mapped[str] = mapped_column(String(12), ForeignKey('survey.question.id', ondelete='CASCADE'), nullable=False, comment='Question à laquelle la réponse correspond')
    id_questionnaire: Mapped[str] = mapped_column(String(12), ForeignKey('survey.questionnaire.id', ondelete='CASCADE'), nullable=False, comment='Questionnaire auquel la réponse correspond')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    id_questionnaire_entretien: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.questionnaire_entretien.id', ondelete='CASCADE'), comment='Lien vers questionnaire_entretien')
    id_questionnaire_evaluation: Mapped[Optional[str]] = mapped_column(String(12), ForeignKey('talent.questionnaire_evaluation.id', ondelete='SET NULL'), comment='Lien vers questionnaire_evaluation (une réponse peut être associée à un entretien ou à une évaluation)')
    contenu_reponse: Mapped[Optional[str]] = mapped_column(Text)
    fichier_reponse: Mapped[Optional[str]] = mapped_column(String(255))
    note_reponse: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2), comment='Note attribuée à la réponse (si évaluation numérique)')

    #Relations
    question: Mapped['Question'] = relationship('Question', back_populates='reponse')
    questionnaire: Mapped['Questionnaire'] = relationship('Questionnaire', back_populates='reponse')
    questionnaire_entretien: Mapped[Optional['QuestionnaireEntretien']] = relationship('QuestionnaireEntretien', back_populates='reponse')
    questionnaire_evaluation: Mapped[Optional['QuestionnaireEvaluation']] = relationship('QuestionnaireEvaluation', back_populates='reponse')


#==============================================Schemas Roadmap======================================================



