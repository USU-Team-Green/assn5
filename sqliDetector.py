import re
import numpy as np


def test_for_illegal_queries(query):
    danger_terms = [
        "convert(",
        "xtype",
        "varchar",
    ]
    badness = 0
    for term in query.split():
        if term.lower() in danger_terms:
            badness += 1
    final = float(badness) / float(len(query.split()))
    message = None
    if final > .5:
        message = 'Likely contains an illogical or illegal query'
    return final, message

def test_for_tautologies(query):
    danger_patterns = [
        r"\d+\s*=\s*\d+",
        r"\d+\s*=\s*convert"
    ]
    badness = 0
    for pat in danger_patterns:
        if re.search(pat, query.lower()):
            badness += 1

    final = float(badness) / float(len(danger_patterns))
    message = None
    if final > .5:
        message = 'Likely contains a tautology'
    return (final, message)

def test_for_union_select(query):
    pattern = r'union\s+select'
    if re.search(pattern, query.lower()):
        return 1, 'Contains a union select'
    else:
        return 0, None

def test_for_piggyback(query):
    if len(re.findall(';', query)) > 1:
        return 1, 'There is probably a piggybacked query'
    else:
        return 0, None

def test_for_inference(query):
    danger_pattern = r'\bif(?:\s+|\()' # tests for 'if ' or 'if('
    if re.search(danger_pattern, query.lower()):
        return 0.9, 'Probably contains an if statement'
    else:
        return 0, None
def test_for_alternate_encoding(query):
    danger_pattern = r'exec\(char\(0x'
    if re.search(danger_pattern, query.lower()):
        return 1, 'Likely contains an alternate encoding attack'
    else:
        return 0, None

def test_for_general_danger_patterns(query):
    scores_and_messages = [
        test_for_illegal_queries(query),
        test_for_tautologies(query),
        test_for_union_select(query),
        test_for_piggyback(query),
        test_for_inference(query),
        test_for_alternate_encoding(query),
    ]
    
    nonzero_scores = list(filter(lambda x: x[0] != 0, scores_and_messages))
    if nonzero_scores == []:
        return 0, []
    score = np.mean([score[0] for score in nonzero_scores])
    messages = [score[1] for score in nonzero_scores]

    return score, messages


if __name__ == "__main__":
    done = False
    while not done:
        print("Which query would you like to test?")
        print("\t1: ItemName")
        print("\t2: UserName and Password")
        print("\t(q to quit)")
        resp = input()
        score, messages = None, None
        if resp == 'q':
            done = True
        elif resp == '1':
            resp = input('Enter ItemName: ')
            query = 'SELECT ItemDescription, ItemPrice\nFROM Items\nWHERE ItemName = {};'.format(resp)
            score, messages = test_for_general_danger_patterns(query)
        else:
            uname = input('Enter UserName: ')
            pas = input('Enter Password: ')
            query = 'SELECT Accounts\nFROM Users\nWHERE Username={} AND Password={};'.format(uname, pas)
            score, messages = test_for_general_danger_patterns(query)
        print('The score is {} ({}%)'.format(score, score * 100))
        for mes in messages:
            if mes:
                print(mes)
        resp = input("\nTry again? (Y/n) ")
        if resp not in ['Y', 'y']:
            done = True

