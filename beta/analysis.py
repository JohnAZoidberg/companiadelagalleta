#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()
import cg
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
    
cg.print_header()
cg.print_html_header()
cg.println('<a href="index.py">Add</a>')

purchases = cg.load_purchases()['purchases']

country_pop = OrderedDict((str(x), {str(y): 0 for y in xrange(1, len(cg.country_list)+1)}) for x in xrange(0, len(cg.cookie_list)))
cookie_pop = OrderedDict((str(x), 0) for x in xrange(0, len(cg.cookie_list)))
for p in purchases:
    for cookie in p['cookies']:
        cookie_pop[cookie] += 1
        country_pop[cookie][p['country']] += 1
for key, val in cookie_pop.iteritems():
    cg.println(str(val) + ': ' + cg.cookie_list[key])
print '<hr>'
print '<ul>'
for cookie_key, val in country_pop.iteritems():
    print '<li>' + cg.cookie_list[cookie_key] + '</li>'
    print '<ul>'
    for country_key, count in val.iteritems():
        print '<li>'
        print str(count) + ": " + cg.country_list[str(country_key)]
        print '</li>'
    print '</ul>'
print '</ul>'
cg.print_html_footer()
