# Words Of Game
#### Video Demo: <https://youtu.be/mB8wh3t-l7I>
#### Description:

**"Words Of Game"** is an engaging word game that challenges players to unscramble a set of letters to form as many words as possible. The game provides players with a random or chosen word, and their goal is to rearrange the letters to form words that are at least three letters long.

Players can enter their guesses into a text box or using images of letters, and the game will check to see if their guesses are valid words. The game can also provide hints to help players who are struggling.

"Words Of Game" is a fun and educational game that can help players build their vocabulary and improve their spelling skills. It is suitable for players of all ages and can be played alone or with friends. With its simple and addictive gameplay, "Words Of Game" is sure to provide hours of entertainment for word lovers everywhere!

#### Usage:

There are 3 main buttons on the main screen:

[![menu.png](https://i.postimg.cc/v87XxNKz/menu.png)](https://postimg.cc/Bt62dM4L)
* **New game /index** - where we are begin:
    * type the word (4-9 letters) or
    * choose number of letter to get random word and click ***Play!***
* **All words /all**:
    * If you want to check all possible words that you can form, click ***All words*** and type the word that you are interested in: */all*
* **Added by user /users**:
    * You can add words and delete added words as well. The list of all added words you can get clicking ***Added by user***.


#### /game:

After you have chosen a word in any available way, you will discover yourself directly on the game page.

Here are the main items on it:
1. **Key word** made of images of every letter
2. **Guessword** with the check to exclude repetition of letters and ability to delete letters. If there is no word in current database, game asks you if it should be added.
3. **Input and check** - you can type word or click letters as well
4. **Guessword list** and **progress bar** - this is your game process
5. **Hints** - you can choose hint as one word, or watch the list of all remaining words

[![game.png](https://i.postimg.cc/gkHd1xRy/game.png)](https://postimg.cc/JG09k4pt)

I used:
* **SQL** - for searching word, choosing the random word, adding word, etc.
* **Python** - for operating with SQL database; for operating with GET and POST methods in all html files.
* **Flask** - for using blocks and GET and POST methods in all html files.
* **Jinja** - to "convert" text to image with the help of loops and variables (later about it), and for changing output depending on the value of variables with if blocks.
* **JavaScript** - to change the properties of objects, to choose or delete letters with full check to exclude repetition of them.

*The example of adding word:*

[![add-word.png](https://i.postimg.cc/pd4j61Qh/add-word.png)](https://postimg.cc/GBP9BK5d)

*The example of finding all the words:*

[![win.png](https://i.postimg.cc/zD6gDQ4x/win.png)](https://postimg.cc/QVgt0f87)


#### /all:
At this page you could check number of possible words and delete those what has been added before by user:

[![all.png](https://i.postimg.cc/KYq3CcL8/all.png)](https://postimg.cc/4Kc39gBD)


#### /users:
At this page you could check all the words that has been added before by user and delete the if it's necessary:
[![added.png](https://i.postimg.cc/zvnCmZ82/added.png)](https://postimg.cc/K38kLWKt)

#### Something interesting:
In the course of writing the project I ran into a couple of problems that I successfully solved:

**The first one** and the main one was the fast way to find all possible words that we can form from the original one.
I did it this way:
1. I created the database from the dictionary, that contain words with number of letters from 3 to 9,
2. Then I added one more column with the same letters of the word but **in an alphabetical order**,
<code>CREATE TABLE words (
    word TEXT(46) NOT NULL UNIQUE,
    number_letters SMALLINT UNSIGNED NOT NULL,
    order_letters TEXT(46) NOT NULL,
    add_by_user TEXT(13));</code>
*Steps 1 and 2 solution is in the folder **preparatory_stage***
3. I made temporary list of all possible letter's combinations (also in an alphabetical order) without permutation: recursive function <code>def word_to_dict(word)</code>
4. Then I wrote a loop for looking each item in database <code>def possible_words()</code> with the same alphabetical order and add search word to the new list

And at the end we have the list with all possible words that we can form from the original one

**The second one** was to make a check to exclude repetition of letters while guessing the word.
I used regular expression to fix it, but I also used letters as a name of files with images (<code>id="{{ letter }}" src="/static/letters/{{ letter }}.png"</code>), and as "id" to change its properties (while adding or deleting a letter from the guessword). We also can find 2 or 3 repeating letters in word (for example: l**i**m**i**tat**i**on). So, with the help of <code>.forEach()</code>, comparing each id and propeties I finally made it works good.
[![game.gif](https://i.postimg.cc/NFPk5X25/game.gif)](https://postimg.cc/wRLmr7Vp)

**The last one** was to find the way to change size of images depending on the size of the window in order pages not to look ugly on small screen or mobile devices. I decided it with the help of CSS custom properties (variables).

*Examples of screen images on different devices:*
[![ipad-mini.png](https://i.postimg.cc/prvPHH4G/ipad-mini.png)](https://postimg.cc/DJx9rt2L)
[![Galaxy.png](https://i.postimg.cc/j5RYCXqv/Galaxy.png)](https://postimg.cc/wt4GGDms)
[![iphonexr.png](https://i.postimg.cc/fyrbxFJM/iphonexr.png)](https://postimg.cc/GTvrRXFf)


#### and a little P.S.:
All the images of letters I drew myself, and it's a great achivement for me😂
Thank you for reading, and join it!