# -*- coding: utf-8 -*-

# Requires: python3 -m spacy download en_core_web_sm

from collections import Counter

import googletrans as gt
import spacy
import logging

# Google Translate API reference: https://cloud.google.com/translate/docs/reference/rest


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
                                         "crisis", }

    def get_language(self, text):
        logging.info("Get language for '%s'", text[0:256])
        return gt.LANGUAGES[self.translator.detect(text[0:256]).lang]

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
    print("Detected language:", proc.get_language(remedy_txt))
    translated = proc.ggl_translate(remedy_txt)
    print("Translated to:", translated)
    print("Detected language of translation:", proc.get_language(translated))
    print("English keywords:", proc.get_keywords(translated))