CREATE TABLE ROLE (
    id_role INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE UTILISATEUR (
    id_utilisateur INTEGER PRIMARY KEY,
    nom_utilisateur TEXT,
    prenom_utilisateur TEXT,
    tel_utilisateur TEXT,
    poids_utilisateur TEXT,
    email_utilisateur TEXT,
    mdp_utilisateur TEXT,
    role_id INTEGER,
    active BOOLEAN DEFAULT TRUE,
    fs_uniquifier VARCHAR(255) UNIQUE,
    FOREIGN KEY (role_id) REFERENCES ROLE (id_role)
);

CREATE TABLE CONTACT (
    id_contact INTEGER PRIMARY KEY,
    concerne TEXT,
    sujet TEXT,
    contenu TEXT,
    id_utilisateur INTEGER,
    FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR (id_utilisateur)
);

CREATE TABLE PONEY (
    id_poney INTEGER PRIMARY KEY,
    nom_poney TEXT,
    capacite_poney INTEGER
);

CREATE TABLE RESERVATION (
    id_reservation INTEGER PRIMARY KEY,
    id_poney INTEGER,
    id_utilisateur INTEGER,
    id_seance INTEGER,
    FOREIGN KEY (id_poney) REFERENCES PONEY (id_poney),
    FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR (id_utilisateur),
    FOREIGN KEY (id_seance) REFERENCES SEANCE (id_seance)
);

CREATE TABLE SEANCE (
    id_seance INTEGER PRIMARY KEY,
    annee_seance INTEGER,
    semaine_seance INTEGER,
    jour_seance INTEGER,
    heure_debut_seance TIME,
    heure_fin_seance TIME,
    nb_places_seance INTEGER,
    active BOOLEAN DEFAULT TRUE,
    moniteur_id INTEGER,
    FOREIGN KEY (moniteur_id) REFERENCES UTILISATEUR (id_utilisateur)
);
