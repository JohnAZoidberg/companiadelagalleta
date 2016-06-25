# coding=utf-8
import json
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

blanco = " Chocolate Blanco"
negro  = " Chocolate Negro"
leche  = " Chocolate con Leche"
list_cookies = [
	"Galletas a la carta - 10",
	"Galletas a la carta - 20",
	"Galletas a la carta - 30",
	"Basic bag pequeña - Mix",
	"Basic bag pequeña - Frutas Tropicales",
	"Basic bag pequeña - Sabores de Canarias",
	"Basic bag pequeña - Chocolate",
	"Basic bag pequeña - Clásica",
	"Basic bag grande - Mix",
	"Basic bag grande - Frutas Tropicales",
	"Basic bag grande - Sabores de Canarias",
	"Basic bag grande - Chocolate",
	"Basic bag grande - Clásica",
	"Cube box pequeña - Mix",
	"Cube box pequeña - Frutas Tropicales",
	"Cube box pequeña - Sabores de Canarias",
	"Cube box pequeña - Chocolate",
	"Cube box pequeña - Clásica",
	"Cube box grande - Mix",
	"Cube box grande - Frutas Tropicales",
	"Cube box grande - Sabores de Canarias",
	"Cube box grande - Chocolate",
	"Cube box grande - Clásica",
	"Pyramid window box pequeña - Mix",
	"Pyramid window box pequeña - Frutas Tropicales",
	"Pyramid window box pequeña - Sabores de Canarias",
	"Pyramid window box pequeña - Chocolate",
	"Pyramid window box pequeña - Clásica",
	"Elegant box 1 verde Mix",
	"Elegant box 1 verde Chocolate",
	"Elegant box 1 verde Baño de chocolate",
	"Elegant box 1 crema Mix",
	"Elegant box 1 crema Frutas tropicales",
	"Elegant box 1 crema Sabores de Canarias",
	"Elegant box 2 verde Mix",
	"Elegant box 2 verde Chocolate",
	"Elegant box 2 verde Baño de chocolate",
	"Elegant box 2 verde Excelencia",
	"Elegant box 2 crema Mix",
	"Elegant box 2 crema Frutas tropicales",
	"Elegant box 2 crema Sabores de Canarias",
	"Elegant box 2 crema Clasica",
	"Elegant box 3 verde Mix",
	"Elegant box 3 verde Chocolate",
	"Elegant box 3 verde Baño de chocolate",
	"Elegant box 3 verde Excelencia",
	"Elegant box 3 crema Mix",
	"Elegant box 3 crema Frutas tropicales",
	"Elegant box 3 crema Sabores de Canarias",
	"Elegant box 3 crema Clasica",
	"Strelitzia box - Mix",
	"Strelitzia box - Sabores de Canarias",
	"Mango box - Mix",
	"Mango box - Excelencia",
	"Plumeria box - Excelencia",
        "Galleta individual"
]
cookie_list = OrderedDict((str(i+1), list_cookies[i]) for i in xrange(len(list_cookies)))
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
save_file = 'purchases.txt'

def print_header():
    print "Content-Type: text/html;charset=utf-8"
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


def load_purchases():
    try:
        with open(save_file, 'r') as f:
            purchases = json.load(f)
    except (IOError, ValueError):
        purchases = {"purchases": []}
    return purchases
