# YARP
YARP - Yet Another Recursive Parser

YARP provides a framework for easily creating recursive parsers in Python. Hand-built parsers are fast, flexible, and allow easy error detection and reporting when compared to parser generators that use EBNF.

Two examples of parsers created with YARP are provided in the examples directory.

## JSON parsing example

### Getting started

To create a parser, start by extending the Parser class. Use the @lexemes annotation to set the expected lexemes for the rule (and all rules until the lexemes are redefined).

```python
json_lexemes = {'{', '}', ',', '[', ']', ':', 'true', 'false', 'null', '"', '\\'}
class JSONParser(Parser):

@lexemes(json_lexemes)
def parse(self):
    super().parse()
    self.value() #parse a json value
```

### AST production rules

Rules that add nodes to the abstract syntax tree can be created using the @ast annotation. The rule below will parse the lexeme 'true' and add a node to the AST. If this rule is encountered and a token mismatch occurs, a syntax error will be printed along with information about where in the token stream it occurred. Note that the @ast annotation also allows for optional rules with the 'optional' parameter.

```python
@ast("true", require=['true'], description="boolean")
def true_val(self, tokens):
    pass
```

### Pattern matching

You can match patterns forward into the token stream without consuming tokens. This is essentially the lookahead functionality from other parser generators.

```python
@ast("array", require=['['], description="array")
def json_array(self, tokens):
    self.consume_whitespace()
    while (not self.match_pattern(']')):
        self.value()
        self.accept(',')
    self.accept(']')
```

### Rules with alternatives

Rules with alternatives can be added using the parse_alternatives function. This uses pattern matching (of one or more tokens) to determine which production rule to use. If no alternative is valid, then a syntax error will occur with the provided description of what was expected.

```python
@ast("value")
def value(self):
    self.consume_whitespace()
    self.parse_alternatives([(['{'], self.json_object),
                             (['['], self.json_array),
                             (['"'], self.string),
                             (['true'], self.true_val),
                             (['false'], self.false_val),
                             (['null'], self.null_val),
                             ([RegularExpression(NUMBER_REGEX)], self.number)],
                            "value")
    self.consume_whitespace()
```

