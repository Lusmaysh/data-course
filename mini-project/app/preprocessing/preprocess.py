import spacy

npl = spacy.load("en_core_web_sm")

def tokenize(text: str):
    """
    Tokenize text using spaCy, keeping only alphabetic tokens that are not stop words.
    Return lemmatized, lowercased tokens.
    """
    doc = npl(text)
    tokens = []
    for t in doc:
        if t.is_alpha and not t.is_stop:
            tokens.append(t.lemma_.lower())

    return tokens