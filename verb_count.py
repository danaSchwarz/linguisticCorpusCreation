import operator
import spacy
nlp = spacy.load("es_dep_news_trf")


# verb objekt for every lemma in the text
class VerbObject:
    def __init__(self, verb_name):
        self.verb_counter = 0
        self.verb_name = verb_name
        self.verb_nsub = 0
        self.verb_null = 0

    def print_verb_object(self):
        print(
            f"{self.verb_name}\t{self.verb_counter}\t{self.verb_nsub}\t{self.verb_null}")


# checks if nsubj within the children of a verb (checks if the sentence has a subject)
def has_nsubj(verb_token):
    return any(token.dep_ == "nsubj" for token in verb_token.children)


verb_dict = {}


def create_verb_object(lemma):
    return VerbObject(lemma)


# Text is processed and scanned for Verbs
def process_text(text):
    doc = nlp(text)

    current_verb = None

    for token in doc:
        if token.pos_ == "VERB":
            current_verb_1 = token.lemma_

            current_verb = current_verb_1.rstrip(" élyo")

            if current_verb not in verb_dict:
                verb_dict[current_verb] = VerbObject(current_verb)

            existing_verb = verb_dict[current_verb]

            existing_verb.verb_counter += 1

            if has_nsubj(token):
                existing_verb.verb_nsub += 1
            else:
                existing_verb.verb_null += 1

# Sort Verb dict by counter of verb object


def sort_verb_dict(verb_dict_1):
    sorted_dict = {}
    i = 0
    for verb in (sorted(verb_dict_1.values(), key=operator.attrgetter('verb_counter'), reverse=True)):
        sorted_dict[i] = verb
        i += 1

    return sorted_dict


def print_table(verb_list):
    print("Index\tVerb\tCounter\tNsubj\tNull")
    for i, verb_obj in enumerate(verb_list):
        print(f"{i+1}\t", end="")
        verb_obj.print_verb_object()


def sum_verbs(dict):
    sum = 0
    null = 0
    for verb in dict:
        x = verb.verb_counter
        sum += x
        y = verb.verb_null
        null += y

    return sum, null


if __name__ == "__main__":
    # load text file
    with open("test.txt", 'r', encoding="utf-8") as f:
        input_text = f.read()

    verbs = process_text(input_text)
    verb_dict_sorted = (sort_verb_dict(verb_dict))
    print_table(verb_dict_sorted.values())
    print(sum_verbs(verb_dict_sorted.values()))
