from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '7156618229:AAHk8ulzmz87lzw5XXkMfTPEF2GW1c3EXds'
CHAT_ID = '-1001419545064'


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=data)


@app.route('/github-webhook/', methods=['POST'])
def github_webhook():
    if request.method == 'POST':
        payload = request.json

        if 'commits' in payload:
            repo_name = payload['repository']['full_name']
            branch = payload['ref'].split('/')[-1]
            pusher = payload['pusher']['name']
            commit_messages = "\n".join([commit['message'] for commit in payload['commits']])

            message = f"Repository: *{repo_name}*\nBranch: *{branch}*\nPusher: *{pusher}*\nCommits:\n{commit_messages}"
            send_telegram_message(message)

        if 'action' in payload and payload['action'] == 'closed' and payload['pull_request']['merged']:
            repo_name = payload['repository']['full_name']
            branch = payload['pull_request']['base']['ref']
            merger = payload['pull_request']['merged_by']['login']

            message = f"Repository: *{repo_name}*\nBranch: *{branch}*\nMerged by: *{merger}*"
            send_telegram_message(message)

        return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
