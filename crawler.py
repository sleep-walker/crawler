#!/usr/bin/python -u

import click
import requests
import urlparse
from lxml import html, etree
from subprocess import call
from shlex import split


def call_cmd(cmd, text):
    '''
    Call external command and replace '{}' with the text(s) obtained via XPath.
    '''

    c = []
    for x in split(cmd):
        if x == '{}':
            for t in text:
                c.append(t)
        else:
            c.append(x)
    call(c)


def print_part(text):
    '''
    Print part of the page which was obtained via XPath.
    '''
    for t in text:
        print(t)


def crawl_page(url, next_=[], print_=[], action_=[]):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    next_urls = set()
    for p in next_:
        urls = tree.xpath(p)
        if urls:
            new_urls = []
            for u in urls:
                if not u.startswith('http'):
                    new_urls.append(urlparse.urljoin(url, u))
                else:
                    new_urls.append(u)
                next_urls.update(new_urls)

    for p in print_:
        print_part(tree.xpath(p))

    for p, cmd in action_:
        call_cmd(cmd, tree.xpath(p))

    return next_urls


@click.command()
@click.version_option(version='0.1')
@click.option('--next', '-n', multiple=True,
              help=('XPath pointing to URL to follow while it matches'))
@click.option('--print', '-p', multiple=True,
              help=('XPath pointing to region which should be printed to '
                    'screen'))
@click.option('--action', '-a', nargs=2, type=(str, str), multiple=True,
              help=('XPath (first parameter) pointing to region which should '
                    'be passed to a command (second parameter). Use \'{}\' to '
                    'indicate positions, wher it should be replaced.'))
@click.option('--silent', '-s', is_flag=True,
              help='do not print any output')
@click.argument('url', nargs=-1)
def main(**kwargs):
    stack = [u for u in kwargs['url']]

    visited = set()
    next_ = kwargs['next']
    print_ = kwargs['print']
    action_ = kwargs['action']
    silent = kwargs['silent']
    while stack:
        url = stack.pop(0)
        if not silent:
            click.echo("url (%d/%d): %s" % (
                len(visited) + 1,
                len(visited) + len(stack) + 1,
                str(url)
            ))

        if url in visited:
            continue

        new_next = crawl_page(
            url,
            next_=next_,
            print_=print_,
            action_=action_
        )

        visited.add(url)

        if new_next:
            stack.extend(new_next)


if __name__ == '__main__':
    main()
