from string import Template
from format_test.decorators import benchmark


@benchmark
def template_run(num: int = 100):
    t = Template("text $num and $text")
    for i in range(num):
        t.substitute({'num': i, 'text': 'text'})
