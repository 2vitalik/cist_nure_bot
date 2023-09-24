import conf
from src.utils.slack import slack_exception
from src.utils.tg import tg_send


def errors(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            from shared_utils.conf import conf as shared_conf
            shared_conf.slack_hooks = conf.slack_hooks

            try:
                return func(*args, **kwargs)
            except Exception as e:
                message = f'<code>{slug}</code>\n' \
                          f'⚠️ <b>{type(e).__name__}</b>: {str(e)}'
                slack_exception(slug, e)
                tg_send(conf.telegram_admin, message)
                raise
        return wrapped
    return decorator
