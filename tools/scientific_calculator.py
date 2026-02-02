import math
import argparse

# Try importing readline for command history support (Unix/macOS)
# On Windows, this requires 'pyreadline3' or standard input fallbacks
try:
    import readline
except ImportError:
    # Readline is optional; if unavailable we simply continue without history support.
    pass

class ScientificCalculator:
    def __init__(self):
        # 1. Initialize the math environment
        self.env = self._build_env()
        # 2. Storage for user-defined variables
        self.variables = {}
        # 3. Store last result
        self.last_result = 0

    def _build_env(self):
        """Constructs the safe dictionary of math functions."""
        
        # Helper wrappers for degree conversion
        def _asin_deg(x): return math.degrees(math.asin(x))
        def _acos_deg(x): return math.degrees(math.acos(x))
        def _atan_deg(x): return math.degrees(math.atan(x))

        return {
            # Constants
            "pi": math.pi,
            "tau": math.tau,
            "e": math.e,
            "inf": math.inf,
            "nan": math.nan,

            # Basic
            "abs": abs,
            "round": round,
            "pow": pow,
            "sqrt": math.sqrt,
            "cbrt": math.cbrt,  # Cube root (Python 3.11+)

            # Logarithms
            "log": math.log10,   # Standard log base 10
            "ln": math.log,      # Natural log
            "log2": math.log2,
            "exp": math.exp,

            # Trig (Inputs in Degrees)
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),

            # Inverse Trig (Outputs in Degrees)
            "asin": _asin_deg,
            "acos": _acos_deg,
            "atan": _atan_deg,

            # Hyperbolic (Standard Radians)
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,

            # Combinatorics & Number Theory
            "fact": math.factorial,
            "comb": math.comb,   # nCr
            "perm": math.perm,   # nPr
            "gcd": math.gcd,
            "lcm": math.lcm,

            # Misc
            "ceil": math.ceil,
            "floor": math.floor,
            "hypot": math.hypot, # Euclidean norm
            "rad": math.radians, # Convert deg -> rad
            "deg": math.degrees, # Convert rad -> deg
        }

    def help_menu(self):
        """Returns a list of available functions."""
        funcs = sorted([k for k, v in self.env.items() if callable(v)])
        consts = sorted([k for k, v in self.env.items() if not callable(v)])
        return (
            f"\n--- Available Constants ---\n{', '.join(consts)}\n\n"
            f"--- Available Functions ---\n{', '.join(funcs)}\n"
        )

    def evaluate(self, expression: str):
        """Evaluates expression, handling assignments and variable lookups."""
        expression = expression.strip()

        # Handle 'help' command
        if expression.lower() == 'help':
            return self.help_menu()

        # Check for assignment: e.g., "x = sin(90) * 5"
        var_name = None
        if "=" in expression:
            parts = expression.split("=", 1)
            var_name = parts[0].strip()
            expression = parts[1].strip()

            # Safety check: Don't allow overwriting core functions (e.g. 'sin = 5')
            if var_name in self.env:
                return f"Error: Cannot overwrite built-in '{var_name}'"
            if not var_name.isidentifier():
                return f"Error: '{var_name}' is not a valid variable name"

        try:
            # Merge safe env + user variables + last result ('ans')
            calc_context = self.env.copy()
            calc_context.update(self.variables)
            calc_context['ans'] = self.last_result

            # EVALUATE
            # Note: We restrict __builtins__ to None for basic safety against imports
            result = eval(expression, {"__builtins__": None}, calc_context)

            # Store result logic
            self.last_result = result
            if var_name:
                self.variables[var_name] = result
                return f"{var_name} = {result}"
            
            return result

        except SyntaxError:
            return "Error: Invalid Syntax"
        except ZeroDivisionError:
            return "Error: Division by Zero"
        except NameError as e:
            return f"Error: Unknown variable or function ({e})"
        except Exception as e:
            return f"Error: {e}"

    def run_interactive(self):
        print("Scientific Calculator (CLI)")
        print("Type 'help' for functions, 'exit' to quit.")
        print("Features: History (↑, if available), Variables (x=5), Previous Ans (ans)\n")

        while True:
            try:
                expr = input("math> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye 👋")
                break

            if expr.lower() in {"exit", "quit"}:
                print("Goodbye 👋")
                break
            
            if not expr:
                continue

            output = self.evaluate(expr)
            
            # Formatting output (if float, make it pretty)
            if isinstance(output, float):
                print(f"= {output:g}") # :g removes trailing zeros
            else:
                print(f"= {output}")

def main():
    parser = argparse.ArgumentParser(description="Python Scientific Calculator")
    parser.add_argument("expression", nargs="?", help="Math expression to evaluate")
    args = parser.parse_args()

    calc = ScientificCalculator()

    if args.expression:
        print(calc.evaluate(args.expression))
    else:
        calc.run_interactive()

if __name__ == "__main__":
    main()