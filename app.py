from flask import Flask, render_template, request
from cs50 import SQL
import re


# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///words.db")

WORD_TO_PLAY = ""
LEN_WORD_TO_PLAY = 0
TEMP_DICT = []
FINAL_LIST = []
FINAL_DICT = {}
USER_LIST = []
REST_LIST = []
TEMP_WORD = ""
pattern = re.compile("^[a-zA-Z]+$")


def choose_word(lenght):
    """Choose random word."""
    word = db.execute("SELECT * FROM words WHERE number_letters=? ORDER BY RANDOM() LIMIT 1", lenght)[0]["word"]
    return word


def check_word(user_word):
    """Check user's word."""
    if db.execute("SELECT * FROM words WHERE word=?", user_word) == []:
        return False
    else:
        word = db.execute("SELECT * FROM words WHERE word=?", user_word)[0]["word"]
        return word


def word_to_dict(word):
    """Make all possible combinations without permutation."""
    global TEMP_DICT
    if len(word) == 3:
        return
    else:
        for i in range(len(word)):
            attempt = word[:i] + word[i + 1:]
            if attempt not in TEMP_DICT:
                TEMP_DICT.append(attempt)
            word_to_dict(attempt)


def possible_words():
    """Check for match words with a help of def word_to_dict(). List for play."""
    order_this_word = "".join(sorted(WORD_TO_PLAY))
    global TEMP_DICT, FINAL_LIST, REST_LIST
    TEMP_DICT = []
    word_to_dict(order_this_word)
    TEMP_DICT.append(order_this_word)

    # matching database search
    for item in TEMP_DICT:
        result = db.execute("SELECT word FROM words WHERE order_letters = ? AND NOT word = ?", item, WORD_TO_PLAY)
        # in case of 1 word
        if len(result) == 1:
            FINAL_LIST.append(result[0]["word"])
        # in case of more than 1 word
        elif len(result) > 1:
            for word in result:
                FINAL_LIST.append(word["word"])
    FINAL_LIST.sort()
    REST_LIST = FINAL_LIST.copy()
    # print(FINAL_LIST)
    return


def possible_words_dict():
    """Check for match words with a help of def word_to_dict(). Dict for /all."""
    order_this_word = "".join(sorted(WORD_TO_PLAY))
    global TEMP_DICT, FINAL_DICT, REST_LIST
    TEMP_DICT = []
    word_to_dict(order_this_word)
    TEMP_DICT.append(order_this_word)

    # matching database search
    for item in TEMP_DICT:
        result = db.execute("SELECT word, add_by_user FROM words WHERE order_letters = ? AND NOT word = ?", item, WORD_TO_PLAY)
        # in case of 1 word
        if len(result) == 1:
            FINAL_DICT[result[0]["word"]] = result[0]["add_by_user"]
        # in case of more than 1 word
        elif len(result) > 1:
            for word in result:
                FINAL_DICT[word["word"]] = word["add_by_user"]
    FINAL_DICT = dict(sorted(FINAL_DICT.items()))
    REST_LIST = FINAL_DICT.copy()
    return


