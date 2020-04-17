# -*- coding: utf-8 -*-

import logging
from collections import Counter

# Requires: python3 -m spacy download en_core_web_sm
import spacy
# Google Translate API reference: https://googleapis.dev/python/translation/latest/index.html
from google.cloud import translate_v2
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
        self.nlp = spacy.load("en_core_web_sm")  # de_core_news_sm
        self.nlp.Defaults.stop_words |= STOP_WORDS
        self.nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
        self.translator = translate_v2.Client(target_language='en')

    @staticmethod
    def smart_truncate(content, length=2000, suffix='...'):
        if len(content) <= length:
            return content
        else:
            return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix

    def spc_detect_language(self, text):
        shortened = self.smart_truncate(text)
        doc = self.nlp(shortened)
        # detecting contains 'score' (0..1) and 'language' en, de
        return doc._.language['score'], doc._.language['language']

    def ggl_detect_language(self, text):
        shortened = self.smart_truncate(text, 100)
        logging.debug("Get language for '%s'", shortened)
        return self.translator.detect_language(shortened)  # en, de

    def ggl_translate(self, text, src_lang, length=2000):
        # see https://cloud.google.com/translate/quotas
        shortened = self.smart_truncate(text, length)
        logging.debug("Going to translate %d characters from %s", len(shortened), src_lang)
        translation = self.translator.translate(shortened, source_language=src_lang)
        # noinspection PyTypeChecker
        return translation['translatedText']

    def get_keywords(self, text, nr_keywords=12):
        doc = self.nlp(text)
        key_words = []
        for chunk in doc:
            if chunk.is_alpha and not chunk.is_stop:
                key_words.append(chunk.text.lower())

        return [word.title() for word, _
                in Counter(key_words).most_common(nr_keywords)]


if __name__ == '__main__':
    txt_frontliner = """Inspiration
                What it does
                How I built it
                Challenges I ran into
                Accomplishments that I'm proud of
                What I learned
                What's next for Frontlinehelper.org
                After watching news reports about so many restaurants facing hardship and seeing testimonials of COVID-19 frontline workers such as healthcare workers, truckers, grocery workers, etc. I realized that they could be brought together to help one another. My husband and son both work in our family trucking company, so I know first hand how hard everyone is working and the toll it takes. By connecting donors who donate money and/or time to pick up and deliver with restaurants willing to do curbside, to-go or catering, we can use the money donated to pay the restaurants (which keeps them in business), the donors to pick up the food and deliver it, and the frontline workers get fed. Then, I kept hearing about how some daycare facilities were closing. Now you've got all these workers who are already background checked and licensed, out of work. But the front line folks still need childcare or elder care. Why not partner them together? So that's how Frontline Helper was born. I secured the urls of frontlinehelper.org and frontlinehelper.com and we are in the process of creating the wireframes. We're building it so that it can be copied in all other communities...not just my local community,"""

    txt = """
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
    print("Detected language (google):", proc.ggl_detect_language(txt))
    (score, lang) = proc.spc_detect_language(txt)
    print("Detected language (spacey):", lang, " score:", score)

    cleaned = ' '.join(txt.split())
    translated = proc.ggl_translate(cleaned, lang)
    print("Translated to:", translated)

    print("Detected language of translation:", proc.ggl_detect_language(translated))
    # FIXME: Verify stopwords filtering, ie. why is "need" still in result keywords?
    print("English keywords:", proc.get_keywords(translated))
