import os
import time
from datetime import datetime
import traceback


class BusinessException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Logger:
    severity_levels = [
        "Trace", "Info",
        "Warning", "Critical", "Error",
        "Business Exception", "System Exception"
    ]
    class Log:
        def __init__(
                self, message: str, severity: str,
                exception_type: str | None = None,
                stacktrace: str | None = None,
                timestamp: datetime | None = None
        ):
            self.timestamp = datetime.now() if timestamp is None else timestamp
            self.message = message
            self.severity = severity
            self.exception_type = exception_type
            self.stacktrace = stacktrace

        def print(self):
            severity_colors = {
                "Trace": "", "Info": "",
                "Warning": "\033[93m", "Critical": "\033[31m", "Error": "\033[30m\033[41m",
                "Business Exception": "\033[30m\033[43m", "System Exception": "\033[30m\033[41m"
            }
            print(f"{severity_colors[self.severity]}{self}\033[0m")

        def __str__(self):  # TODO: add coloring to str based on severity
            ret_string = ""

            ret_string += (self.exception_type + ': ' if self.exception_type is not None else '')
            ret_string += self.message
            ret_string += ('\n' + self.stacktrace if self.stacktrace is not None else '')

            return ret_string

        def __repr__(self):
            ret_string = ""

            ret_string += f"{self.timestamp} - {self.severity}:"
            ret_string += f"\n{self}"

            return ret_string

        def __iter__(self):
            yield "timestamp", self.timestamp.isoformat()
            yield "message", self.message
            yield "severity", self.severity
            yield "stacktrace", self.stacktrace
            yield "exception_type", self.exception_type

    def __init__(self):
        self.logs = []
        self.minimum_print_severity = 1
        self.working_dir = os.getcwd()

    def _log(
            self, *messages: str,
            sep: str = "", severity: int = 1,
            exception_type=None, stacktrace=None
    ):
        log = self.Log(
            sep.join([str(message) for message in messages]),
            self.severity_levels[severity],
            exception_type, stacktrace
        )
        self.logs.append(log)
        if severity >= self.minimum_print_severity:
            log.print()

    def log_trace(self, *messages: str, sep: str = ""):
        self._log(*messages, sep=sep, severity=0 )

    def log_info(self, *messages: str, sep: str = ""):
        self._log(*messages, sep=sep, severity=1)

    def log_warning(self, *messages: str, sep: str = ""):
        self._log(*messages, sep=sep, severity=2)

    def log_critical(self, *messages: str, sep: str = ""):
        self._log(*messages, sep=sep, severity=3)

    def log_error(self, *messages: str, sep: str = ""):
        self._log(*messages, sep=sep, severity=4)

    def log_business_exception(self, exception: Exception):
        self._log(
            str(exception), sep="", severity=5,
            exception_type=type(exception).__name__,
            stacktrace=''.join(traceback.format_exception(exception)).strip()
        )

    def log_system_exception(self, exception: Exception):
        self._log(
            str(exception), sep="", severity=6,
            exception_type=type(exception).__name__,
            stacktrace=''.join(traceback.format_exception(exception)).strip()
        )

    def log_exception(self, exception: Exception):
        if type(exception) is BusinessException:
            self.log_business_exception(exception)
        else:
            self.log_system_exception(exception)

    def to_json(self):
        return [dict(log) for log in self.logs]

    def __len__(self):
        return len(self.logs)

    def __getitem__(self, idx: int):
        return self.logs[idx]

    def __str__(self):
        return "\n".join([str(log) for log in self.logs])

