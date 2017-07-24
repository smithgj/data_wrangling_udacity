#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This exercise shows some important concepts that you should be aware about:
- using codecs module to write unicode files
- using authentication with web APIs
- using offset when accessing web APIs

To run this code locally you have to register at the NYTimes developer site
and get your own API key. You will be able to complete this exercise in our UI
without doing so, as we have provided a sample result. (See the file
'popular-viewed-1.json' from the tabs above.)

Your task is to modify the article_overview() function to process the saved
file that represents the most popular articles (by view count) from the last
day, and return a tuple of variables containing the following data:
- labels: list of dictionaries, where the keys are the "section" values and
  values are the "title" values for each of the retrieved articles.
- urls: list of URLs for all 'media' entries with "format": "Standard Thumbnail"

All your changes should be in the article_overview() function. See the test()
function for examples of the elements of the output lists.
The rest of functions are provided for your convenience, if you want to access
the API by yourself.
"""
import json
import codecs
import requests
import logging
import collections

logging.basicConfig(filename='nytimes.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.DEBUG)


URL_MAIN = "http://api.nytimes.com/svc/"
URL_POPULAR = URL_MAIN + "mostpopular/v2/"
API_KEY = {"popular": "406c72dfc872448597fb62b04e40cd29",
           "article": "406c72dfc872448597fb62b04e40cd29"}


def get_from_file(kind, period):
    filename = "popular-{0}-{1}.json".format(kind, period)
    logging.debug("check1")
    with open(filename, "r") as f:
        return json.loads(f.read())


def article_overview(kind, period):
    data = get_from_file(kind, period)
    logging.debug(len(data))
    titles = []
    urls = []
    mytitle = []
    mysection = []
    myDict = {}
    for i in range(0, len(data)):
        mytitle.append(data[i]["title"])
        mysection.append(data[i]["section"])
        logging.info("i = " + str(i))
        logging.info(mytitle)
        logging.info(mysection)

        for j in range(0, len(data[i]["media"])):
            logging.debug(data[i]["media"][j])
            logging.debug(data[i]["media"][j]["media-metadata"])
            for k in range(0, len(data[i]["media"][j]["media-metadata"])):
                logging.debug(data[i]["media"][j]['media-metadata'][k])
                if (data[i]["media"][j]['media-metadata'][k]["format"] == "Standard Thumbnail" ):
                    urls.append(data[i]["media"][j]['media-metadata'][k]["url"] )
    # YOUR CODE HERE

    for x in range(0, len(mysection)):
        myDict[x]= {mysection[x]:mytitle[x]}
        titles.append(myDict[x])
    return (titles, urls)


def query_site(url, target, offset):
    # This will set up the query with the API key and offset
    # Web services often use offset paramter to return data in small chunks
    # NYTimes returns 20 articles per request, if you want the next 20
    # You have to provide the offset parameter
    if API_KEY["popular"] == "" or API_KEY["article"] == "":
        print
        "You need to register for NYTimes Developer account to run this program."
        print
        "See Intructor notes for information"
        return False
    params = {"api-key": API_KEY[target], "offset": offset}
    r = requests.get(url, params=params)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def get_popular(url, kind, days, section="all-sections", offset=0):
    # This function will construct the query according to the requirements of the site
    # and return the data, or print an error message if called incorrectly
    if days not in [1, 7, 30]:
        print
        "Time period can be 1,7, 30 days only"
        return False
    if kind not in ["viewed", "shared", "emailed"]:
        print
        "kind can be only one of viewed/shared/emailed"
        return False

    url += "most{0}/{1}/{2}.json".format(kind, section, days)
    data = query_site(url, "popular", offset)

    return data


def save_file(kind, period):
    # This will process all results, by calling the API repeatedly with supplied offset value,
    # combine the data and then write all results in a file.
    data = get_popular(URL_POPULAR, "viewed", 1)
    num_results = data["num_results"]
    full_data = []
    with codecs.open("popular-{0}-{1}.json".format(kind, period), encoding='utf-8', mode='w') as v:
        for offset in range(0, num_results, 20):
            data = get_popular(URL_POPULAR, kind, period, offset=offset)
            full_data += data["results"]

        v.write(json.dumps(full_data, indent=2))


def test():
    logging.debug("check0")
    titles, urls = article_overview("viewed", 1)
    assert len(titles) == 20
    assert len(urls) == 30
    assert titles[2] == {'Opinion': 'Professors, We Need You!'}
    assert urls[20] == 'http://graphics8.nytimes.com/images/2014/02/17/sports/ICEDANCE/ICEDANCE-thumbStandard.jpg'


if __name__ == "__main__":
    test()