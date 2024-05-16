DROP TABLE IF EXISTS dispositivos;

CREATE TABLE dispositivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitante TEXT NOT NULL,
    ultimoping DATETIME NOT NULL
);
