from __future__ import print_function

import sys

# Excluded or unsuccessful attempts
# grako     requires seperate code generation step
# pwpeg
# speg
# peglet
# pyrser
# glop      mentions OMeta and LPeg, but I can't work out how to call it
# ply
# rply

s = '(foo(bar()baz))'

import regex
# https://nikic.github.io/2012/06/15/The-true-power-of-regular-expressions.html
# https://stackoverflow.com/questions/26385984/recursive-pattern-in-regex
pattern = regex.compile(r'\( (?> [^()]+ | (?R) )* \)', regex.VERBOSE)
print('regex:', pattern.match(s).group(0))

pattern = regex.compile(r'(?<balanced> \( (?> [^()]+ | (?&balanced) )* \) )',
                        regex.VERBOSE)
print('regex:', pattern.match(s).group('balanced'))


from _ppeg import Pattern as P
pattern = P.Grammar("(" + (1-P.Set("()")**1 | P.Var(0))**0 + ")")
capture = P.Cap(pattern)
# import pe
# pattern = pe.compile(' balanced <- "(" ([^()] / balanced)* ")" ')
# capture = pe.compile('{balanced <- "(" ([^()] / balanced)* ")"}')
print('_ppeg:', pattern(s).pos)
print('_ppeg:', capture(s).captures)


import parsley # MIT, based on OMeta, pure python
brackets = parsley.makeGrammar("balanced = '(' (~('(' | ')') anything | balanced)* ')'", {})
capture = parsley.makeGrammar("balanced = <'(' (~('(' | ')') anything | balanced)* ')'>", {})

print('parsley:', brackets(s).balanced())
print('parsley:', capture(s).balanced())


sys.path.append('esrapy')
import esrapy # GPL, pure python, not pip installable
pattern = esrapy.compile("balanced = '(' (<[^()]+> | balanced)* ')'")
print('esrapy:', pattern.match(s))


import pyparsing # MIT
pattern = pyparsing.nestedExpr('(', ')', ignoreExpr=None)
print('payparsing:', pattern.parseString(s))


import simpleparse.parser # BSD, bundles mxTextTools under mxLicense
parser = simpleparse.parser.Parser("balanced := '(', (-[()]+ / balanced)*, ')'",
                                   root='balanced')
print('simpleparse:', parser.parse(s)) # some sort of result tree

#import arpeggio
#def balanced():
#    return '(', arpeggio.ZeroOrMore([arpeggio.Not(['(', ')']), balanced]), ')'
#parser = arpeggio.ParserPython(balanced)
#print('arpeggio:', parser.parse(s))

#import pypeg
# Subclass a load of primitives, sod that

#import spark
# http://pages.cpsc.ucalgary.ca/~aycock/spark/

import parsimonious # MIT, Pure Python
grammar = parsimonious.Grammar('balanced = "(" ( ~"[^()]+" / balanced )* ")"')
print('parsimonious:', grammar.parse(s))

import peglet # GPL
parser = peglet.Parser(r'balanced = \( ([^()]+ | balanced)* \) ')
# AFAICT peglet doesn't support referring to rules inside a capture
# (balanced) matches/returns the string 'balanced', not the rule
#print(parser(s)) # sre_constants.error: unbalanced parenthesis

import parson # GPL
grammar = parson.Grammar("balanced : '(' ( /[^()]+/ | balanced )* ')'.")
parser = grammar()
print('parson:', parser.balanced(s))
print('parson:', parson.capture(parser.balanced)(s))
# The curly braces denote capture
grammar = parson.Grammar("balanced : '(' { /[^()]+/ | balanced }* ')'.")
parser = grammar()
print('parson:', parser.balanced(s))
grammar = parson.Grammar("balanced : {'(' ( /[^()]+/ | balanced )* ')'}.")
parser = grammar()
print('parson:', parser.balanced(s))

#import pyrser
#"balanced = ['('  [ [~['(' | ')']]+ | balanced ] ')']"
# requires subclassing

from rpython.rlib import parsing


