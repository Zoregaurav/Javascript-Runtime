# Thunder JS Runtime

A clean, from-scratch JavaScript runtime and interpreter written in Python for Thunder Hackathon 2.0. It reads JavaScript source from a file, tokenizes it, parses it into an AST, and executes that AST using a scoped runtime environment. It does not call Node.js, V8, Deno, Bun, QuickJS, or any external JavaScript engine.

## Architecture

```text
source.js
   |
   v
lexer.py        -> tokens
   |
   v
parser.py       -> ast_nodes.py
   |
   v
interpreter.py  -> environment.py -> runtime.py
   |
   v
builtins.py     -> console.log output
```

## Project Layout

```text
project/
├── main.py
├── lexer.py
├── parser.py
├── ast_nodes.py
├── interpreter.py
├── environment.py
├── runtime.py
├── builtins.py
├── tests/
└── README.md
```

## Supported Features

- Variables: `let`, `const`, `var`
- Arithmetic: `+`, `-`, `*`, `/`, `%`, `**`
- Comparison: `==`, `===`, `!=`, `!==`, `<`, `>`, `<=`, `>=`
- Logical operators: `&&`, `||`, `!`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- Updates: `++`, `--`
- Conditionals: `if`, `else if`, `else`
- Loops: `while`, `for`, `break`, `continue`
- Functions: declarations, function expressions, arrow functions, callbacks, closures, `return`
- Arrays: literals, indexing, `length`, `push`, `pop`, `shift`, `unshift`, `reverse`, `join`, `slice`, `map`, `filter`, `reduce`, `forEach`
- Strings: `length`, indexing, `split`, `substring`, `slice`, `includes`, `startsWith`, `endsWith`, `toUpperCase`, `toLowerCase`, `trim`, `replace`
- Objects: literals, nested objects, dot access, bracket access, property updates
- Built-ins: `console.log`, `Math.floor`, `Math.ceil`, `Math.round`, `Math.abs`, `Math.max`, `Math.min`, `Math.random`, `new Date()`, `Date.now()`
- Spread: array spread, object spread, spread call arguments
- Type conversion: `Number`, `String`, `Boolean`, `parseInt`, `parseFloat`

## How To Run

```bash
python main.py sample.js
```

Example:

```javascript
function add(a, b) {
  return a + b;
}

const values = [1, 2, 3];
console.log(add(2, 5));
console.log(values.map(x => x * 2).join(","));
```

Output:

```text
7
2,4,6
```

## Tests

Run the Python test suite:

```bash
python -m unittest discover -s tests
```

The suite covers the required showcase programs:

- Odd Even Checker
- Triangle Pattern
- Armstrong Number
- Array Reverse
- Palindrome Checker

It also includes 20 additional edge-case tests for callbacks, closures, array methods, string methods, objects, spread, loops, Math, Date, and conversions.

## Design Notes

The interpreter uses a direct `evaluate(node, env)` dispatch model. Each AST node maps to a dedicated evaluator method, keeping parser concerns separate from runtime execution. Environments form a parent-linked scope chain, so nested blocks and functions can resolve variables through lexical scope.

Built-ins are implemented as Python-native runtime values exposed through the same call protocol as user-defined JavaScript functions. Array and string methods are bound dynamically from member access, which allows expressions such as `arr.map(x => x * 2).join(",")`.

## Limitations

This is a focused educational runtime, not a full ECMAScript implementation. It intentionally omits modules, classes, prototypes, async/await, promises, regular expressions, destructuring, template literals, `this`, `try/catch`, and full automatic semicolon insertion.

## Future Improvements

- Add a richer ECMAScript conformance test suite
- Implement prototypes and `this`
- Add destructuring and rest parameters
- Support template literals and regular expressions
- Improve diagnostics with source snippets
- Add bytecode compilation as a second execution backend

## 📸 Screenshots

![Homepage](https://github.com/Zoregaurav/Javascript-Runtime/blob/f3ea036f04838254f329fc3022ae75f53698cc9c/Screenshot%202026-06-15%20000625.png)
![Homepage]()

