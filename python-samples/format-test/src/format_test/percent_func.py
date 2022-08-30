from format_test.decorators import benchmark


@benchmark
def percent_run(num: int = 100):
    for i in range(num):
        "test %d and %s" % (i, "text")


@benchmark
def pre_percent_run(num: int = 100):
    text = "test %d and %s"
    for i in range(num):
        text % (i, "text")
