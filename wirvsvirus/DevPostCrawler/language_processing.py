# -*- coding: utf-8 -*-


import spacy
from collections import Counter
import googletrans as gt


class LanguageProcessing(object):

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.translator = gt.Translator()
        self.nlp.Defaults.stop_words |= {"solution",
                                         "solutions",
                                         "problem",
                                         "problems",
                                         "team",
                                         "group",
                                         "corona",
                                         "people",
                                         "risk",
                                         "want",
                                         "need",
                                         "time",
                                         "crisis",}

    def get_language(self, text):
        return gt.LANGUAGES[self.translator.detect(text).lang]

    def ggl_translate(self, text):
        translation = self.translator.translate(text)
        return [translation.text, gt.LANGUAGES[translation.lang]]

    def get_keyword(self, text):
        text = self.ggl_translate(text)

        doc = self.nlp(text)
        key_words = []
        for chunk in doc:
            if chunk.is_alpha and not chunk.is_stop:
                key_words.append(chunk.text.lower())

        return [word.title() for word, _
                    in Counter(key_words).most_common(5)]
