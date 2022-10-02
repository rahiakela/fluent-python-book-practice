import os
import time
import sys
import requests


# List of the ISO 3166 country codes for the 20 most populous countries in order of decreasing population
POP20_CC = "CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR".split()

# The Web site with the flag images
BASE_URL = "http://flupy.org/data/flags"

# Local directory where the images are saved.
DEST_DIR = "downloads/"


# Simply save the img (a byte sequence) to filename in the DEST_DIR.
def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, "wb") as fp:
        fp.write(img)


def get_flag(cc):
    # Given a country code, build the URL and download the image, returning the binary contents of the response.
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)

    return resp.content


def show(text):
    """
    Display a string and flush sys.stdout so we can see progress in a one-line
    display; this is needed because Python normally waits for a line break to flush
    the stdout buffer.
    """
    print(text, end=" ")
    sys.stdout.flush()


# to compare with the concurrent implementations.
def download_many(cc_list):
    """
    loop over the list of country codes in alphabetical order, to make it clear that the
    ordering is preserved in the output; return the number of country codes downloaded.
    """
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + ".gif")

    return len(cc_list)


# main records and reports the elapsed time after running download_many;
def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = "\n{} flags downloaded in {:.2f}s"
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)

