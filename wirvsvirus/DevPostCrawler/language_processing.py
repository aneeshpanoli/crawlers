# -*- coding: utf-8 -*-

import logging
from collections import Counter

# Google Translate API reference: https://cloud.google.com/translate/docs/reference/rest
import googletrans as gt
# Requires: python3 -m spacy download en_core_web_sm
import spacy
from spacy_langdetect import LanguageDetector

STOP_WORDS = {'able', 'better', 'build', 'built', 'causes', 'challenge',
              'challenges', 'changed', 'context', 'corona', 'covid',
              'create', 'crisis', 'curious', 'current', 'dear',
              'developed', 'different', 'end', 'forward', 'got', 'group',
              'hackathon', 'hackathons', 'high', 'impacts', 'inspiration',
              'journey', 'key', 'lot', 'list', 'need', 'new',
              'opportunity', 'people', 'presentation', 'problem',
              'problems', 'project', 'proud', 'provide', 'ran',
              'related', 'risk', 'situations', 'solution', 'solutions',
              'start', 'step', 'team', 'time', 'true', 'want', 'way'}


class LanguageProcessing(object):

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.Defaults.stop_words |= STOP_WORDS
        self.nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
        self.translator = gt.Translator()

    def spc_detect_language(self, text):
        doc = self.nlp(text)
        # detecting contains 'score' (0..1) and 'language' en, de
        return doc._.language['score'], doc._.language['language']

    def ggl_detect_language(self, text):
        logging.debug("Get language for '%s'", text[0:256])
        return gt.LANGUAGES[self.translator.detect(text[0:256]).lang]  # english, german

    def ggl_translate(self, text):
        # see https://cloud.google.com/translate/quotas
        translation = self.translator.translate(text[0:5000])
        return translation.text

    def get_keywords(self, text, nr_keywords=20):
        doc = self.nlp(text)
        key_words = []
        for chunk in doc:
            if chunk.is_alpha and not chunk.is_stop:
                key_words.append(chunk.text.lower())

        return [word.title() for word, _
                in Counter(key_words).most_common(nr_keywords)]


if __name__ == '__main__':
    remedy_txt = """
    Bedarfserbringer (Betriebe, Haushalte, Gesundheitseinrichtungen) 
    pflegen den Bestand lagernder Schutzartikel in die Plattform ein.
    
    Bedarfsträger (Krankenhäuser, Ärzte, Pflegedienste, weitere Institutionen) können über RemedyMatch innerhalb 
    kürzester Zeit einen aktuellen Überblick über verfügbare medizinische Schutzausrüstung erhalten und den Kontakt 
    zu dem/den Bedarfserbringer/n aufnehmen, welche Ressourcen zur Verfügung stellen können um die Lieferengpässe 
    dieser Artikel zu überbrücken.

    Schutzartikel, welche dem medizinischen Einsatz nicht gerecht werden, können an besonders gefährdete 
    Institutionen/Personengruppen (Apotheker, Tankstellen, Bankangestellte, Lebensmittelversorgung, Universitäten usw.) 
    verteilt werden um deren Schutz zu gewährleisten. Durch die Bevölkerung/Unternehmen gespendete Artikel müssen 
    (nachweislich korrekt gelagert und) originalverpackt sein, um für den medizinischen Einsatz geeignet zu sein.

    Die Verfügbarkeit kann über RemedyMatch geographisch eingegrenzt werden oder über Geomatching um die rasche 
    Versorgung dringend benötigter medizinischer Schutzartikel sicherzustellen.

    Ebenso bietet RemedyMatch die Möglichkeit Logistikpartner einzubinden und Angebote für Transportunterstützung 
    anzufordern. Hierzu können sich Logistikpartner (bspw. Bundeswehr, vertrauenswürdige/verifizierte 
    Privatpersonen/Unternehmer) registrieren um gemeinnützige Unterstützungsleistung anzubieten. 
    Über Geomatching werden Bedarfsträger, Bedarfserbringer und Logistikpartner miteinander verknüpft und 
    können sich über eine integrierte Chat-Funktion verständigen.

    Organisatorische Anforderungen für die erfolgreiche Umsetzung mit RemedyMatch: Einrichtung von Sammelstellen 
    für Spenden von Privatpersonen/Unternehmen Sammlung der Spenden und Transport in drei Zentrallager (Nord/Mitte/Süd). 
    Überschüssiger medizinischer Bedarf kann ebenso in den Zentrallagern vorgehalten werden um eine 
    24x7 Verfügbarkeit gewährleisten zu können.
    """
    proc = LanguageProcessing()
    print("Detected language (google):", proc.ggl_detect_language(remedy_txt))
    (score, lang) = proc.spc_detect_language(remedy_txt)
    print("Detected language (spacey):", lang, " score:", score)
    translated = proc.ggl_translate(remedy_txt)
    print("Translated to:", translated)
    print("Detected language of translation:", proc.ggl_detect_language(translated))
    # FIXME: Verify stopwords filtering, ie. why is "need" still in result keywords?
    print("English keywords:", proc.get_keywords(translated))
