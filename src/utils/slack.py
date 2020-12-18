from shared_utils.api.slack.core import post_to_slack


def slack_status(message):
    post_to_slack('status', message)


def slack_error(message):
    post_to_slack('errors', message)


def slack_message(message):
    post_to_slack('messages', message)


def slack_callback(message):
    post_to_slack('callbacks', message)
