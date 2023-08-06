import requests
import json
import datetime

def report_failure_to_slack_wrapper(slack_webhook_url):
    def report_failure_to_slack(context):
        channel = context['dag'].tags[0]
        execution_date = datetime.datetime.fromisoformat(context['execution_date'])
        execution_date = f"{execution_date.year}-{execution_date.month}-{execution_date.day}"
        message = f"[Pipeline Error] [{channel}] [{execution_date}]"
        payload = {'text': message}
        headers = {'Content-type': 'application/json'}
        requests.post(slack_webhook_url, data=json.dumps(payload), headers=headers)
    return report_failure_to_slack