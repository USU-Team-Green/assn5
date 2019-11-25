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




def score_email(email_sender,  email_body):

    print('scoring email...\n')

    score = 10

    score -= spelling_errors(email_body)

    score -= phishing_terms(email_body)

    score -= examine_sender(email_sender)

    return score



def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper



if __name__ == '__main__':

    email_sender = 'confirm-to.own@airbnb.com'

    email_body_input = "dhl a muscket for home defense, and that's what the founding fathers dhl."



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