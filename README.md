# ExpressionEvaluator

A project I made a few years ago that takes a math expression and finds the answer, without using any third party libraries or eval().
I keep coming back to it to use it in my projects and improving it so I decided to put it on GitHub so other people can to.

To use, just call `evaluate_string(input)` on your string expression.
Although I don't see any reason to, it's also possible to separately call `format_string(input)` and `evaluate(formatted_string)` and get the same result. Infact, the `evaluate_string` code is:
```
def evaluate_string(string):
        formatted_equation = format_string(string)
        return evaluate(formatted_equation)
```

The possible exceptions it should be able to raise are: ExpressionEvaluator.ZeroDivision, ExpressionEvaluator.EquationSyntaxError, ExpressionEvaluator.UnknownCharacter, ExpressionEvaluator.TooBigNumber, and OverflowError
