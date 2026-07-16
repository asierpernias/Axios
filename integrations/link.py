import time


pending_links = {}


def start(slack_id):
    pending_links[slack_id] = {
        "created": time.time()
    }


def waiting(slack_id):
    return slack_id in pending_links


def finish(slack_id):
    if slack_id in pending_links:
        del pending_links[slack_id]