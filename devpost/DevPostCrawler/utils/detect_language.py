import spacy
from spacy_langdetect import LanguageDetector

if __name__ == '__main__':
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

    text = """This is English text. Er lebt mit seinen Eltern und seiner Schwester in Berlin. 
              Yo me divierto todos los días en el parque. 
              Je m'appelle Angélica Summer, j'ai 12 ans et je suis canadienne."""
    doc = nlp(text)

    # document level language detection. Think of it like average language of document!
    print("Detected language: ", doc._.language)

    # sentence level language detection
    for i, sent in enumerate(doc.sents):
        print(sent, sent._.language)

