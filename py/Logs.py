import os
import time
from datetime import datetime
import traceback
from inspect import stack


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
            stacktrace=''.join(traceback.format_exception(exception))
        )

    def log_system_exception(self, exception: Exception):
        self._log(
            str(exception), sep="", severity=6,
            exception_type=type(exception).__name__,
            stacktrace=''.join(traceback.format_exception(exception))
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


def call_with_logs(f: callable, logger: Logger) -> any:
    logger.log_info(f"{f.__name__} called")
    ret_val = f()
    logger.log_info(f"{f.__name__} ended")
    return ret_val


def retry(
        f: callable, logger: Logger | None = None,
        expected_val: any = None,
        retry_action: callable = lambda: None,
        retry_delay: float = 0, max_retries: int = 3
) -> any:
    retries = 0
    while True:
        try:
            ret_val = f()
            if expected_val is not None and ret_val != expected_val:
                raise Exception("Unexpected value")
            return ret_val
        except Exception as e:
            if retries >= max_retries:
                raise e
            retry_action()
            if logger is not None:
                logger.log_exception(e)
            retries += 1
            time.sleep(retry_delay)
            print(f"Retrying: {retries}")


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
    return


if __name__ == "__main__":
    main()
