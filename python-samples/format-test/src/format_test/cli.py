import click

from format_test.format_func import format_run, pre_format_run
from format_test.fstring_func import fstring_run
from format_test.logging_func import logging_run
from format_test.percent_func import percent_run, pre_percent_run
from format_test.plus_func import plus_run
from format_test.template_func import template_run


@click.command()
@click.option("-n", "--num", type=click.IntRange(1), default=10000000)
def cli(num):
    click.echo(f"run script {num=}")
    format_run(num)
    fstring_run(num)
    percent_run(num)
    pre_format_run(num)
    pre_percent_run(num)
    logging_run(num)
    plus_run(num)
    template_run(num)
