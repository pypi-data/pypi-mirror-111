from celtis.Config import __version__
import click, sys, click_log
from celtis.Target import Target
from celtis.Logger import logger
from celtis.Scanner import Scanner

@click.version_option(__version__)
@click.group()
def cli():
    return Cli()

class Cli:
    def __init__(self):
        pass

    @cli.command()
    @click_log.simple_verbosity_option(logger)
    @click.option('-u', '--url', default='', type=str)
    @click.argument('targets', default=sys.stdin, type=click.File('r'))
    def scan(url, targets):
        """Scan a url or several targets from a file or standard input."""
        if(url):
            targets = [url]
        scanner = Scanner(Target(targets), 3)
        scanner.loop()

