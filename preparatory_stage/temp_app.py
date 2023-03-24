from cs50 import SQL
from large import dict

db = SQL("sqlite:///words.db")

words = dict()
lenght = len(words)

for word in words:
    letters = len(word)
    if "'" not in word and 2 < letters < 10:
        order = "".join(sorted(word))
        db.execute("INSERT INTO words (word, number_letters, order_letters) VALUES (?, ?, ?)", word, letters, order)
