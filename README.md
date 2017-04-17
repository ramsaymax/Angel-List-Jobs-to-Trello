# AngelList Jobs to Trello

This script allows you to push new jobs found on Angelist to a Trello board. It will update the board with the initial list it finds, then incrementally add new jobs as they are discovered and shoot you an email when a new listing is found. it is intended to run on a server as it runs every `x` minutes (you can specify this parameter).

I find this script to be helpful when I'm job searching, as it can give you a head start on new listings. It also allows for easier organization of jobs that you've applied for.

  - AngelList have closed their API, so this data is not easily accessible
  - Their job notifications aggregate after a certain time period, so you dont get notified of new listings instantly
  - This script works as of 16/04/2017 (Not sure how long Angel.co will keep their current HTTP get/post combo used to retrieve the listings)
  - Changing the loop timing may increase the likihood of rate limiting/IP blocking

### Features
 - Adds an orange label if the employer is known to respond quickly
 - Adds a green label for new listings
 - Notifies by email when a new listing has been found

### Dependencies

  - Beautiful Soup - https://crummy.com/software/BeautifulSoup/
  - An API Key and account with Mail Gun - https://mailgun.com/
  - Trello API Key and account - https://trello.com
  - A server to run the script on, I use https://pythonanywhere.com. You can run this locally but it is intended to run in the background permanently

### Before you begin

1. Add Mail Gun API Key to `auth_mailgun.txt`
2. Add Trello API Key and Token to `auth_trello.json`
3. Specify search Params in `job_data.json` (I have some sample data in here, if you'd like you add new fields that I have not included you'll need to intercept a new request using a chrome extension like [Postman Interceptor](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en)

### Initial Setup

1. Clone the Repository into the directory of your choice
```sh
$ git clone https://github.com/ramsaymax/Angel-List-Jobs-to-Trello.git
```

1. Login to Trello and get the board ID from the URL string as shown below. This is the ID of the board containing the list you'd like to write to.
![options CSV](http://i.imgur.com/qhQ7o6C.png)
2. Create a new list in trello, and make a note of its **exact name** as it appears in their app

3. `cd` into the project folder where you've cloned this script and run:
```sh
$ python setup.py
```
4. Enter the board ID as shown above, and press enter.
5. Enter the **exact name** of the list as it appears in Trello. Press enter and you'll be prompted with a success message if the setup was successful.

6. Enter the email address you'd like new job notifications sent to.


6. Lastly, make sure `daily_check.csv` is empty (This allows for the board to populate).

7. run `python main.py`

You should now see jobs populating in your board list.
![options CSV](http://i.imgur.com/4bhTqTx.png)
