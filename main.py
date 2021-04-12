# encoding: utf-8

import mysql.connector
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


def watchSources():

    mydb = mysql.connector.connect(
        host="localhost",
        user="python",
        passwd="python",
        database='gamesfeed'
    )

    ativos = mydb.cursor(dictionary=True)

    ativos.execute("SELECT * FROM sources WHERE active = 1")

    ativos = ativos.fetchall()

    query_insert = mydb.cursor(dictionary=True)
    query_tags = mydb.cursor(dictionary=True)

    try:
        for row in ativos:
            print('Fetching source: %s - %s' % (row["name"], row["url"]))

            page = requests.get(row["url"])

            if page.status_code == 200:
                # soup = BeautifulSoup(page.text, "lxml")
                # print('[%s] Searching splitter' % (row["name"]))
                source_code = strip_text(page.text, row["ignore_before"], row["ignore_after"])

                if source_code is None:
                    print('No splitter found')
                    continue

                # print('[%s] Splitter found' % (row["name"]))

                sql = ("SELECT * FROM tags WHERE source_id = %d" % (row["id"]))
                query_tags.execute(sql)

                for row_tag in query_tags:
                    # row_tag["tag_title"]
                    soup_page = BeautifulSoup(source_code, "lxml")

                    if row_tag["tag_article"].find('|') == -1: # Não possui class
                        links = soup_page.findAll(row_tag["tag_article"])
                    else:
                        tag = row_tag["tag_article"].split('|', 1)[0]
                        tag_class = row_tag["tag_article"].split('|', 1)[1]
                        links = soup_page.findAll(tag, {"class": tag_class})

                    for link in links:
                        try:
                            url = None
                            description = None
                            img = None

                            soup_link = BeautifulSoup(str(link), "lxml")

                            for a_href in soup_link.find_all('a'):
                                url = a_href.get('href')
                                description = a_href.text.strip()

                                if description.find(" ") == -1:
                                    description = ""

                                break

                            # description = find_between(link, row_tag["tag_start"], row_tag["tag_end"], True, True)

                            for anchor in soup_link.findAll(row_tag["tag_start"]):
                                if row_tag["tag_title"] is None:
                                    tag_title = ""
                                else:
                                    tag_title = row_tag["tag_title"].split('|', 1)[0]

                                    try:
                                        tag_replace = row_tag["tag_title"].split('|', 1)[1]
                                    except:
                                        tag_replace = ""

                                if not valid_string(description):
                                    try:
                                        if tag_title != "":
                                            description = anchor.get(tag_title)
                                            description = description.replace(tag_replace, "")
                                        else:
                                            description = anchor.string
                                    except:
                                        continue

                            if not valid_string(description):
                                description = anchor.string

                            for anchor in soup_link.findAll("img"):
                                img = anchor.get(row_tag["tag_img"])
                                img = img.rsplit('?', 1)[0]

                                if not valid_string(description):
                                    description = anchor.get("alt")

                            url_src = row["url"].rsplit('/', 1)[0]

                            if url[0] == "/":
                                url = url_src + url

                            if not (valid_article(url, description, row["url"])):
                                # print('### [%s] URL: %s - Description: %s ###' % (row["name"], url, description))
                                # print('### Ignored ###')
                                continue

                            try:
                                sql = "INSERT INTO articles(source_id, url, description, img) VALUES (%s, \"%s\", \"%s\", \"%s\")" \
                                    % (row["id"], url, description, str(img or ""))
                                query_insert.execute(sql)
                                mydb.commit()

                                print("====")
                                # print('[%s] Link: %s' % (row["name"], link))
                                print('[%s]' % row["name"])
                                print('URL: %s' % url)
                                print('Description: %s' % description)
                                print('Success recording' % row["name"])

                            except Exception as e:
                                # print('Error recording: %s' % e)
                                continue

                            print("====")

                        except Exception as e:
                            continue
            else:
                print("HTTP return error" + str(page.status_code))
    except Exception as e:
        print(e)

        time.sleep(3)


print("Starting sources verification..")
watchSources()
print("Done fetching!")
