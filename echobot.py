import time
import requests
from settings import TOKEN

url_get_updates = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
url_send_message = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

try:
    with open('last_update.txt', 'r') as f:
        last_update_id = int(f.read())
except FileNotFoundError:
    last_update_id = 0

while True:
    params = {
        'offset': last_update_id,
        'timeout': 10
    }

    r = requests.get(url_get_updates, params=params)
    data = r.json()

    result = data.get('result', [])

    if not result:
        time.sleep(1)
        continue

    for update in result:
        msg = update.get('message', {})
        user = msg.get('from', {})

        text = msg.get('text')
        chat_id = user.get('id')

        if text and chat_id:
            message_params = {
                'chat_id': chat_id,
                'text': text
            }
            requests.get(url=url_send_message, params=message_params)

        last_update_id = update['update_id'] + 1

        with open('last_update.txt', 'w') as f:
            f.write(str(last_update_id))

