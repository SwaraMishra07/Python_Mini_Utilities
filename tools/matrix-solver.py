import numpy as np
import os
import sys
import time

# --- Configuration ---
PRECISION_DISPLAY = 4 
ZERO_THRESHOLD = 1e-10

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'

class MatrixSolver:
    def __init__(self):
        self.matrix = None
        self.rows = 0
        self.cols = 0

    def clean_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clean_number(self, n):
        """Standardizes floating point noise to cleaner numbers."""
        if abs(n) < ZERO_THRESHOLD: return 0.0
        if abs(n - round(n)) < ZERO_THRESHOLD: return float(round(n))
        return n

    def format_number(self, n):
        n = self.clean_number(n)
        if isinstance(n, complex):
            return f"{n.real:.2f}+{n.imag:.2f}j"
        if n.is_integer(): return f"{int(n)}"
        return f"{n:.{PRECISION_DISPLAY}f}"

    def render_matrix(self, matrix_data, title="MATRIX"):
        """Renders High-Fidelity Mathematical Matrix with Unicode."""
        if matrix_data is None: return
        
        # Handle 1D arrays (vectors) by converting to 2D
        if len(matrix_data.shape) == 1:
            matrix_data = matrix_data.reshape(-1, 1)

        clean_mat = np.vectorize(self.clean_number)(matrix_data)
        rows, cols = clean_mat.shape
        str_grid = []
        col_widths = [0] * cols

        for r in range(rows):
            row_strs = []
            for c in range(cols):
                s = self.format_number(clean_mat[r, c])
                row_strs.append(s)
                if len(s) > col_widths[c]: col_widths[c] = len(s)
            str_grid.append(row_strs)

        total_width = sum(col_widths) + (cols - 1) * 2
        print(f"\n{Colors.CYAN}--- {title} ---{Colors.ENDC}")
        print(f"{Colors.BOLD}⎡{Colors.ENDC} " + " " * total_width + f" {Colors.BOLD}⎤{Colors.ENDC}")
        for r in range(rows):
            line = "  ".join(str_grid[r][c].rjust(col_widths[c]) for c in range(cols))
            print(f"{Colors.BOLD}⎢{Colors.ENDC} {line} {Colors.BOLD}⎥{Colors.ENDC}")
        print(f"{Colors.BOLD}⎣{Colors.ENDC} " + " " * total_width + f" {Colors.BOLD}⎦{Colors.ENDC}\n")

    def get_input(self):
        self.clean_screen()
        print(f"{Colors.HEADER}MATRIX SOLVER PRO - INPUT MODE{Colors.ENDC}")
        try:
            r = int(input(f"Enter Rows: "))
            c = int(input(f"Enter Cols: "))
            print(f"{Colors.BLUE}Enter numbers separated by space (e.g. '1 2 3'){Colors.ENDC}")
            data = []
            for i in range(r):
                while True:
                    try:
                        raw = input(f"Row {i+1}: ")
                        row_vals = [float(x) for x in raw.strip().split()]
                        if len(row_vals) != c: raise ValueError
                        data.append(row_vals)
                        break
                    except ValueError: print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
            self.matrix = np.array(data)
            self.rows, self.cols = r, c
            self.clean_screen()
            self.render_matrix(self.matrix, "USER MATRIX")
        except ValueError:
            self.get_input()

    # --- 🧮 STANDARD OPERATIONS ---
    
    def op_determinant(self):
        if self.rows != self.cols: return print(f"{Colors.FAIL}Square Matrix required.{Colors.ENDC}")
        print(f"\n|A| = {self.clean_number(np.linalg.det(self.matrix))}")

    def op_inverse(self):
        if self.rows != self.cols: return print(f"{Colors.FAIL}Square Matrix required.{Colors.ENDC}")
        try:
            self.render_matrix(np.linalg.inv(self.matrix), "INVERSE (A⁻¹)")
        except np.linalg.LinAlgError:
            print(f"{Colors.FAIL}Matrix is Singular (No Inverse).{Colors.ENDC}")

    def op_transpose(self):
        self.render_matrix(self.matrix.T, "TRANSPOSE (Aᵀ)")

    def op_rank(self):
        print(f"\nRank: {np.linalg.matrix_rank(self.matrix)}")

    def op_trace(self):
        if self.rows != self.cols: return print(f"{Colors.FAIL}Square Matrix required.{Colors.ENDC}")
        print(f"\nTrace (Sum of diagonal) = {self.clean_number(np.trace(self.matrix))}")

    def op_eigen(self):
        if self.rows != self.cols: return print(f"{Colors.FAIL}Square Matrix required.{Colors.ENDC}")
        vals, vecs = np.linalg.eig(self.matrix)
        print(f"\n{Colors.GREEN}Eigenvalues found:{Colors.ENDC}")
        for v in vals:
            print(f" λ = {self.format_number(v)}")
        self.render_matrix(vecs, "EIGENVECTORS (Columns)")

    def op_power(self):
        if self.rows != self.cols: return print(f"{Colors.FAIL}Square Matrix required.{Colors.ENDC}")
        try:
            p = int(input("Enter Integer Power (n): "))
            self.render_matrix(np.linalg.matrix_power(self.matrix, p), f"MATRIX POWER (A^{p})")
        except ValueError: print("Invalid integer.")

    def op_solve_linear(self):
        """Solves Ax = B"""
        if self.rows != self.cols: return print(f"{Colors.FAIL}Coefficient matrix A must be square.{Colors.ENDC}")
        print(f"\n{Colors.BLUE}Enter Vector B (Size {self.rows}){Colors.ENDC}")
        try:
            b_raw = input(f"Enter {self.rows} numbers separated by space: ")
            b = [float(x) for x in b_raw.split()]
            if len(b) != self.rows: 
                print(f"{Colors.FAIL}Vector size mismatch.{Colors.ENDC}")
                return
            
            x = np.linalg.solve(self.matrix, b)
            self.render_matrix(np.array(b), "VECTOR B")
            self.render_matrix(x, "SOLUTION VECTOR X")
        except np.linalg.LinAlgError:
            print(f"{Colors.FAIL}Matrix is Singular. No unique solution.{Colors.ENDC}")
        except ValueError:
            print("Invalid input.")

    # --- 🎓 TUTORIAL MODE ---
    
    def print_step(self, text):
        print(f"{Colors.YELLOW}► {text}{Colors.ENDC}")
        time.sleep(0.5)

    def wait_user(self):
        input(f"\n{Colors.ITALIC}[Press Enter for next step...]{Colors.ENDC}")
        print("-" * 40)

    def tutorial_det_2x2(self):
        self.clean_screen()
        print(f"{Colors.HEADER}🎓 TUTORIAL: Determinant (2x2){Colors.ENDC}")
        example = np.array([[4, 2], [1, 5]])
        self.render_matrix(example, "EXAMPLE MATRIX A")
        a, b, c, d = example[0,0], example[0,1], example[1,0], example[1,1]

        self.print_step("Formula: (a × d) - (b × c)")
        print(f"   a={a}, b={b}, c={c}, d={d}")
        self.wait_user()

        self.print_step("Substitute & Solve:")
        print(f"   = ({int(a)} × {int(d)}) - ({int(b)} × {int(c)})")
        print(f"   = {int(a*d)} - {int(b*c)}")
        print(f"   = {int(a*d - b*c)}")
        input(f"\n{Colors.BLUE}[Tutorial Complete]{Colors.ENDC}")

    def tutorial_inverse_2x2(self):
        self.clean_screen()
        print(f"{Colors.HEADER}🎓 TUTORIAL: Inverse (2x2){Colors.ENDC}")
        example = np.array([[4, 7], [2, 6]])
        self.render_matrix(example, "MATRIX A")
        
        self.print_step("Step 1: Calculate Determinant (ad - bc)")
        det = (4*6) - (7*2)
        print(f"   Det = (4)(6) - (7)(2) = 24 - 14 = {det}")
        self.wait_user()

        self.print_step("Step 2: Swap 'a' and 'd', negate 'b' and 'c'")
        print("   Original: [a  b] -> [ 4  7]")
        print("             [c  d]    [ 2  6]")
        print("\n   Adjugate: [d -b] -> [ 6 -7]")
        print("             [-c a]    [-2  4]")
        adj = np.array([[6, -7], [-2, 4]])
        self.render_matrix(adj, "ADJUGATE MATRIX")
        self.wait_user()

        self.print_step("Step 3: Divide by Determinant")
        print(f"   Multiply Adjugate by 1/{det}")
        inv = adj / det
        self.render_matrix(inv, "INVERSE MATRIX")
        input(f"\n{Colors.BLUE}[Tutorial Complete]{Colors.ENDC}")

    def tutorial_transpose(self):
        self.clean_screen()
        print(f"{Colors.HEADER}🎓 TUTORIAL: Transpose{Colors.ENDC}")
        example = np.array([[1, 2, 3], [4, 5, 6]])
        self.render_matrix(example, "ORIGINAL (2x3)")
        
        self.print_step("Concept: Rows become Columns")
        print("   Row 1 [1, 2, 3] becomes -> Column 1")
        print("   Row 2 [4, 5, 6] becomes -> Column 2")
        self.wait_user()
        
        self.render_matrix(example.T, "TRANSPOSED (3x2)")
        input(f"\n{Colors.BLUE}[Tutorial Complete]{Colors.ENDC}")

    def tutorial_mult_2x2(self):
        self.clean_screen()
        print(f"{Colors.HEADER}🎓 TUTORIAL: Multiplication (Dot Product){Colors.ENDC}")
        mat_a = np.array([[1, 2], [3, 4]])
        mat_b = np.array([[5, 6], [7, 8]])
        self.render_matrix(mat_a, "A")
        self.render_matrix(mat_b, "B")
        
        self.print_step("Rule: Row of A • Column of B")
        self.wait_user()
        
        print("1. Top-Left:  (1×5) + (2×7) = 5 + 14 = 19")
        print("2. Top-Right: (1×6) + (2×8) = 6 + 16 = 22")
        self.wait_user()
        print("3. Bot-Left:  (3×5) + (4×7) = 15 + 28 = 43")
        print("4. Bot-Right: (3×6) + (4×8) = 18 + 32 = 50")
        
        self.render_matrix(np.dot(mat_a, mat_b), "RESULT")
        input(f"\n{Colors.BLUE}[Tutorial Complete]{Colors.ENDC}")

    def run_tutorial_menu(self):
        while True:
            self.clean_screen()
            print(f"{Colors.HEADER}🎓 STEP-BY-STEP LEARNING CENTER{Colors.ENDC}")
            print("1. Determinant (2x2)")
            print("2. Inverse (2x2 Adjoint Method)")
            print("3. Matrix Multiplication")
            print("4. Transpose Visualization")
            print("5. Return to Main Menu")
            
            c = input(f"\n{Colors.BOLD}Select Tutorial >> {Colors.ENDC}")
            if c == '1': self.tutorial_det_2x2()
            elif c == '2': self.tutorial_inverse_2x2()
            elif c == '3': self.tutorial_mult_2x2()
            elif c == '4': self.tutorial_transpose()
            elif c == '5': break

    # --- MAIN LOOP ---
    def run(self):
        self.get_input()
        while True:
            print("\n" + "═"*50)
            self.render_matrix(self.matrix, "CURRENT MATRIX")
            print(f"{Colors.HEADER}OPERATIONS:{Colors.ENDC}")
            print("1. Determinant (|A|)")
            print("2. Inverse (A⁻¹)")
            print("3. Transpose (Aᵀ)")
            print("4. Rank")
            print("5. Trace")
            print("6. Eigenvalues/Vectors")
            print("7. Matrix Power (A^n)")
            print("8. Solve System (Ax = B)")
            print("-" * 20)
            print(f"{Colors.YELLOW}9. 🎓 Step-by-Step Tutorials{Colors.ENDC}")
            print(f"R. Input New Matrix")
            print(f"0. Exit")
            
            choice = input(f"\n{Colors.BOLD}Select >> {Colors.ENDC}").upper()
            
            if choice == '1': self.op_determinant()
            elif choice == '2': self.op_inverse()
            elif choice == '3': self.op_transpose()
            elif choice == '4': self.op_rank()
            elif choice == '5': self.op_trace()
            elif choice == '6': self.op_eigen()
            elif choice == '7': self.op_power()
            elif choice == '8': self.op_solve_linear()
            elif choice == '9': self.run_tutorial_menu()
            elif choice == 'R': self.get_input()
            elif choice == '0': sys.exit()
            else: print("Invalid Option")
            
            if choice != '9':
                input(f"\n{Colors.BLUE}[Press Enter to Continue]{Colors.ENDC}")
                self.clean_screen()

if __name__ == "__main__":
    try:
        import numpy
        app = MatrixSolver()
        app.run()
    except ImportError:
        print("Please install numpy: pip install numpy")