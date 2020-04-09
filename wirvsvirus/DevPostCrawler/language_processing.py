# -*- coding: utf-8 -*-


import spacy
from collections import Counter
import googletrans as gt


class LanguageProcessing(object):

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.translator = gt.Translator()

    def get_language(self, text):
        return gt.LANGUAGES[self.translator.detect(text).lang]

    def ggl_translate(self, text):
        translation = self.translator.translate(text)
        return translation.text

    def get_keyword(self, text):
        language = self.get_language(text)
        if language != 'english':
            text = self.ggl_translate(text)

        doc = self.nlp(text)
        key_words = []
        for chunk in doc.noun_chunks:
            key_words.append(chunk.root.text)

        return [word.title() for word, _
                in Counter(key_words).most_common(5)]
