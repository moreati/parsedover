import
    pegs

const s = "(foo(bar()baz))"

# From http://nim-lang.org/docs/pegs.html#peg-syntax-and-semantics
#
#  .    Any character: If there is a character ahead, consume it and indicate
#       success. Otherwise (that is, at the end of input) indicate failure.
#
#  _    Any Unicode character: If there is an UTF-8 character ahead, consume
#       it and indicate success. Otherwise indicate failure.
#
# I think, but have not verified
#   - "character" in nim-speak means byte
#   - Nim's string type is a byte string, with strong (enforced?)
#     support/convention that anything textual must be UTF-8 encoded

proc main() =
    var
        pattern = peg"balanced <- '(' (![()] . / balanced)* ')'"
        capture = peg"balanced <- {'(' (![()] . / balanced)* ')'}"
        # Currently (Nov 2015) MaxSubpatterns==20,
        # Is this a hard limit on number of captures with .match()?
        captures: array[pegs.MaxSubpatterns, string]

    echo(s.match(pattern))
    echo(s.match(capture, captures))
    echo(repr(captures))

when isMainModule:
    main()

# To run this: nim compile -r fred.nim