def log_message(
    message: str | Exception, logger: Logger | None = None,
    severity: int = 1, raise_exception: bool | None = None
) -> None:
    """
    :param message: message string or exception to be logged
    :param logger: logger object
    :param severity: severity of message (if not exception)
    :param raise_exception: How exceptions are handled;
        None: bubbles up exceptions only if there is no logger provided;
        True: bubbles up any exception;
        False: never bubbles up exceptions
    :return: None
    """
    if type(message) is str:
        if logger is None:
            print(message)
        else:
            logger._log(message, severity=severity)
        return

    if issubclass(type(message), Exception):
        if raise_exception or (raise_exception is None and logger is None):
            raise message

        if logger is None:
            print(message)
            return

        try:
            raise message
        except Exception as e:
            logger.log_exception(e)
        return

    message_err_str = f"Unknown message type: {type(message).__name__}"
    message_val_err = ValueError(message_err_str)
    if raise_exception or (raise_exception is None and logger is None):
        raise message_val_err

    if logger is None:
        print(message_err_str)
        return

    try:
        raise message_val_err
    except Exception as e:
        logger.log_exception(e)
    return


def call_with_logs(f: callable, logger: Logger) -> any:
    """
    Calls the provided function with wrapping logs to indicate that the function has started or ended
    :param f: function being wrapped
    :param logger: logger object
    :return: the value that is returned by f
    """
    logger.log_info(f"{f.__name__} called")
    ret_val = f()
    logger.log_info(f"{f.__name__} ended")
    return ret_val


def benchmark(
    f: callable, logger: Logger | None = None,
    expected_val: any = None
) -> None:
    """
    A wrapping function timer and value checker for benchmarking the speed and expected i/o of a given function.
    :param f: function being wrapped
    :param logger: logger object
    :param expected_val: value that is expected from the function; None is ignored
    :return: None
    """
    log_message(f"{f.__name__} called", logger=logger)
    begin_time = datetime.now()
    result = f()
    end_time = datetime.now()
    log_message(f"{f.__name__} finished", logger=logger)

    if expected_val is not None and expected_val != result:
        log_message(ValueError(f"'{result}' was not the expected value of '{expected_val}'."), logger=logger)

    log_message(f"{end_time-begin_time} taken to execute", logger=logger)
    return


def retry(
    f: callable, logger: Logger | None = None,
    expected_val: any = None,
    retry_action: callable = lambda: None,
    retry_delay: float = 0, max_retries: int = 3
) -> any:
    """
    Retries any wrapped function in an attempt to avoid bubbling up an error
    :param f: function being wrapped
    :param logger: logger object
    :param expected_val: value that is expected to be returned; None is ignored
    :param retry_action: function executed when a retry is required
    :param retry_delay: delay between retries
    :param max_retries: maximum number of retries before bubbling up error
    :return: the value that is returned by f
    """
    retries = 0
    while True:
        try:
            ret_val = f()
            if expected_val is not None and ret_val != expected_val:
                raise ValueError(f"Unexpected value: {ret_val}")
            return ret_val
        except Exception as e:
            if retries >= max_retries:
                raise e
            retry_action()
            if logger is not None:
                logger.log_exception(e)
            retries += 1
            time.sleep(retry_delay)
            log_message(f"Retrying: {retries}")


system_logger = Logger()


def main():
    system_logger.log_trace("trace")
    system_logger.log_info("info")
    system_logger.log_warning("warning")
    system_logger.log_critical("critical")
    system_logger.log_error("error")

    try:
        raise BusinessException("Business exception")
    except Exception as e:
        system_logger.log_exception(e)

    try:
        raise Exception("System exception")
    except Exception as e:
        system_logger.log_exception(e)

    try:
        print(1/0)
    except Exception as e:
        system_logger.log_exception(e)

    try:
        print(3 + "x")
    except Exception as e:
        system_logger.log_exception(e)

    log_message("Log this")
    log_message("Log this with the logger", logger=system_logger)
    log_message("Log this, again", raise_exception=True)
    log_message(UserWarning("Throw this"), logger=system_logger)
    log_message(2, logger=system_logger)
    log_message(2.0, raise_exception=False)
    # log_message(Exception("Throw this, too"), logger=system_logger, raise_exception=True)

    print(system_logger)
    return


if __name__ == "__main__":
    main()
