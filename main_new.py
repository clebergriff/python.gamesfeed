# encoding: utf-8

import time
import requests
import re
from bs4 import BeautifulSoup


def strip_text(full_string, before, after):
    try:
        result = full_string.split(before, 1)[1]

        if (after is not None) & (len(str(after)) > 0):
            result = result.split(after, 1)[0]

        return result
    except:
        return None


def find_between(s, start, end, only_first, trim):
    try:
        result = re.findall("%s.+?%s" % (re.escape(start), re.escape(end)), s)

        if only_first:
            if trim:
                result = result[0]
                result = result[(len(start)):]
                result = result[:-(len(end))]
                return result
            else:
                return result[0]
        else:
            return result
    except:
        return None


def valid_article(url, description, source):
    try:
        source = source.rsplit('/', 1)[0]

        return \
            (url is not None) & \
            (description is not None) & \
            (url.find('#') == -1) & \
            (description.find('<') == -1) & \
            (url.startswith(source))

    except Exception as e:
        return False


def valid_string(string):
    return \
        (string != "") & \
        (string is not None)


def watch_sources():

    query_insert_file = open("articles.txt", "a")
    query_tags_file = open("tags.txt", "r")

    try:
        for line in query_tags_file:
            row_tag = line.split('\t')

            source_id = row_tag[0]
            tag_title = row_tag[1].strip()
            tag_article = row_tag[2].strip()
            tag_start = row_tag[3].strip()
            tag_end = row_tag[4].strip()
            tag_img = row_tag[5].strip()

            url = None
            description = None
            img = None

            try:
                page = requests.get(url)

                if page.status_code == 200:
                    source_code = strip_text(page.text, ignore_before, ignore_after)

                    if source_code is None:
                        continue

                    soup_page = BeautifulSoup(source_code, "lxml")

                    if tag_article.find('|') == -1: # Não possui class
                        links = soup_page.findAll(tag_article)
                    else:
                        tag = tag_article.split('|', 1)[0]
                        tag_class = tag_article.split('|', 1)[1]
                        links = soup_page.findAll(tag, {"class": tag_class})

                    for link in links:
                        try:
                            soup_link = BeautifulSoup(str(link), "lxml")

                            for a_href in soup_link.find_all('a'):
                                url = a_href.get('href')
                                description = a_href.text.strip()

                                if description.find(" ") == -1:
                                    description = ""

                                break

                            for anchor in soup_link.findAll(tag_start):
                                if tag_title == "":
                                    tag_title = None
                                    tag_replace = ""
                                else:
                                    tag_title = tag_title.split('|', 1)[0]

                                    try:
                                        tag_replace = tag_title.split('|', 1)[1]
                                    except:
                                        tag_replace = ""

                                if not valid_string(description):
                                    try:
                                        if tag_title is not None:
                                            description = anchor.get(tag_title)
                                            description = description.replace(tag_replace, "")
                                        else:
                                            description = anchor.string
                                    except:
                                        continue

                            if not valid_string(description):
                                description = anchor.string
                            
                            for anchor in soup_link.findAll("img"):
                                img = anchor.get(tag_img)
                                img = img.rsplit('?', 1)[0]

                            if not valid_string(description):
                                description = anchor.get("alt")

                        url_src = url.rsplit('/', 1)[0]

                        if url[0] == "/":
                            url = url_src + url

                        if not (valid_article(url, description, url_src)):
                            continue

                        query_insert_file.write(f"{source_id}\t{url}\t{description}\t{str(img or '')}\n")
                    
                        print(f"Source ID: {source_id}\tURL: {url}\tDescription: {description}\tImage: {img}")

print("Starting sources verification..")
watch_sources()
print("Done fetching!")