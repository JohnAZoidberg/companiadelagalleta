# coding=utf-8
import json
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

country_list = OrderedDict([
    ('??', "Desconocido"),
    ('de', "Alemania"),
    ('es', "Espana"),
    ('canario', "Islas Canarias"),
    ('ne', "Paíes Bajos"),
    ('gb', "Gran Bretana"),
    ('us', "EE.UU."),
    ('it', "Itala"),
    ('fr', "Francia"),
    ('no', "Noruega"),
    ('xx', "Otro")
])

def print_header(t="text/html"):
    print "Content-Type: "+ t + ";charset=utf-8"
    print


def print_html_header(title, css=None):
    print '<html>'
    print '<head>'
    print '<meta name="viewport" content="width=device-width, initial-scale=1">'
    print '<title>' + title + '</title>'
    if css is not None:
        print '<style>' + css + '</style>'
    print '</head>'
    print '<body>'


def print_html_footer():
    print '</body>'
    print '</html>'


def println(*lns):
    for ln in lns:
        print ln
    print "<br>"
