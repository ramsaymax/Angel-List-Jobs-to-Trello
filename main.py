import requests,csv,json,re,time,datetime
from bs4 import BeautifulSoup
from trello import TrelloApi
from AngelList import *
from mailgun import Mailgun

# Instantiate mailgun class
mg = Mailgun()

# Instantiate AngelList class
angel_list = angelList()

# Load Trello Auth data from file
auth_data = json.loads(open('./auth_trello.json').read())

# Set Trello Auth Data
if auth_data:
    trello = TrelloApi(auth_data['key'])
    trello.set_token(auth_data['token'])
else:
    print "Add API key and token to auth_trello.json"

#get Trello list ID
list_data = json.loads(open('./data_trello_board.json').read())

# Fire off an email to let you know when the script starts
mg.sendEmail(list_data['email'], "Job Script Kickoff Successful",
             "script started at " + str(datetime.datetime.now()))

# Initialize loop counters
counter = 0
half_hour_counter = 0


# Infinite loop to periodically check AngelList
while True:

    # reference array for previous list of jobs
    old_rows_list = []

    # reference array for previous list of jobs + any new jobs discovered
    new_rows_list = []

    # open the file where we store the previous jobs listed

    daily_check_file_reader = open('daily_check.csv', 'rb')
    reader = csv.reader(daily_check_file_reader)

    for row in reader:
        old_rows_list.append(row[0])

    daily_check_file_reader.close()

    try:
        status = ''
        now = datetime.datetime.now().strftime('%Y-%m-%d')

        page_ids = angel_list.getStartupIDs()
        html_data = angel_list.getPageHTML(page_ids)
        json_data = angel_list.parseHTML(html_data)

        for item in json_data:

            company_name = item['company_name']
            title_and_company = item['job_title'] + " at " + company_name
            itemURL = item['joburl']
            image = item['image']
            responder = item['respondsFast']

            if title_and_company not in old_rows_list:
                mg.sendEmail(list_data['email'], "Angelist Job Alert:" +
                             str(title_and_company), itemURL + "\n" + str(datetime.datetime.now()))
                status = "item found"
                new_rows_list.append(title_and_company)
                try:
                    print "found new item"

                    trello.lists.new_card(
                        list_data['list_id'], title_and_company, desc=itemURL)
                    cardList = trello.lists.get_card(
                        list_data['list_id'])

                    for item in cardList:
                        if item['name'] == title_and_company:

                            trello.cards.new_label(item['id'], 'green')
                            trello.cards.new_attachment(
                                item['id'], image, image)
                            if responder == True:
                                trello.cards.new_label(item['id'], 'orange')
                                pass

                except:
                    continue

            else:
                status = "No New Items"

        if new_rows_list:
            "writing new items to daily csv"
            for item in new_rows_list:
                old_rows_list.append(item)
            daily_check_file_writer = open('daily_check.csv', 'wb')

            writer = csv.writer(daily_check_file_writer)

            for item in old_rows_list:
                writer.writerow([item])
            daily_check_file_writer.close()

        counter = 1

        print status

        time.sleep(1800)
        half_hour_counter += 1

        if half_hour_counter == 47:
            exit()

    except Exception as e:
        continue
