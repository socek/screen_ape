from json import loads

from apeback.drivers.mq import BrowserQueueCommand

def is_message_valid(message):
    return (
        'type' in message
        and 'name' in message
        and 'command_id' in message
    )

def controller(channel, method, properties, message):
    message = loads(message)
    browser = BrowserQueueCommand(message["browser_id"])
    if is_message_valid(message):
        message = {
            "type": "command_status",
            "command_id": message["command_id"],
            "status": "not accepted",
        }
    else:
        message = {
            "type": "command_status",
            "command_id": message["command_id"],
            "status": "syntax error",
        }
    browser.send_message(message)
    print('ToBrowser:', message)
