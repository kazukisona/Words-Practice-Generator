DROP TABLE if EXISTS words;
CREATE TABLE words (
    id integer PRIMARY KEY autoincrement,
    word text not null,
    meaning text not null
);