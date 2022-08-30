from format_test.decorators import benchmark


@benchmark
def fstring_run(num: int = 100):
    _text = "text"
    for i in range(num):
        f"test {i} and {_text}"
