BEGIN TRANSACTION;

DROP TABLE IF EXISTS Replies;
DROP TABLE IF EXISTS Questions;

CREATE TABLE Questions (
  id INTEGER PRIMARY KEY, 
  author VARCHAR(50), 
  title VARCHAR(200), 
  body TEXT, 
  time datetime, 
  tags VARCHAR(200)
);

CREATE TABLE Replies (
	id INTEGER PRIMARY KEY,
	author VARCHAR(50),
	body TEXT,
	time DATETIME,
	question_id INTEGER,
	
	FOREIGN KEY (question_id) REFERENCES Questions(id)
);

INSERT INTO Questions VALUES(1,'pepe','Listas en Python','Me gustaria saber como construir listas en Python','2013-06-14 12:00:42','listas, Python');
INSERT INTO Questions VALUES(2,'ana','Diccionarios','Que es exactamente un diccionario? Como se construyen en Python?','2012-03-19 11:54:23','diccionarios, Python, programar');
INSERT INTO Questions VALUES(3,'pepe','Mejor editor para programar','Vim o Emacs?','2015-12-27 16:40:43','Editor, programar');

INSERT INTO Replies VALUES(1,'josefa','Con corchetes!!! Ejemplos de listas son [1,2,3] y [True, False, 3.0]','2015-12-27 15:25:17',1);
INSERT INTO Replies VALUES(2,'josefa','Se me olvido comentar que tambien se generan con el constructor list()','2017-12-27 15:26:32',1);
INSERT INTO Replies VALUES(3,'don_troll','pa k kieres saber eso jaja saludos','2025-08-01 22:33:44',2);

COMMIT;
