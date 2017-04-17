from trello import TrelloApi
import json

board_identifier = raw_input("Enter Board ID: ")
board_list = raw_input(
    "Enter the exact name of the list you'd like to write to: ")

email_address = raw_input(
    "Enter the email address you'd like to notifications sent to: ")

auth_data = json.loads(open('./auth_trello.json').read())

if auth_data:
    trello = TrelloApi(auth_data['key'])
    trello.set_token(auth_data['token'])
    trello.get_token_url(auth_data['appName'],
                         expires='30days', write_access=True)

else:
    print "Add API key and token to auth_trello.json"

trello_board = trello.boards.get_list(board_id=board_identifier, cards=None)

for item in trello_board:
    if item['name'] == board_list:
        data = {'list_id': item['id'],'email':email_address}

if data:
    json_str = json.dumps(data)
    data = json.loads(json_str)
    with open('data_trello_board.json', 'w') as f:
        json.dump(data, f)
    print "Setup Complete! Please run main.py to initialize the AngelList script"

else:
    print "sorry information incorrect, try again"
