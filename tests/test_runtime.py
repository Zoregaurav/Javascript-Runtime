from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class JavaScriptRuntimeTests(unittest.TestCase):
    def run_js(self, source: str) -> str:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
            handle.write(textwrap.dedent(source).strip() + "\n")
            path = Path(handle.name)
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "main.py"), str(path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout.strip()
        finally:
            path.unlink(missing_ok=True)

    def test_odd_even_checker(self):
        self.assertEqual(self.run_js("let n = 7; console.log(n % 2 == 0 ? 'even' : 'odd');"), "odd")

    def test_triangle_pattern(self):
        self.assertEqual(
            self.run_js("""
                for (let i = 1; i <= 3; i++) {
                  let row = "";
                  for (let j = 0; j < i; j++) row += "*";
                  console.log(row);
                }
            """),
            "*\n**\n***",
        )

    def test_armstrong_number(self):
        self.assertEqual(
            self.run_js("""
                let n = 153;
                let x = n;
                let sum = 0;
                while (x > 0) {
                  let d = x % 10;
                  sum += d ** 3;
                  x = Math.floor(x / 10);
                }
                console.log(sum == n);
            """),
            "true",
        )

    def test_array_reverse(self):
        self.assertEqual(self.run_js("const a = [1,2,3]; console.log(a.reverse().join('-'));"), "3-2-1")

    def test_palindrome_checker(self):
        self.assertEqual(
            self.run_js("""
                const word = "level";
                const rev = word.split("").reverse().join("");
                console.log(word === rev);
            """),
            "true",
        )

    def test_function_declaration(self):
        self.assertEqual(self.run_js("function add(a,b){ return a+b; } console.log(add(2,3));"), "5")

    def test_arrow_function_expression_body(self):
        self.assertEqual(self.run_js("const mul = (a,b) => a*b; console.log(mul(4,5));"), "20")

    def test_function_expression_callback(self):
        self.assertEqual(self.run_js("const xs=[1,2,3]; console.log(xs.map(function(x){return x+1;}).join(','));"), "2,3,4")

    def test_filter_callback(self):
        self.assertEqual(self.run_js("console.log([1,2,3,4].filter(x => x % 2 === 0).join(','));"), "2,4")

    def test_reduce_callback(self):
        self.assertEqual(self.run_js("console.log([1,2,3,4].reduce((a,b)=>a+b, 0));"), "10")

    def test_for_each_callback(self):
        self.assertEqual(self.run_js("let s=0; [1,2,3].forEach(x => { s += x; }); console.log(s);"), "6")

    def test_array_push_pop_shift_unshift(self):
        self.assertEqual(
            self.run_js("const a=[2]; a.push(3); a.unshift(1); console.log(a.pop(), a.shift(), a.join(','));"),
            "3 1 2",
        )

    def test_array_slice_and_length(self):
        self.assertEqual(self.run_js("const a=[1,2,3,4]; console.log(a.slice(1,3).join(','), a.length);"), "2,3 4")

    def test_string_methods(self):
        self.assertEqual(
            self.run_js("const s=' hello '; console.log(s.trim().toUpperCase().replace('H','J'));"),
            "JELLO",
        )

    def test_string_predicates(self):
        self.assertEqual(self.run_js("console.log('startup'.includes('art'), 'js'.startsWith('j'), 'js'.endsWith('s'));"), "true true true")

    def test_string_substring_slice(self):
        self.assertEqual(self.run_js("console.log('abcdef'.substring(1,4), 'abcdef'.slice(2,5));"), "bcd cde")

    def test_object_creation_and_member_update(self):
        self.assertEqual(self.run_js("const user={name:'Gaurav', age:21}; user.age=22; console.log(user.name, user.age);"), "Gaurav 22")

    def test_nested_objects(self):
        self.assertEqual(self.run_js("const x={a:{b:9}}; console.log(x.a.b);"), "9")

    def test_spread_arrays_and_objects(self):
        self.assertEqual(self.run_js("const a=[1,2]; const b=[0,...a,3]; const o={x:1}; const p={...o,y:2}; console.log(b.join(','), p.x+p.y);"), "0,1,2,3 3")

    def test_math_builtins(self):
        self.assertEqual(self.run_js("console.log(Math.floor(2.8), Math.ceil(2.1), Math.round(2.5), Math.abs(-4), Math.max(1,5), Math.min(1,5));"), "2 3 3 4 5 1")

    def test_type_conversion(self):
        self.assertEqual(self.run_js("console.log(Number('42') + 1, String(99), Boolean('x'), parseInt('12px'), parseFloat('1.5kg'));"), "43 99 true 12 1.5")

    def test_if_else_if_else(self):
        self.assertEqual(self.run_js("let x=2; if(x===1) console.log('one'); else if(x===2) console.log('two'); else console.log('other');"), "two")

    def test_while_loop_break_continue(self):
        self.assertEqual(
            self.run_js("""
                let i=0; let out="";
                while (i < 5) {
                  i++;
                  if (i == 2) continue;
                  if (i == 5) break;
                  out += String(i);
                }
                console.log(out);
            """),
            "134",
        )

    def test_closure_scope(self):
        self.assertEqual(
            self.run_js("function makeAdder(a){ return function(b){ return a+b; }; } const add2=makeAdder(2); console.log(add2(5));"),
            "7",
        )

    def test_date_builtins(self):
        output = self.run_js("const d = new Date(); console.log(Date.now() > 0, d.toString().length > 0);")
        self.assertEqual(output, "true true")


if __name__ == "__main__":
    unittest.main()
