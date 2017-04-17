import requests
import urllib2
import csv
import json
import re
import time
import datetime
from bs4 import BeautifulSoup
from trello import TrelloApi


class angelList(object):

    def __init__(self):
        super(angelList, self).__init__()

    def getStartupIDs(self):
        payload_data = json.loads(open('./job_data.json').read())

        url = "https://angel.co/job_listings/startup_ids"
        headers = {
            'accept': "*/*",
            'origin': "https://angel.co",
            'x-csrf-token': "gUUpmkKuDq2M/2bauNDkA+iwOucebsQWJsQsclI/gSU=",
            'x-requested-with': "XMLHttpRequest",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'dnt': "1",
            'referer': "https://angel.co/jobs",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.8",
            'cookie': "_ga=GA1.2.715248434.1490732477; amplitude_idangel.co=eyJkZXZpY2VJZCI6ImNhZjllMzQ3LTQ5ZWItNDE5My1iNjk5LWExNTZjZDI5MWM1NlIiLCJ1c2VySWQiOiI0MzIwNjEiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE0OTE2MDc2Nzg4NTYsImxhc3RFdmVudFRpbWUiOjE0OTE2MTAwNzY2NTQsImV2ZW50SWQiOjI2LCJpZGVudGlmeUlkIjo3Mywic2VxdWVuY2VOdW1iZXIiOjk5fQ==; mp_mixpanel__c=2; ajs_group_id=null; ajs_user_id=%22432061%22; ajs_anonymous_id=%22b027ed2467c4446b37fda1e5a195c2fa%22; mp_6a8c8224f4f542ff59bd0e2312892d36_mixpanel=%7B%22distinct_id%22%3A%20%22432061%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24username%22%3A%20%22max-ramsay-1%22%2C%22angel%22%3A%20false%2C%22candidate%22%3A%20true%2C%22roles%22%3A%20%5B%0A%20%20%20%20%22software%20engineer%22%2C%0A%20%20%20%20%22frontend%20developer%22%0A%5D%2C%22quality_ceiling%22%3A%20%226%22%2C%22%24search_engine%22%3A%20%22google%22%7D; _angellist=661553c33edde97a09da4eddead92959; _ga=GA1.2.715248434.1490732477; amplitude_idangel.co=eyJkZXZpY2VJZCI6ImNhZjllMzQ3LTQ5ZWItNDE5My1iNjk5LWExNTZjZDI5MWM1NlIiLCJ1c2VySWQiOiI0MzIwNjEiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE0OTE2MDc2Nzg4NTYsImxhc3RFdmVudFRpbWUiOjE0OTE2MTAwNzY2NTQsImV2ZW50SWQiOjI2LCJpZGVudGlmeUlkIjo3Mywic2VxdWVuY2VOdW1iZXIiOjk5fQ==; _ga=GA1.2.715248434.1490732477; amplitude_idangel.co=eyJkZXZpY2VJZCI6ImNhZjllMzQ3LTQ5ZWItNDE5My1iNjk5LWExNTZjZDI5MWM1NlIiLCJ1c2VySWQiOiI0MzIwNjEiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE0OTE2MDc2Nzg4NTYsImxhc3RFdmVudFRpbWUiOjE0OTE2MTAwNzY2NTQsImV2ZW50SWQiOjI2LCJpZGVudGlmeUlkIjo3Mywic2VxdWVuY2VOdW1iZXIiOjk5fQ==; mp_mixpanel__c=0; ajs_group_id=null; ajs_user_id=%22432061%22; ajs_anonymous_id=%22b027ed2467c4446b37fda1e5a195c2fa%22; mp_mixpanel__c=2; ajs_group_id=null; ajs_user_id=%22432061%22; ajs_anonymous_id=%22b027ed2467c4446b37fda1e5a195c2fa%22; mp_6a8c8224f4f542ff59bd0e2312892d36_mixpanel=%7B%22distinct_id%22%3A%20%22432061%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24username%22%3A%20%22max-ramsay-1%22%2C%22angel%22%3A%20false%2C%22candidate%22%3A%20true%2C%22roles%22%3A%20%5B%0A%20%20%20%20%22software%20engineer%22%2C%0A%20%20%20%20%22frontend%20developer%22%0A%5D%2C%22quality_ceiling%22%3A%20%226%22%2C%22%24search_engine%22%3A%20%22google%22%7D; _angellist=661553c33edde97a09da4eddead92959",
            'cache-control': "no-cache",
            'postman-token': "3a1a77b9-4da8-fbb3-b493-c185e8824cca"
        }
        response = requests.request(
            "POST", url, data=payload_data, headers=headers)
        jsonData = response.json()

        idList = jsonData['ids']
        print idList
        strList = []
        for item in idList:
            item = str(item)
            strList.append(item)
        return strList

    def getPageHTML(self, string_list):
        querystring = {"startup_ids[]": string_list}
        url = "https://angel.co/job_listings/browse_startups_table"
        headers = {
            'accept': "*/*",
            'x-csrf-token': "gUUpmkKuDq2M/2bauNDkA+iwOucebsQWJsQsclI/gSU=",
            'x-requested-with': "XMLHttpRequest",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            'dnt': "1",
            'referer': "https://angel.co/jobs",
            'accept-encoding': "gzip, deflate, sdch, br",
            'accept-language': "en-US,en;q=0.8",
            'cookie': "_ga=GA1.2.715248434.1490732477; amplitude_idangel.co=eyJkZXZpY2VJZCI6ImNhZjllMzQ3LTQ5ZWItNDE5My1iNjk5LWExNTZjZDI5MWM1NlIiLCJ1c2VySWQiOiI0MzIwNjEiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE0OTE2MDc2Nzg4NTYsImxhc3RFdmVudFRpbWUiOjE0OTE2MTAwNzY2NTQsImV2ZW50SWQiOjI2LCJpZGVudGlmeUlkIjo3Mywic2VxdWVuY2VOdW1iZXIiOjk5fQ==; mp_mixpanel__c=2; ajs_group_id=null; ajs_user_id=%22432061%22; ajs_anonymous_id=%22b027ed2467c4446b37fda1e5a195c2fa%22; mp_6a8c8224f4f542ff59bd0e2312892d36_mixpanel=%7B%22distinct_id%22%3A%20%22432061%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24username%22%3A%20%22max-ramsay-1%22%2C%22angel%22%3A%20false%2C%22candidate%22%3A%20true%2C%22roles%22%3A%20%5B%0A%20%20%20%20%22software%20engineer%22%2C%0A%20%20%20%20%22frontend%20developer%22%0A%5D%2C%22quality_ceiling%22%3A%20%226%22%2C%22%24search_engine%22%3A%20%22google%22%7D; _angellist=661553c33edde97a09da4eddead92959; _ga=GA1.2.715248434.1490732477; amplitude_idangel.co=eyJkZXZpY2VJZCI6ImNhZjllMzQ3LTQ5ZWItNDE5My1iNjk5LWExNTZjZDI5MWM1NlIiLCJ1c2VySWQiOiI0MzIwNjEiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE0OTE2MDc2Nzg4NTYsImxhc3RFdmVudFRpbWUiOjE0OTE2MTAwNzY2NTQsImV2ZW50SWQiOjI2LCJpZGVudGlmeUlkIjo3Mywic2VxdWVuY2VOdW1iZXIiOjk5fQ==; _ga=GA1.2.715248434.1490732477; amplitude_idangel.co=eyJkZXZpY2VJZCI6ImNhZjllMzQ3LTQ5ZWItNDE5My1iNjk5LWExNTZjZDI5MWM1NlIiLCJ1c2VySWQiOiI0MzIwNjEiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE0OTE2MDc2Nzg4NTYsImxhc3RFdmVudFRpbWUiOjE0OTE2MTAwNzY2NTQsImV2ZW50SWQiOjI2LCJpZGVudGlmeUlkIjo3Mywic2VxdWVuY2VOdW1iZXIiOjk5fQ==; mp_mixpanel__c=0; ajs_group_id=null; ajs_user_id=%22432061%22; ajs_anonymous_id=%22b027ed2467c4446b37fda1e5a195c2fa%22; mp_mixpanel__c=2; ajs_group_id=null; ajs_user_id=%22432061%22; ajs_anonymous_id=%22b027ed2467c4446b37fda1e5a195c2fa%22; mp_6a8c8224f4f542ff59bd0e2312892d36_mixpanel=%7B%22distinct_id%22%3A%20%22432061%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24username%22%3A%20%22max-ramsay-1%22%2C%22angel%22%3A%20false%2C%22candidate%22%3A%20true%2C%22roles%22%3A%20%5B%0A%20%20%20%20%22software%20engineer%22%2C%0A%20%20%20%20%22frontend%20developer%22%0A%5D%2C%22quality_ceiling%22%3A%20%226%22%2C%22%24search_engine%22%3A%20%22google%22%7D; _angellist=661553c33edde97a09da4eddead92959",
            'cache-control': "no-cache",
            'postman-token': "508b38cc-4f44-dbcd-922a-b82be2771938"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        return response.text

    def parseHTML(self, html_data):
        coun = 0
        parsedArr = []
        soup = BeautifulSoup(html_data, "lxml")
        aArray = soup.findAll("div", {"class": "browse_startups_table_row"})

        for item in aArray:
            respondsFast = False

            tagRow = item.findAll("div", {"class": "tag-row"})
            for tagerItem in tagRow:
                thisText = tagerItem.get_text()
                if 'quickly' in thisText:
                    respondsFast = True

            topCorner = item.findAll("td", {"class": "top-left-corner"})
            for topItem in topCorner:
                image = item.find('img')['src']

            for title in item.findAll("div", {"class": "tags"}):

                tags = title.get_text().replace('\n', '').lower()

                if 'francisco' in tags:
                    listingData = item.findAll("div", {"class": "listing-row"})
                    for item in listingData:

                        title = item.find("a").get_text().replace('\n', '')
                        joburl = item.find("a").get('href').replace('\n', '')
                        findArr = re.findall(
                            r"\/[^\/][^\/]*\/([^\/]*)\/", joburl)
                        company = findArr[0]
                        lowtitle = title.lower()
                        if 'senior' not in lowtitle and 'engineer' in lowtitle and 'front' in lowtitle and 'lead' not in lowtitle:

                            parsedDict = {}
                            parsedDict["company_name"] = company
                            parsedDict["job_title"] = title
                            parsedDict["joburl"] = joburl
                            parsedDict["image"] = image
                            parsedDict['respondsFast'] = respondsFast
                            parsedArr.append(parsedDict)
        return parsedArr
