import re
import sys
from pprint import pprint


BRACKET_ACRONYMS_RE = r'\(([A-Z1-9-]+?)\)'


'''
Find bracketed acryonyms
Map acro letters to first letters of tokens, then see if remaining letters exist in the middle of words
'''

class AcronymResolver():

    def __init__(self, text):
        self.text = text
        self.acro_data = self.acro_definitions(text)
        self.resolved = self.resolve_acros(text, self.acro_data)

    def acro_definitions(self, text):
        text = str(text)
        matches = re.finditer(BRACKET_ACRONYMS_RE, text)
        results = {}
        tokens = re.split(r'\s|\.|-|,', text)
        tokens = [t for t in tokens if t]
        for match in matches:
            acro = match.groups()[0]
            print(acro)
            span = (match.start() + 1, match.end() - 1)
            acro_idx = None
            for i, token in enumerate(tokens):
                if token == match.group():
                    acro_idx = i
                    break
            if not acro_idx:
                continue
            # search_length = 7
            # search_start = (acro_idx - 1) - 7
            # search_end = acro_idx
            # First try equal number of words and same letter beginings
            search_start = acro_idx - len(acro)
            search_end = acro_idx
            pre_tokens = tokens[search_start:search_end]
            def_tokens = []
            letters_already = []
            for i, letter in enumerate(reversed(acro)):
                for tok in reversed(pre_tokens):
                    if letter.lower() == tok[0].lower() and i not in letters_already:
                        def_tokens.append(tok)
                        letters_already.append(i)
            def_tokens = list(reversed(def_tokens))
            def_ = ' '.join(def_tokens)
            print(def_)
            results[acro] = {
                'definition': def_,
            }
            # letters_still = [l for i, l in enumerate(reversed(acro)) if i not in letters_already]
            # print('letters still:', letters_still)
        return results

    def resolve_acros(self, text, acro_definitions):
        text = str(text)
        for acro, d in acro_definitions.items():
            regex = r'[^\(]{0}[^\)]'.format(acro)
            repl = ' {0} '.format(d['definition'])
            text = re.sub(regex, repl, text)
        return text


if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        print('Pass text file')
        exit()
    with open(file, 'rb') as f:
        text = f.read()
        acro_defs = acro_definitions(text)
        text = resolve_acros(text, acro_defs)
        # pprint(acro_defs)
        print(text)