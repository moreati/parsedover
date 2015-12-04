local lpeg = require "lpeg"

brackets_pattern = lpeg.P{ "(" * ((1 - lpeg.S"()") + lpeg.V(1))^0 * ")" }
brackets_capture = lpeg.C(brackets_pattern)

print(brackets_pattern:match("(foo(bar()baz))")) -- prints 16
print(brackets_capture:match("(foo(bar()baz))")) -- prints (foo(bar()baz))


local re = require "re"

brackets_pattern = re.compile(' balanced <- "(" ([^()] / balanced)* ")" ')
brackets_capture = re.compile('{balanced <- "(" ([^()] / balanced)* ")"}')

print(brackets_pattern:match("(foo(bar()baz))")) -- prints 16
print(brackets_capture:match("(foo(bar()baz))")) -- prints (foo(bar()baz))

