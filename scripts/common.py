import time
import datetime

class color:
    HEADER = '\033[95m'
    DEBUG = '\033[94m'  # blue
    SUCCESS = '\033[92m'  # green
    WARNING = '\033[93m'  # yellow
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        pass

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def start(str):
    print(color.BOLD + "[%s] > %s" % (timestamp(), str) + color.ENDC)

def finish(isSuccess, str):
    if (isSuccess):
        print(color.BOLD + color.SUCCESS + "[%s] < [+] %s: PASSED" % (timestamp(), str) + color.ENDC)
    else:
        print(color.BOLD + color.FAIL + "[%s] < [-] %s: FAILED" % (timestamp(), str) + color.ENDC)

def startTest(test_name):
    print(color.BOLD + "[%s] > Starting %s test..." % (timestamp(), test_name) + color.ENDC)

def finishTest(test_name, isSuccess, test_start_time=None):
    if (isSuccess):
        print()
        print("-" * 79)
        print(color.BOLD + color.SUCCESS + "[%s] < [+] Test '%s' overall result: PASSED" % (timestamp(), test_name) + color.ENDC)
        if (test_start_time != None):
            print(color.BOLD + "Test execution time is %s seconds" % (round(time.time() - test_start_time, 1)))
    else:
        print(color.BOLD + color.FAIL + "[%s] < [-] Test '%s' overall result: FAILED" % (timestamp(), test_name) + color.ENDC)
        if (test_start_time != None):
            print(color.BOLD + "Test execution time is %s seconds" % (round(time.time() - test_start_time, 1)) + color.ENDC)

def success(str):
    print(color.SUCCESS + "[%s] [+] %s: Passed" % (timestamp(), str) + color.ENDC)

def fail(str):
    print(color.FAIL + "[%s] [-] %s: Failed" % (timestamp(), str) + color.ENDC)

def info(str):
    print("[%s] [.] %s" % (timestamp(), str))

def debug(str):
    print(color.DEBUG + "[%s] [.] %s" % (timestamp(), str) + color.ENDC)

def warning(str):
    print(color.WARNING + "[%s] [.] %s" % (timestamp(), str) + color.ENDC)
