DROP TABLE RESERVATION;
DROP TABLE ADHERANT;
DROP TABLE MONITEUR;
DROP TABLE PONEY;

CREATE TABLE ADHERANT(
    ipA int PRIMARY KEY,
    nomA varchar(20),
    prenomA varchar(20),
    telA varchar(10) unique,
    poid int
)

CREATE TABLE MONITEUR(
    idM int PRIMARY KEY,
    nomM varchar(20),
    prenomM varchar(20),
    telM varchar(10) unique
)

CREATE TABLE PONEY(
    idP int PRIMARY KEY,
    nomP varchar(20),
    capacite int,
)

CREATE TABLE RESERVATION(
    dateR date,
    idA int,
    idP int,
    idM int,
    duree int,
    individuel boolean,
    FOREIGN KEY idA REFERENCE ADHERANT(idA),
    FOREIGN KEY idM REFERENCE MONITEUR(idM),
    FOREIGN KEY idP REFERENCE PONEY(idP),
    PRIMARY KEY (dateR, idA, idP, idM),
)