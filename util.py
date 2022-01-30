import unicodedata
from datetime import datetime
import time
from pathlib import Path
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def logMsg(msg, mode, artist_name):

    col = 0
    prefix = 0

    if mode == "okdl":
        col = bcolors.OKCYAN
        prefix = "[OK_DL   ]"

    elif mode == "okndl":
        col = bcolors.OKBLUE
        prefix = "[OK_NO_DL]"

    elif mode == "warn":
        col = bcolors.WARNING
        prefix = "[WARNING ]"

    elif mode == "err":
        col = bcolors.FAIL
        prefix = "[ERROR   ]"
    else:
        print(bcolors.FAIL + "SUPPLIED INVALID LOG MODE!!! USE EITHER okdl, okndl, warn, or err!")

    timestamp = getCurrentTimestamp()

    # Log to console
    print(col + f"[{timestamp}][{artist_name}]: " + msg)

    # Log to logfile
    logfile = open("./logs/" + slugify(artist_name) + ".txt", "a") # Open existing or create
    logfile.write(prefix + " " + "[" + timestamp + "]: " + msg + "\n")
    logfile.close()


def extensionFromUrl(url):
    rurl = url[::-1]
    rext = ""
    for c in rurl:
        if c != '.':
            rext = rext + c
        else:
            break

    ext = rext[::-1]

    # Now remove the get parameters
    foundQuestionmark = False
    actualExt = ""
    for c in ext:
        if c == '?':
            foundQuestionmark = True

        if not foundQuestionmark:
            actualExt = actualExt + c

    return actualExt


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def getCurrentTimestamp():
    return datetime.utcfromtimestamp(time.time()).strftime("%m-%d-%Y %H-%M")
