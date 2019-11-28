from spellchecker import SpellChecker
import re
import math



def phishing_terms(email_body):

    num_hits = 0
    partial_score = 0


    for word in email_body:
        with open('commonPhishingTerms.txt') as f:
            if word.strip() in f.read() and len(word.strip()) > 2:
                num_hits += 1



    print('\n PHISHING TERMS')
    print('num hits: ', num_hits)
    percentage  = (num_hits / len(email_body)) * 100
    print('percentage: ', percentage, '%')

    if percentage > 5:
        partial_score = 5

    if(percentage > 10):
        partial_score = 10

    return partial_score




def spelling_errors(email_body):

    num_errors = 0
    partial_score = 0

    spell = SpellChecker()


    for word in email_body:

        if word != spell.correction(word):
            num_errors += 1

    percentage = (num_errors / len(email_body)) * 100

    print('SPELLING ERRORS')
    print('# errors: ', num_errors, ' percentage: ', percentage,"%")



    if percentage > 50:
        partial_score = 9

    return partial_score



def examine_sender(email_sender):
    spell = SpellChecker()

    num_hits = 0
    partial_score = 0

    sender_split = email_sender.split('@')

    first_part = sender_split[0]
    second_part = sender_split[1]


    #analyze first part
    num_dots = 0
    num_dashes = 0
    for char in first_part:
        if char == '.':
            num_dots += 1
        if char == '-':
            num_dashes += 1


    if num_dots > 1:
        num_hits += 5

    #big red flag if numbers in first part of email
    for char in first_part:
        with open('numbers.txt') as f:
            if char in f.read():
                num_hits += 10



    if first_part != spell.correction(first_part):
        num_hits += 10

    if (num_dashes + num_dots) >= 2:
        num_hits += 8

    #analyze second part
    num_dots = 0
    num_dashes = 0

    for char in second_part:
        if char == '.':
            num_dots += 1
        if char == '-':
            num_dashes += 1

    if num_dots > 1:
        num_hits += num_dots * 2
    if num_dashes > 1:
        num_hits += num_dashes * 2

    if num_dashes + num_dots > 2:
        num_hits += 3

    #spell check on second part
    if second_part != spell.correction(second_part):
        num_hits += 10


    # configure score
    partial_score += num_hits / 1.5


    print('\n Sender Score')
    print('hits: ', num_hits)
    print('sender sub score: ', partial_score)

    return partial_score


def write_to_blacklist(email_sender):

    new_addition = "\n" + email_sender

    with open('blacklist.txt') as f:
        if email_sender in f.read():
            print(email_sender, " already in blacklist")
            return
        else:
            passwords = open("blacklist.txt", "a")
            passwords.write(new_addition)
            passwords.close()


def check_blacklist(email_sender):

    on_blacklist = False

    sender_split = email_sender.split('@')

    second_part = sender_split[1]

    with open('blacklist.txt') as f:

        if email_sender in f.read():
            print("\n", email_sender, " ON BLACKLIST")
            on_blacklist = True

        if second_part in f.read():
            print("\n", second_part, " ON BLACKLIST")
            on_blacklist = True




    return on_blacklist


def check_whitelist(email_sender):

    on_whitelist = False

    sender_split = email_sender.split('@')

    second_part = sender_split[1]

    with open('whitelist.txt') as f:
        if second_part in f.read():
            print("\n", second_part, " ON WHITELIST")
            on_whitelist = True


    return on_whitelist


def score_email(email_sender,  email_body):

    print('scoring email...\n')

    score = 10

    on_whitelist = check_whitelist(email_sender)
    if on_whitelist == True:
        score = 10
        return score

    on_blacklist = check_blacklist(email_sender)
    if on_blacklist == True:
        score = 1
        return score

    score -= spelling_errors(email_body)

    score -= phishing_terms(email_body)

    score -= examine_sender(email_sender)


    if score == 1:
        write_to_blacklist(email_sender)

    return score



def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper



if __name__ == '__main__':

    # email_sender = 'blacklisttest1@testing.com'
    #
    # email_body_input = "testng"

    email_sender = input("Enter sending email address: ")
    email_body_input = input("Enter email body: ")


    #turns email body into list of words separated by spaces
    email_body = re.sub("[^\w]", " ", email_body_input).split()

    score = score_email(email_sender, email_body)


    seven_ten = '(not likely at all spam)'
    four_six = '(somewhat likely spam)'
    one_three = '(very likely spam)'

    decision = ''

    score = truncate(score, 1)

    if score >= 7:
        decision = seven_ten

    if score >= 4 and score <= 6:
        decision = four_six

    if score < 4:
        decision = one_three

    if score < 1:
        score = 1

    if score > 10:
        score = 10

    print('\n final score = ', score, decision)