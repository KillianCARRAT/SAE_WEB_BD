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

DELIMITER |

CREATE FUNCTION check_nbr_par(nDateR DATETIME, nIdM INT)
RETURNS BOOLEAN
DETERMINISTIC -- Je l'ai mis parce que monterminal m'a dit de le mettre pour que ca fonctionne
BEGIN
    DECLARE nb_participants INT;

    -- Compter les participants qui sont déjà dans le cours
    SELECT COUNT(*) INTO nb_participants
    FROM RESERVATION
    WHERE dateR = nDateR
      AND idM = nIdM;

    RETURN nb_participants >= 10;
END|

DELIMITER ;

DELIMITER |

CREATE FUNCTION check_repos(nIdP INT, 
    nDateR DATETIME, nDuree INT)
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE finNewRes DATETIME;
    DECLARE debTempsDern1 DATETIME;
    DECLARE finTempsDern1 DATETIME;
    DECLARE debTempsDern2 DATETIME;
    DECLARE finTempsDern2 DATETIME;
    DECLARE totalHeuresConsecutives INT;

    -- Calcul de la fin du cours qu'on veut ajouter
    SET finNewRes = nDateR + INTERVAL nDuree HOUR;

    -- Récupère l'avant dernière réservation
    SELECT dateR, dateR + INTERVAL duree HOUR INTO debTempsDern1, finTempsDern1
    FROM RESERVATION
    WHERE idP = nIdP
    ORDER BY dateR DESC
    LIMIT 1, 1;

    -- Récupère la dernière réservation
    SELECT dateR, dateR + INTERVAL duree HOUR INTO debTempsDern2, finTempsDern2
    FROM RESERVATION
    WHERE idP = nIdP
    ORDER BY dateR DESC
    LIMIT 1;

    -- Calcul par défaut du dernier cours
    SET totalHeuresConsecutives = 0;

    IF finTempsDern1 IS NOT NULL AND debTempsDern2 IS NOT NULL THEN
        SET totalHeuresConsecutives = TIMESTAMPDIFF(HOUR, debTempsDern2, finTempsDern2);

        -- Si les réservations sont consécutives
        IF TIMESTAMPDIFF(HOUR, finTempsDern1, debTempsDern2) < 1 THEN
            SET totalHeuresConsecutives = TIMESTAMPDIFF(HOUR, debTempsDern1, finTempsDern2);
        END IF;
    END IF;

    RETURN totalHeuresConsecutives + nDuree > 2 
            AND TIMESTAMPDIFF(HOUR, finTempsDern2, nDateR) < 1;
END |

DELIMITER ;

DELIMITER |

CREATE FUNCTION check_capa(nIdA INT, nIdP INT)
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE capacite_poney INT;
    DECLARE poids_adherent INT;

    -- Capacité poney
    SELECT capacite INTO capacite_poney
    FROM PONEY
    WHERE idP = nIdP;

    -- Poid adhérent
    SELECT poid INTO poids_adherent
    FROM ADHERANT
    WHERE idA = nIdA;

    RETURN poids_adherent > capacite_poney;
END|

DELIMITER ;

DELIMITER |

CREATE FUNCTION dispo_poney(p_idP INT, p_dateR DATETIME) 
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    -- Vérifie si le poney est déjà réservé à cette date et heure
    IF EXISTS (
        SELECT 1
        FROM RESERVATION
        WHERE idP = p_idP
        AND dateR = p_dateR
    ) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END |

DELIMITER ;

DELIMITER |

CREATE FUNCTION dispo_moniteur(p_idM INT, p_dateR DATETIME) 
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    -- Vérifie si le moniteur est déjà réservé à cette date et heure
    IF EXISTS (
        SELECT 1
        FROM RESERVATION
        WHERE idM = p_idM
        AND dateR = p_dateR
    ) THEN
        RETURN TRUE;
    ELSE 
        RETURN FALSE;
    END IF;
END |

DELIMITER ;

DELIMITER |

CREATE TRIGGER check_resa
BEFORE INSERT ON RESERVATION
FOR EACH ROW
BEGIN
    -- Comparer le poids de l'adhérent avec la capacité du poney
    IF check_capa(NEW.idA, NEW.idP) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "Le poid de l'adhérent est supérieur à la capacité du poney";
    END IF;

    -- Vérification de la disponibilité d'un poney
    IF dispo_poney(NEW.idP, NEW.dateR) THEN 
        SIGNAL SQLSTATE '45000' 
            set MESSAGE_TEXT = 'Ce poney est déjà réservé à cette date et heure.';
    END IF;

    -- Vérifie le nombre de participant si le cours est collectif
    IF NEW.individuel = FALSE THEN
        -- Appel de la fonction pour vérifier le nombre de participants
        IF check_nbr_par(NEW.dateR, NEW.idM) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Il y a déjà trop de participants à ce cours.';
        END IF;
    ELSE
        -- Vérification de la disponibilité d'un moniteur
        IF dispo_moniteur(NEW.idM, NEW.dateR) THEN 
            SIGNAL SQLSTATE '45000' 
                set MESSAGE_TEXT = 'Ce moniteur est déjà réservé à cette date et heure.';
        END IF;
    END IF;


    -- Vérifie si le poney a travaillé plus de 2 heures
    IF check_repos(NEW.idP, NEW.dateR, NEW.duree) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Le poney ne peut pas travailler plus de 2 heures consécutives.';
    END IF;

END|

DELIMITER ;
