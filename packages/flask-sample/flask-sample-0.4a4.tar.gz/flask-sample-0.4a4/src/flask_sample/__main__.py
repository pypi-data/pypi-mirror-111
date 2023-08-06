#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import click
import shutil
from flask_sample.app import STATIC_DIR


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
def static(path):
    """
    Collect and save static files
    """
    click.echo(path)
    shutil.copytree(src=STATIC_DIR, dst=path)


if __name__ == '__main__':
    cli()
