-- Vérification capcité/poid
-- Poney avec une capacité de 100 kg
INSERT INTO PONEY (idP, nomP, capacite) VALUES (10000, 'Tornado', 100);

-- Adhérent avec un poids de 80 kg
INSERT INTO ADHERANT (idA, nomA, prenomA, telA, poid) VALUES (10000, 'Dupont', 'Jean', '0123456789', 80);

-- Réservation valide
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (1, '2024-11-21 10:00:00', 10000, 10000, 1, 1, TRUE);

-- Adhérent avec un poids de 120 kg
INSERT INTO ADHERANT (idA, nomA, prenomA, telA, poid) VALUES (200000, 'Martin', 'Paul', '0123456780', 120);

-- Réservation non valide
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (2, '2024-11-22 10:00:00', 200000, 10000, 1, 1, TRUE);


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


-- INSERT pour teste de poid/capacite
-- Vérification non valide : 11e participant pour le même cours collectif 
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel)
VALUES (11, '2024-11-21 14:00:00', 11, 1, 1, 1, FALSE);

-- Poney avec une capacité de 100 kg
INSERT INTO PONEY (idP, nomP, capacite) VALUES (10000, 'Tornado', 100);

-- Adhérent avec un poids de 80 kg
INSERT INTO ADHERANT (idA, nomA, prenomA, telA, poid) VALUES (10000, 'Dupont', 'Jean', '0123456789', 80);

-- Réservation valide
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (1, '2024-11-21 10:00:00', 10000, 10000, 1, 1, TRUE);

-- Adhérent avec un poids de 120 kg
INSERT INTO ADHERANT (idA, nomA, prenomA, telA, poid) VALUES (200000, 'Martin', 'Paul', '0123456780', 120);

-- Réservation non valide
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (2, '2024-11-22 10:00:00', 200000, 10000, 1, 1, TRUE);


-- Respect des temps de repos
-- Ajouter une réservation valide
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (1, '2024-11-21 10:00:00', 1, 1, 1, 1, TRUE);

-- Reservation valide
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (2, '2024-11-21 11:00:00', 2, 1, 1, 1, TRUE);

-- Reservation non valide, le poney a besoin de 1 heures de repos
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (3, '2024-11-21 12:00:00', 2, 1, 1, 1, TRUE);

-- Reservation valide : le poney a eu 1 heures de repos
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (4, '2024-11-21 13:00:00', 2, 1, 1, 2, TRUE);

-- Réservation non valide : le poney doit avoir 1 heure de repos
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (5, '2024-11-21 15:00:00', 3, 1, 1, 1, TRUE);

-- Validité diposbilité poney et moniteur
-- Insertion valide
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (1, '2024-11-21 10:00:00', 1, 1, 1, 2, TRUE);

-- Vérification : échouer pour insertion d'un poney
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (2, '2024-11-21 10:00:00', 2, 1, 2, 1, TRUE);

-- Vérification : échouer pour insertion d'un moniteur
INSERT INTO RESERVATION (idR, dateR, idA, idP, idM, duree, individuel) 
VALUES (3, '2024-11-21 10:00:00', 3, 2, 1, 1, TRUE);