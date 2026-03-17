import re

def clean_email(text):

    # remove headers
    text = re.sub(r"(from|subject|return-path|received):.*\n", "", text, flags=re.I)

    # remove html
    text = re.sub(r"<.*?>", "", text)

    text = text.lower()

    # replace emails
    text = re.sub(r"\S+@\S+", "EMAIL", text)

    # replace urls
    text = re.sub(r"http\S+|www\S+", "URL", text)

    # replace numbers
    text = re.sub(r"\d+", "NUMBER", text)

    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text