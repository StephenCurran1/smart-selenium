"""Helper methods common to all api entry points"""
import uuid
import functools
import datetime
import os
import rapidjson
from flask import g
from flask import Response
from flask import json
from ..lib import logger
from ..lib import constants as SMART_SELENIUM


def no_handler():
    err = error_message(SMART_SELENIUM.ERRORS['CHANNEL_NOT_SUPPORTED'],
                        'Channel is not supported')
    return failure([err], status_code=400)


def error_message(code, msg, field=''):
    return {
        'code': code,
        'message': msg,
        'field': field
    }


def success(data, status_code=200, **kwargs):  # pragma: no cover
    _resp = {
        'status': kwargs.get('status', 'success'),
        'data': data,
        'message': kwargs.get('message', '')
    }

    return Response(json.dumps(_resp), status_code)


def failure(data, status_code=400, **kwargs):  # pragma: no cover
    _resp = {
        'status': kwargs.get('status', 'error'),
        'errors': data,
        'message': kwargs.get('message', '')
    }

    return Response(json.dumps(_resp), status_code)


def _response_from_dict(_resp, status_code, **kwargs):
    json = rapidjson.dumps(_resp, datetime_mode=rapidjson.DM_ISO8601 | rapidjson.DM_NAIVE_IS_UTC,
                           number_mode=rapidjson.NM_DECIMAL)

    return Response(json, mimetype='application/json', status=status_code)


def generate_id():
    return uuid.uuid4()


def missing_fields_response(fields):
    errors = [error_message(SMART_SELENIUM.ERRORS['MISSING_REQUIRED'],
                            'Missing required field',
                            field=field)
              for field in fields]
    return failure(errors)


def validation(*required_args):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            missing = [k for k in required_args if k not in g.params]
            if missing:
                return missing_fields_response(missing)
            return f(*args, **kwargs)

        return wrapper

    return decorator

