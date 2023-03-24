CREATE TABLE IF NOT EXISTS words (
    word TEXT(46) NOT NULL UNIQUE,
    number_letters SMALLINT UNSIGNED NOT NULL,
    possible_words SMALLINT UNSIGNED,
    order_letters TEXT(46) NOT NULL
);

SELECT word FROM words WHERE add_by_user="added_by_user";
SELECT word FROM words WHERE word="oca";

DELETE FROM words;
DELETE FROM words WHERE number_letters < 3;

ALTER TABLE words
ADD add_by_user TEXT(13);

ALTER TABLE words
DROP COLUMN possible_words;

DROP TABLE words;

SELECT COUNT(word) FROM words;
SELECT COUNT(word) FROM words WHERE number_letters = 3;


CREATE TABLE words (
    word TEXT(46) NOT NULL UNIQUE,
    number_letters SMALLINT UNSIGNED NOT NULL,
    order_letters TEXT(46) NOT NULL,
    add_by_user TEXT(13));