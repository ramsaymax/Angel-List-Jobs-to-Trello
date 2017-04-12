import requests,urllib2,csv,json,re,time,datetime
from bs4 import BeautifulSoup
from trello import TrelloApi

class angelList(object):

    def __init__(self):
        super(angelList, self).__init__()

    def getStartupIDs(self):
        # retrieve this resquest from the postman Chrome extention - https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en 
        #make sure the payload has your specific filters in it
        url = "https://angel.co/job_listings/startup_ids"
        payload = "filter_data%5Blocations%5D%5B%5D=1692-San%20Francisco%2C%20CA&filter_data%5Broles%5D%5B%5D=Frontend%20Developer&filter_data%5Bsalary%5D%5Bmax%5D=120&filter_data%5Bsalary%5D%5Bmin%5D=65&filter_data%5Bskills%5D%5B%5D=Javascript&filter_data%5Btypes%5D%5B%5D=full-time&tab=find"
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
            'cookie': #Cookie removed for privacy reasons
            'cache-control': "no-cache",
            'postman-token': "3a1a77b9-4da8-fbb3-b493-c185e8824cca"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        jsonData = response.json()
        idList = jsonData['ids']
        strList = []
        for item in idList:
            item = str(item)
            strList.append(item)
        return strList


    def getPageHTML(self,string_list):
        # retrieve this resquest from the postman Chrome extention - https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en 
        querystring = {"startup_ids[]": string_list}
        url ="https://angel.co/job_listings/browse_startups_table"
        headers = {
            'accept':"*/*",
            'x-csrf-token':"gUUpmkKuDq2M/2bauNDkA+iwOucebsQWJsQsclI/gSU=",
            'x-requested-with':"XMLHttpRequest",
            'user-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            'dnt':"1",
            'referer':"https://angel.co/jobs",
            'accept-encoding':"gzip, deflate, sdch, br",
            'accept-language':"en-US,en;q=0.8",
            'cookie': #Cookie removed for privacy reasons
            'cache-control':"no-cache",
            'postman-token':"508b38cc-4f44-dbcd-922a-b82be2771938"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.text


    def parseHTML(self,html_data):
        parsedArr = []
        soup = BeautifulSoup(html_data,"lxml")
        aArray = soup.findAll("div", { "class" : "listing-row" })
        for item in aArray:
            for title in item.findAll("div", { "class" : "tags" }):
                tags = title.get_text().replace('\n','').lower()
                if 'francisco' in tags:
                    title = item.find("a").get_text().replace('\n','')
                    joburl = item.find("a").get('href').replace('\n','')
                    findArr = re.findall(r"\/[^\/][^\/]*\/([^\/]*)\/", joburl)
                    company = findArr[0]
                    lowtitle = title.lower()
                    if 'senior' not in lowtitle and 'engineer' in lowtitle and 'front' in lowtitle and 'lead' not in lowtitle:
                        parsedDict = {}
                        parsedDict["company_name"] = company
                        parsedDict["job_title"] = title
                        parsedDict["joburl"] = joburl
                        parsedArr.append(parsedDict)
        return parsedArr


def email(to,subject,text):
    kickoff_email = requests.post(
        "https://api.mailgun.net/v3/sandbox47aaee9808044dacb6e02729d74ce45b.mailgun.org/messages",
        auth=("api",  ), #mailgun API key here
        data={"from": "Mailgun Sandbox <postmaster@sandbox47aaee9808044dacb6e02729d74ce45b.mailgun.org>",
        "to": to,
        "subject": subject,
         "text": text})



email("ENTER YOUR EMAIL ADDRESS","Job Script Kickoff Successful","script started at " + str(datetime.datetime.now()))

itemCheckList = []
dataArr = []
counter = 0
half_hour_counter = 0
trello = TrelloApi('') #add API Key 
trello.set_token('') #add Token
while True:

    try:
        status = ''
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        angel_list = angelList()
        page_ids = angel_list.getStartupIDs()
        html_data = angel_list.getPageHTML(page_ids)
        json_data = angel_list.parseHTML(html_data)

        for item in json_data:
            company_name = item['company_name']
            title_and_company = item['job_title'] + " at " + company_name
            itemURL = item['joburl']

            if half_hour_counter < 1:
                print title_and_company
                try:
                    trello.lists.new_card('ENTER CARD ID', title_and_company, desc=itemURL)
                except Exception as e:
                    print e
                
                exit()

            if title_and_company not in itemCheckList and counter > 0:
                status = "item found"
                try:
                    trello.lists.new_card('ENTER CARD ID', title_and_company, desc=itemURL)
                except:
                    continue

                email("EMAIL ADDRESS","Angelist Job Alert:" + str(title_and_company),itemURL + "\n" + str(datetime.datetime.now()))

            else:
                status = "No New Items"

            itemCheckList.append(title_and_company)

        counter = 1

        print status

        time.sleep(1800)
        half_hour_counter += 1

        if half_hour_counter == 47:
            exit()

    except Exception as e:
        continue
