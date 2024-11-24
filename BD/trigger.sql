DROP FUNCTION IF EXISTS check_nbr_par;
DROP FUNCTION IF EXISTS check_capa;
DROP FUNCTION IF EXISTS dispo_moniteur;
DROP FUNCTION IF EXISTS dispo_poney;
DROP FUNCTION IF EXISTS check_repos;

DELIMITER |

CREATE FUNCTION check_nbr_par(nDateR DATETIME, nIdP INT, nIdM INT)
RETURNS BOOLEAN
DETERMINISTIC -- Je l'ai mis parce que monterminal m'a dit de le mettre pour que ca fonctionne
BEGIN
    DECLARE nb_participants INT;

    -- Compter les participants qui sont déjà dans le cours
    SELECT COUNT(*) INTO nb_participants
    FROM RESERVATION
    WHERE dateR = nDateR
      AND idP = nIdP
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

CREATE TRIGGER check_poid_capacite
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
        IF check_nbr_par(NEW.dateR, NEW.idP, NEW.idM) THEN
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

-- 10 participants
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel)
VALUES (1, '2024-11-21 14:00:00', 1, 1, 1, 1, FALSE),
        (2, '2024-11-21 14:00:00', 2, 2, 1, 1, FALSE),
        (3, '2024-11-21 14:00:00', 3, 3, 1, 1, FALSE),
        (4, '2024-11-21 14:00:00', 4, 4, 1, 1, FALSE),
        (5, '2024-11-21 14:00:00', 5, 5, 1, 1, FALSE),
        (6, '2024-11-21 14:00:00', 6, 27, 1, 1, FALSE),
        (7, '2024-11-21 14:00:00', 7, 7, 1, 1, FALSE),
        (8, '2024-11-21 14:00:00', 8, 8, 1, 1, FALSE),
        (9, '2024-11-21 14:00:00', 9, 9, 1, 1, FALSE),
        (10, '2024-11-21 14:00:00', 10, 10, 1, 1, FALSE);

-- Insertion invalide pas plus de 10 participants
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel)
VALUES (11, '2024-11-21 14:00:00', 11, 11, 1, 1, FALSE);