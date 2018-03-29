import re
import urllib2

from bs4 import BeautifulSoup
from nltk.corpus import stopwords  # Filter out stopwords, such as 'the', 'or', 'and'


def text_cleaner(website):
    try:
        site = urllib2.urlopen(website).read()
    except:
        return

    soup_obj = BeautifulSoup(site, "html.parser")

    for script in soup_obj(["script", "style"]):
        script.extract()

    text = soup_obj.get_text()

    lines = (line.strip() for line in text.splitlines())  # break into lines

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' '
        return chunk_out

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode(
        'utf-8')
    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    except:
        return

    text = re.sub("[^a-zA-Z.+3]", " ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
    text = text.lower().split()

    stop_words = set(stopwords.words("english"))
    text = [w for w in text if not w in stop_words]

    text = list(
        set(text))

    return text
