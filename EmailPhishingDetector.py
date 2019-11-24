from spellchecker import SpellChecker
import re
import fileinput



def phishing_terms(email_body):
    num_hits = 0
    partial_score = 0



    phishing_terms = open(r"commonPhishingTerms.txt", "r+")


    for term in phishing_terms:

        for word in email_body:
            if word == term:
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





def score_email(email_input,  email_body):

    print('scoring email...\n')

    score = 10


    score -= spelling_errors(email_body)

    score -= phishing_terms(email_body)

    return score




if __name__ == '__main__':

    email_input = 'swagdaddy@youngpapi.com'

    email_body_input = "Own a muscket for home defense, since that's what the founding fathers intended. "



    email_body = re.sub("[^\w]", " ", email_body_input).split()

    score = score_email(email_input, email_body)

    seven_ten = '(not very likely spam)'
    four_six = '(somewhat likely spam)'
    one_three = '(very likely spam)'

    decision = ''

    if score >= 7:
        decision = seven_ten

    if score >= 4 and score <= 6:
        decision = four_six

    if score <= 3:
        decision = one_three

    print('\n final score = ', score, decision)