@app.route("/", methods=["GET", "POST"])
def index():
    global WORD_TO_PLAY, LEN_WORD_TO_PLAY, USER_LIST, FINAL_LIST, REST_LIST
    USER_LIST = []
    FINAL_LIST = []
    REST_LIST = []

    if request.method == "POST":
        # request word or lenght
        word = request.form.get("word")
        len_word = request.form.get("lenght_word")

        # checking for input
        if word == "" and len_word == "choose number of letters":
            return render_template("index.html")

        elif word == "":
            # random word + check for case with no possible words
            while FINAL_LIST == []:
                word = choose_word(len_word)
                WORD_TO_PLAY = word
                LEN_WORD_TO_PLAY = int(len_word)
                possible_words()
            return render_template("game.html", word_to_play=word, len_word_to_play=len_word, table=USER_LIST, table_lenght=len(USER_LIST), answer=FINAL_LIST, all_lenght=len(FINAL_LIST))

        elif (len_word == "choose number of letters" or len_word is None) and word is not None:
            # call for function to check user's word
            word = word.lower()
            len_word = len(word)
            # check for symbols and lenght
            if not pattern.search(word) or len_word > 9 or len_word < 4:
                message = "Four to nine letters, not numbers or other symbols!"
                return render_template("index.html", message=message)

            checked_word = check_word(word)

            if checked_word:
                # ask user to add the word or not
                WORD_TO_PLAY = checked_word
                LEN_WORD_TO_PLAY = int(len_word)
                possible_words()
                return render_template("game.html", word_to_play=checked_word, len_word_to_play=len_word, table=USER_LIST, table_lenght=len(USER_LIST), answer=FINAL_LIST, all_lenght=len(FINAL_LIST))
            else:
                WORD_TO_PLAY = word
                LEN_WORD_TO_PLAY = len(word)
                return render_template("index.html", new_word=word)

        else:
            # add new word into database
            if request.form.get("add_word") == "add":
                order = "".join(sorted(WORD_TO_PLAY))
                db.execute("INSERT INTO words (word, number_letters, order_letters, add_by_user) VALUES (?, ?, ?, ?)", WORD_TO_PLAY, LEN_WORD_TO_PLAY, order, "added_by_user")
                possible_words()
                return render_template("game.html", word_to_play=WORD_TO_PLAY, len_word_to_play=LEN_WORD_TO_PLAY, table=USER_LIST, table_lenght=len(USER_LIST), answer=FINAL_LIST, all_lenght=len(FINAL_LIST))
            else:
                return render_template("index.html")

    elif request.method == "GET":
        return render_template("index.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    global WORD_TO_PLAY, LEN_WORD_TO_PLAY, FINAL_LIST, TEMP_WORD, REST_LIST
    guess_word = request.form.get("guessWord")
    if request.method == "POST":
        if guess_word is not None:
            # in case of repeat
            if guess_word in USER_LIST:
                message = "Already got it!"
            # in case of the same word
            elif guess_word == WORD_TO_PLAY:
                message = "It's the same word 😉"
            # in case of mathing
            elif guess_word in FINAL_LIST:
                USER_LIST.append(guess_word)
                REST_LIST.remove(guess_word)
                message = "Right!"
            # in case of too short
            elif len(guess_word) < 3:
                message = "At least three letters!"
            # in case of unknown word
            else:
                message = "Wrong!"
                TEMP_WORD = guess_word
            return render_template("game.html", word_to_play=WORD_TO_PLAY, len_word_to_play=LEN_WORD_TO_PLAY, table=USER_LIST, table_lenght=len(USER_LIST), message=message, new_word=TEMP_WORD, answer=REST_LIST, answer_lenght=len(REST_LIST), all_lenght=len(FINAL_LIST))

        elif request.form.get("add_word") == "add":
            # add new word into database
            USER_LIST.append(TEMP_WORD)
            lenght = len(TEMP_WORD)
            order = "".join(sorted(TEMP_WORD))
            message = "Word added!"
            db.execute("INSERT INTO words (word, number_letters, order_letters, add_by_user) VALUES (?, ?, ?, ?)", TEMP_WORD, lenght, order, "added_by_user")
            return render_template("game.html", word_to_play=WORD_TO_PLAY, len_word_to_play=LEN_WORD_TO_PLAY, table=USER_LIST, table_lenght=len(USER_LIST), message=message, answer=REST_LIST, answer_lenght=len(REST_LIST), all_lenght=len(FINAL_LIST))

        elif request.form.get("add_word") == "no":
            return render_template("game.html", word_to_play=WORD_TO_PLAY, len_word_to_play=LEN_WORD_TO_PLAY, table=USER_LIST, table_lenght=len(USER_LIST), answer=REST_LIST, answer_lenght=len(REST_LIST), all_lenght=len(FINAL_LIST))

    else:
        return render_template("game.html", word_to_play=WORD_TO_PLAY, len_word_to_play=LEN_WORD_TO_PLAY, table=USER_LIST, table_lenght=len(USER_LIST), answer=REST_LIST, answer_lenght=len(REST_LIST), all_lenght=len(FINAL_LIST))


@app.route("/all", methods=["GET", "POST"])
def all():
    global WORD_TO_PLAY, FINAL_DICT
    WORD_TO_PLAY = ""
    option = request.form.get("action")
    if request.method == "POST":
        if option == "check":
            FINAL_DICT = {}
            word = request.form.get("infoWord")
            WORD_TO_PLAY = word.lower()
            # print(WORD_TO_PLAY)
            # check for symbols and lenght
            if not pattern.search(word) or len(word) > 9 or len(word) < 4:
                message = "Four to nine letters, not numbers or other symbols!"
                return render_template("all.html", message=message, all_lenght=len(FINAL_DICT))

            # all words
            checked_word = check_word(WORD_TO_PLAY)
            if checked_word:
                message = "Here it is!"
                # update FINAL_DICT
                possible_words_dict()
                return render_template("all.html", word=WORD_TO_PLAY, message=message, table=FINAL_DICT, all_lenght=len(FINAL_DICT))
            else:
                message = "Can't find this word"
                FINAL_DICT = {}
                return render_template("all.html", word=WORD_TO_PLAY, message=message, all_lenght=len(FINAL_DICT))
        else:
            # delete chosen word
            db.execute("DELETE FROM words WHERE word = ?", option)
            message = f"{option} deleted"
            FINAL_DICT.pop(option)
            return render_template("all.html", word=WORD_TO_PLAY, message=message, table=FINAL_DICT, all_lenght=len(FINAL_DICT))

    else:
        return render_template("all.html", word=WORD_TO_PLAY, all_lenght=len(FINAL_DICT))


@app.route("/users", methods=["GET", "POST"])
def users():
    option = request.form.get("action")
    message = ""
    if request.method == "POST" and option is not None:
        # delete chosen word
        db.execute("DELETE FROM words WHERE word = ?", option)
        message = f"{option} deleted"

    FINAL_DICT = db.execute("SELECT word, add_by_user FROM words WHERE add_by_user = ? ORDER BY word", "added_by_user")
    return render_template("users.html", table=FINAL_DICT, message=message, all_lenght=len(FINAL_DICT))
