from cs50 import SQL
# from short import dict

db = SQL("sqlite:///words.db")


WORD_TO_PLAY = "lops"
LEN_WORD_TO_PLAY = len(WORD_TO_PLAY)

order_this_word = "".join(sorted(WORD_TO_PLAY))
print("word: ", WORD_TO_PLAY)
print("lenght: ", LEN_WORD_TO_PLAY)
print("reodered: ", order_this_word)
temp_dict = []
final_dict = []

def word_to_dict(word):
    global temp_dict
    if len(word) == 3:
        return
    else:
        for i in range(len(word)):
            attempt = word[:i] + word[i + 1:]
            if attempt not in temp_dict:
                temp_dict.append(attempt)
            word_to_dict(attempt)

word_to_dict(order_this_word)
print(sorted(temp_dict))

for item in temp_dict:
    result = db.execute("SELECT word FROM words WHERE order_letters = ?", item)
    if len(result) == 1:
        final_dict.append(result[0]["word"])
    elif len(result) > 1:
        for word in result:
            final_dict.append(word["word"])


print(final_dict)
print("Words: ", len(final_dict))