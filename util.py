from click import BadArgumentUsage
from flask import jsonify
import functools
import logging
import werkzeug.exceptions as ex

log = logging.getLogger()

def handle_exception(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            return view(**kwargs)
        except ex.HTTPException as e:
            raise e
        except Exception as e:
            log.exception('exception in http request')
            return jsonify({'status': f'server error: {e.args}'}), 500

    return wrapped_view