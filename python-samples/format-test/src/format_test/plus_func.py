from format_test.decorators import benchmark


@benchmark
def plus_run(num: int = 100):
    for i in range(num):
        "test" + str(i) + "and" + "text"
