DROP TABLE IF EXISTS dispositivos;

CREATE TABLE dispositivos (
    visitante TEXT PRIMARY KEY NOT NULL,
    ultimoping DATETIME NOT NULL
);
