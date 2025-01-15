-- Table ROLE
CREATE TABLE ROLE (
    id_role INT PRIMARY KEY,
    name TEXT
);

-- Table UTILISATEUR
CREATE TABLE UTILISATEUR (
    id_utilisateur INT PRIMARY KEY,
    nom_utilisateur TEXT,
    prenom_utilisateur TEXT,
    tel_utilisateur TEXT,
    poids_utilisateur TEXT,
    email_utilisateur TEXT,
    mdp_utilisateur TEXT,
    role_id INT,
    active BOOLEAN DEFAULT TRUE,
    fs_uniquifier VARCHAR(255) UNIQUE,
    FOREIGN KEY (role_id) REFERENCES ROLE(id_role)
);

-- Table CONTACT
CREATE TABLE CONTACT (
    id_contact INT PRIMARY KEY,
    concerne TEXT,
    sujet TEXT,
    contenu TEXT,
    id_utilisateur INT,
    FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR(id_utilisateur)
);

-- Table PONEY
CREATE TABLE PONEY (
    id_poney INT PRIMARY KEY,
    nom_poney TEXT,
    capacite_poney INT
);

-- Table RESERVATION
CREATE TABLE RESERVATION (
    id_reservation INT PRIMARY KEY,
    id_poney INT,
    id_utilisateur INT,
    FOREIGN KEY (id_poney) REFERENCES PONEY(id_poney),
    FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR(id_utilisateur)
);

-- Table RESERVATION_UTILISATEUR
CREATE TABLE RESERVATION_UTILISATEUR (
    id_utilisateur INT,
    id_reservation INT,
    PRIMARY KEY (id_utilisateur, id_reservation),
    FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR(id_utilisateur),
    FOREIGN KEY (id_reservation) REFERENCES RESERVATION(id_reservation)
);

-- Table RESERVATION_SEANCE
CREATE TABLE RESERVATION_SEANCE (
    id_seance INT,
    id_reservation INT,
    PRIMARY KEY (id_seance, id_reservation),
    FOREIGN KEY (id_seance) REFERENCES SEANCE(id_seance),
    FOREIGN KEY (id_reservation) REFERENCES RESERVATION(id_reservation)
);

-- Table SEANCE
CREATE TABLE SEANCE (
    id_seance INT PRIMARY KEY,
    annee_seance INT,
    semaine_seance INT,
    jour_seance INT,
    heure_debut_seance TIME,
    heure_fin_seance TIME,
    nb_places_seance INT,
    active BOOLEAN DEFAULT TRUE,
    moniteur_id INT,
    FOREIGN KEY (moniteur_id) REFERENCES UTILISATEUR(id_utilisateur)
);
