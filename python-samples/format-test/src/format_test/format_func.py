from format_test.decorators import benchmark


@benchmark
def format_run(num: int = 100):
    for i in range(num):
        "test {} and {}".format(i, "text")


@benchmark
def pre_format_run(num: int = 100):
    text = "test {} and {}"
    for i in range(num):
        text.format(i, "text")
