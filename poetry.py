# markovify is used to make the markov chains that generate the lines
# for more, visit: https://github.com/jsvine/markovify
import markovify
# the natural language toolkit is used to check rhymes here but can be used for many things.
# visit their website for more: http://www.nltk.org/
import nltk
import string

translator = str.maketrans(
    {key: None for key in string.punctuation})  # this line is used later to strip a string of punctuation
# this block establishes the corpus for the markov chain
# I've used shakespeares sonnets but any text file can be used so long as it is in the same directory
with open("shakespeare.txt") as corpus_text:
    corpus = corpus_text.read()

model = markovify.NewlineText(corpus)
again = True


# returns the rhymes of a given word
# stolen from stack overflow http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)


# uses the rhyme function to check if words rhyme
# also stolen from stack overflow http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
def doTheyRhyme(word1, word2):
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find(word2) == len(word1) - len(word2):
        return False
    if word2.find(word1) == len(word2) - len(word1):
        return False

    return word1 in rhyme(word2, 1)


# returns a line of poetry that is not a blank line
# not stolen from stack overflow
def make_valid_line():
    improper = True
    rhyme = ""
    line = ""
    while improper:
        line = model.make_sentence()
        try:  # try except is used here because the program crashes if rsplit is used on an empty line
            rhyme = line.rsplit(None, 1)[-1]
            rhyme = rhyme.translate(translator)
            improper = False
        except:
            improper = True
    valid_line = (line, rhyme)
    return valid_line


# makes a stanza of a given length using ABAB CDCD... rhyme scheme
# also not stolen from stack overflow
def make_stanza(lines):
    stanza = []
    a = ""
    b = ""
    a2 = ""
    b2 = ""
    for q in range(round(lines / 4)):
        verse = make_valid_line()
        a = verse[1]
        stanza.append(verse[0])

        verse = make_valid_line()
        b = verse[1]
        stanza.append(verse[0])

        for p in range(2):
            if p == 0:
                verse = make_valid_line()
                a2 = verse[1]
                while not doTheyRhyme(a, a2):
                    verse = make_valid_line()
                    a2 = verse[1]
                if doTheyRhyme(a2, a):
                    stanza.append(verse[0])
            else:
                verse = make_valid_line()
                b2 = verse[1]
                while not doTheyRhyme(b2, b):
                    verse = make_valid_line()
                    b2 = verse[1]
                if doTheyRhyme(b, b2):
                    stanza.append(verse[0])
    return stanza


def make_rhyming_couplet():
    couplet = []
    a = ""
    b = ""

    line = make_valid_line()
    a = line[1]
    couplet.append(line[0])

    line = make_valid_line()  # this piece is necessary to make the while loop run at least once
    b = line[1]

    while not doTheyRhyme(a, b):
        line = make_valid_line()
        b = line[1]
        if doTheyRhyme(a, b):
            couplet.append(line[0])

    return couplet


for j in range(3):
    poem = make_stanza(4)
    for line in poem:
        print(line)
    print("")

couplet = (make_rhyming_couplet())

for line in couplet:
    print(line)


# This is the messy non-formal initial code
# while again:
#     for k in range(5):
#         valid = False
#         while valid == False:
#             verse = model.make_sentence()
#             try:
#                 word2 = verse.rsplit(None, 1)[-1]
#                 word2 = word2.translate(translator)
#                 valid = True
#             except:
#                 valid = False
#         i = 1
#         verses.append(verse)
#         verse_count = verse_count + 1
#         print("verse " + str(verse_count) + " written")
#         while i < 2:
#             verse = model.make_sentence()
#             try:
#                 word1 = verse.rsplit(None, 1)[-1]
#                 word1 = word1.translate(translator)
#             except:
#                 word1 = "None"
#             if (not word1 == "None") and (doTheyRhyme(word1, word2)):
#                 verses.append(verse)
#                 i = i + 1
#                 verse_count = verse_count + 1
#                 print("verse " + str(verse_count) + " written")
#                 lines_generated = 0
#                 word2 = word1
#                 word2 = word2.translate(translator)
#             elif lines_generated < 300:
#                 lines_generated = lines_generated + 1
#                 if lines_generated % 19 == 0:
#                     print("thinking of a good verse...")
#                 elif lines_generated % 27 == 0:
#                     print("sipping coffee...")
#                 elif lines_generated % 42 == 0:
#                     print("procrastinating")
#             else:
#                 verses.append(verse)
#                 i = i + 1
#                 verse_count = verse_count + 1
#                 print("verse " + str(verse_count) + " written")
#                 word2 = word1
#                 word2 = word2.translate(translator)
#
#     print("")
#     for line in verses:
#         print(line)
#     print("")
#
#     again = False
