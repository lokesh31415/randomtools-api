import os
from datetime import datetime

default_path = os.environ.get("RAND_LOG_PATH", "logs")
_filename = "randlog.log"
_enable_print = os.environ.get("RAND_LOGPRINT_ENABLE", "y") == "y"

# private functions
def _get_datetime_iso():
    return datetime.now().replace(microsecond=0).isoformat()

def _format_msg(msg_type:str, msg: str):
    return f"{msg_type}({_get_datetime_iso()}): {msg}"

def _write_log(log_msg):
    # create the file path if not available
    if not os.path.isdir(default_path): os.makedirs(default_path)
    # get full path and log into the log file
    full_path = os.path.join(default_path, _filename)
    with open(full_path, 'a') as f:
        f.write(log_msg + "\n")
    if _enable_print: print(log_msg + "\n")

# public APIs
def exception(msg:str):
    """
    To Log Exceptions message.
    """
    log_msg = _format_msg(msg_type='Exception', msg=msg)
    _write_log(log_msg=log_msg)


def error(msg:str):
    """
    To Log an Error message.
    """
    log_msg = _format_msg(msg_type='Error', msg=msg)
    _write_log(log_msg=log_msg)


def warning(msg:str):
    """
    To Log a Warning.
    """
    log_msg = _format_msg(msg_type='Warning', msg=msg)
    _write_log(log_msg=log_msg)


def message(msg:str):
    """
    To Log a Message.
    """
    log_msg = _format_msg(msg_type='Message', msg=msg)
    _write_log(log_msg=log_msg)

