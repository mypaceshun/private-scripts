import click

from threading_test import __name__, __version__
from threading_test.simple_threading import run as simple_run
from threading_test.threadpool import run as threadpool_run


@click.group()
@click.version_option(version=__version__, package_name=__name__)
@click.help_option("-h", "--help")
@click.option("-v", "--verbose", is_flag=True, help="verbose output")
@click.pass_context
def cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose


@cli.command()
@click.version_option(version=__version__, package_name=__name__)
@click.help_option("-h", "--help")
@click.option("-v", "--verbose", is_flag=True, help="verbose output")
@click.pass_context
def simple(ctx, verbose):
    simple_run()


@cli.command()
@click.version_option(version=__version__, package_name=__name__)
@click.help_option("-h", "--help")
@click.option("-v", "--verbose", is_flag=True, help="verbose output")
@click.pass_context
def threadpool(ctx, verbose):
    threadpool_run()
