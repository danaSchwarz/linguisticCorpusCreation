import pandas as pd
import spacy

# load nlp model
nlp = spacy.load("es_dep_news_trf")

# load text file
with open("test.txt", 'r', encoding="utf-8") as f:
    input_text = f.read()


def process_text(input_text):
    # process text
    doc = nlp(input_text)

    for sent in doc.sents:
        satz = sent.text

        for token in sent:

            # filter verbs and auxiliars
            if token.pos_ == "VERB" or token.pos_ == "AUX":

                # asign properties
                token_name = token
                verb_lemma = token.lemma_
                verb_type = token.pos_
                verb_text = token.text

                # filter and strip symbols that can become obstacles in the process
                if verb_lemma.endswith(" él") or verb_lemma.endswith(" yo"):
                    verb_lemma_new = verb_lemma.rstrip(" élyo")
                    verb_lemma = verb_lemma_new

                # asign rest of the properties
                v_persona = token_name.morph.get("Person", "")
                v_numero = token_name.morph.get("Number", "")
                has_nsubj = False
                this_nsubj = ""
                pron = False

                # look for nominative subjects
                for token in token_name.children:
                    if token.dep_ == "nsubj":
                        has_nsubj = True
                        this_nsubj = token.text
                        if token.pos_ == "PRON":
                            pron = True

                        break

                # since morph creates a list if a property is found
                # for formatting purposes the list is turned into a string and symbols are stripped
                verb_numero = ""
                verb_persona = ""

                if len(v_numero) > 0:
                    verb_numero = v_numero[0].strip("[']")

                if len(v_persona) > 0:
                    verb_persona = v_persona[0].strip("[']")

                v_tense = token.morph.get("Tense")
                v_modo = token.morph.get("Mood")
                verb_tense = ""
                verb_modo = ""

                if len(v_tense) > 0:
                    verb_tense = v_tense[0].strip("[']")

                if len(v_modo) > 0:
                    verb_modo = v_modo[0].strip("[']")

                # unfortunately the spanish model is not very accurate nor useful for finding time tenses therefor it was necessary to hardcode certain suffixes
                # aditionally to that it was necessary to fill the gaps and correct where necessary later in the final excel document
                if verb_tense == "" or verb_tense == "Past":
                    if verb_text.endswith("r") or verb_text.endswith("rle") or verb_text.endswith("rse") or verb_text.endswith("rla") or verb_text.endswith("rlo") or verb_text.endswith("rme") or verb_text.endswith("rte") or verb_text.endswith("ros") or verb_text.endswith("rnos") or verb_text.endswith("rlos") or verb_text.endswith("rlas") or verb_text.endswith("rles"):
                        verb_tense = "Infinitiv"
                        verb_modo = ""

                    elif verb_text.endswith("o") and verb_persona == "1":
                        verb_tense = "Pres"
                        verb_modo = "Ind"

                    elif verb_text.endswith("ría") or verb_text.endswith("rías") or verb_text.endswith("ríamos") or verb_text.endswith("rían"):
                        verb_tense = "Cond"
                        verb_modo = ""

                    elif verb_text.endswith("ia") or verb_text.endswith("ía") or verb_text.endswith("ías") or verb_text.endswith("ias") or verb_text.endswith("ían") or verb_text.endswith("ian") or verb_text.endswith("iamos") or verb_text.endswith("íamos") or verb_text.endswith("aba") or verb_text.endswith("abas") or verb_text.endswith("abamos") or verb_text.endswith("ábamos") or verb_text.endswith("aban"):
                        verb_tense = "Imperf"
                        verb_modo = "Ind"

                    elif verb_text.endswith("aré") or verb_text.endswith("arás") or verb_text.endswith("ará") or verb_text.endswith("arámos") or verb_text.endswith("arán") or verb_text.endswith("eré") or verb_text.endswith("erás") or verb_text.endswith("erá") or verb_text.endswith("erámos") or verb_text.endswith("erán"):
                        verb_tense = "Futur"
                        verb_modo = ""

                    elif verb_text.endswith("ó") or verb_text.endswith("é") or verb_text.endswith("iste") or verb_text.endswith("aste"):
                        verb_tense = "Indef"
                        verb_modo = ""

                    elif verb_text.endswith("ando") or verb_text.endswith("endo"):
                        verb_tense = "Gerundio"
                        verb_modo = ""

                    elif verb_text.endswith("ado") or verb_text.endswith("ido"):
                        verb_tense = "Partizip"
                        verb_modo = ""

                    elif verb_text == "fui" or verb_text == "fue" or verb_text == "fuimos" or verb_text == "fueron":
                        verb_tense = "Indef"
                        verb_modo = ""

                    elif verb_text == "era" or verb_text == "eras" or verb_text == "eramos" or verb_text == "éramos" or verb_text == "eran":
                        verb_tense = "Imperf"
                        verb_modo = "Ind"

                    elif verb_text == "soy" or verb_text == "eres" or verb_text == "sos" or verb_text == "es" or verb_text == "somos" or verb_text == "sois" or verb_text == "son":
                        verb_tense = "Pres"
                        verb_modo = "Ind"

                    elif verb_text.endswith("a") or verb_text.endswith("amos") and verb_lemma.endswith("ar"):
                        verb_tense = "Pres"
                        verb_modo = "Ind"

                    elif verb_text.endswith("e") or verb_text.endswith("emos") and verb_lemma.endswith("er"):
                        verb_tense = "Pres"
                        verb_modo = "Ind"

                    else:
                        verb_tense = "not found"
                        verb_modo = ""

                # the object is created and appended to the list which will later be converted to an excel file
                verb_list.append(WordObject(
                    verb_lemma, verb_type, token_name, verb_numero, verb_persona, verb_tense, verb_modo, has_nsubj, pron, this_nsubj, satz))


# Verb Objekt
class WordObject:
    def __init__(self, verb_lemma, verb_type, verb_name, verb_num, verb_pers, verb_tense, verb_modo, verb_nsubj, pron, verb_this_nsubj, sentence):
        self.verb_lemma = verb_lemma
        self.verb_aux = verb_type
        self.verb_name = verb_name
        self.verb_num = verb_num
        self.verb_pers = verb_pers
        self.verb_tense = verb_tense
        self.verb_modo = verb_modo
        self.verb_nsubj = verb_nsubj
        self.verb_pron = pron
        self.verb_this_nsubj = verb_this_nsubj
        self.verb_sentence = sentence

    # print object (part of print table below)

    def to_dict(self) -> dict:
        return {
            "Lemma": self.verb_lemma,
            "Aux": self.verb_aux,
            "Verb": self.verb_name,
            "Número": self.verb_num,
            "Persona": self.verb_pers,
            "Tiempo": self.verb_tense,
            "Modo": self.verb_modo,
            "Nsubj": self.verb_nsubj,
            "Pron": self.verb_pron,
            "Subj": self.verb_this_nsubj,
            "Frase": self.verb_sentence
        }

# convert list into excel file


def export_excel(verb_list: list[WordObject], filename):
    rows = []
    for i, word_obj in enumerate(verb_list):
        rows.append(word_obj.to_dict())
    df = pd.DataFrame.from_dict(rows)

    df.to_excel(f'{filename}.xlsx', index=False)


verb_list = []

process_text(input_text)
export_excel(verb_list, "test_completed")
