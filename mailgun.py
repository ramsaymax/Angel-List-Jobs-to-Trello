import requests

class Mailgun:

    def __init__(self):
        self.api_key = ''
        self.load_auth_from_file()

    def load_auth_from_file(self):
        if self.api_key == '':
            with open("./auth_mailgun.txt", "r") as myfile:
                self.api_key = myfile.readline().strip()

    def sendEmail(self, to, subject, message):

        print "Sending email to: " + to
        requests.post("https://api.mailgun.net/v3/sandbox47aaee9808044dacb6e02729d74ce45b.mailgun.org/messages",
                      auth=("api", self.api_key),
                      data={"from": "Mailgun Sandbox <postmaster@sandbox47aaee9808044dacb6e02729d74ce45b.mailgun.org>",
                            "to": to,
                            "subject": subject,
                            "text": message})
