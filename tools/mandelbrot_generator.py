import os
import sys
import time

# Try to import dependencies; handle missing ones gracefully
try:
    import numpy as np
except ImportError:
    print("Error: This tool requires 'numpy'. Please run: pip install numpy")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.align import Align
    from rich.prompt import FloatPrompt, IntPrompt, Confirm
    from rich.layout import Layout
    from rich.live import Live
except ImportError:
    print("Error: This tool requires 'rich'. Please run: pip install rich")
    sys.exit(1)

# Initialize Rich Console
console = Console()

class MandelbrotGenerator:
    def __init__(self):
        # Viewport settings (Standard Mandelbrot view)
        self.center_r = -0.75  # Real axis (x)
        self.center_i = 0.0    # Imaginary axis (y)
        self.zoom = 1.0
        
        # Resolution settings
        self.width = 80
        self.height = 40
        self.max_iter = 100
        
        # Terminal character aspect ratio correction (Characters are usually taller than wide)
        # 2.0 is a good approximation for most monospaced fonts
        self.aspect_ratio = 2.0 
        
        # ASCII Gradient: Dark -> Light (Dense -> Sparse)
        # Using a density string to represent iteration count
        self.chars = " .:-=+*#%@"

    def calculate_set(self):
        """
        Vectorized calculation of the Mandelbrot set using NumPy.
        Returns a 2D array of iteration counts.
        """
        # Calculate mathematical bounds based on zoom and center
        # The base view is roughly (-2.5 to 1.0) on Real axis
        r_radius = 1.5 / self.zoom
        i_radius = (1.5 / self.aspect_ratio) * (self.height / self.width) * 2.5 / self.zoom

        # Generate coordinate grids
        r_vals = np.linspace(self.center_r - r_radius, self.center_r + r_radius, self.width)
        i_vals = np.linspace(self.center_i - i_radius, self.center_i + i_radius, self.height)
        
        # C is the complex grid (c = r + i*j)
        # Broadcasting creates a 2D grid
        C = r_vals[np.newaxis, :] + i_vals[:, np.newaxis] * 1j

        # Z is the moving point, initialized to 0
        Z = np.zeros_like(C)
        
        # Array to store iteration counts (default to max_iter)
        escape_time = np.full(C.shape, self.max_iter, dtype=int)
        
        # Mask to track points that haven't escaped yet
        mask = np.full(C.shape, True, dtype=bool)

        for i in range(self.max_iter):
            # Only compute for points that are still within bounds
            # Z[mask] selects only the active pixels, optimizing speed significantly
            Z[mask] = Z[mask] * Z[mask] + C[mask]
            
            # Check for escape: |Z| > 2 (or |Z|^2 > 4 for efficiency)
            escaped_now = (Z.real**2 + Z.imag**2) > 4.0
            
            # Update escape time for points that just escaped
            newly_escaped = escaped_now & mask 
            escape_time[newly_escaped] = i
            
            # Remove escaped points from calculation
            mask[escaped_now] = False
            
            # Early exit if everything has escaped
            if not np.any(mask):
                break
                
        return escape_time

    def render_frame(self):
        """Generates the ASCII art string from the calculation data."""
        data = self.calculate_set()
        lines = []

        for row in data:
            line_chars = []
            for iterations in row:
                if iterations == self.max_iter:
                    # Point is inside the set (stable)
                    line_chars.append(" ") 
                else:
                    # Point is outside; color based on escape velocity
                    char_idx = iterations % len(self.chars)
                    line_chars.append(self.chars[char_idx])
            lines.append("".join(line_chars))
        
        return "\n".join(lines)

    def interactive_loop(self):
        """Runs the main application loop."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Render the fractal
            art = self.render_frame()
            
            # UI Construction
            title = f"[bold cyan]Mandelbrot Explorer[/] | Zoom: {self.zoom:.2e}x | Center: {self.center_r:.5f}{self.center_i:+.5f}i"
            panel = Panel(Align.center(f"[blue]{art}[/]"), title=title, border_style="green")
            console.print(panel)
            
            # Menu
            console.print("[bold]Options:[/]")
            console.print("1. [green]Zoom In[/]  2. [green]Zoom Out[/]  3. [green]Move[/]  4. [green]Resolution[/]  5. [green]Reset[/]  0. [red]Exit[/]")
            
            choice = IntPrompt.ask("Select", default=1)

            if choice == 1:
                factor = FloatPrompt.ask("Zoom Factor", default=2.0)
                self.zoom *= factor
            elif choice == 2:
                factor = FloatPrompt.ask("Zoom Factor", default=2.0)
                self.zoom /= factor
            elif choice == 3:
                console.print("[dim]Tip: Standard Mandelbrot is centered at -0.75 + 0.0i[/]")
                self.center_r = FloatPrompt.ask("Real (X) Center", default=self.center_r)
                self.center_i = FloatPrompt.ask("Imaginary (Y) Center", default=self.center_i)
            elif choice == 4:
                self.width = IntPrompt.ask("Width", default=self.width)
                self.height = IntPrompt.ask("Height", default=self.height)
                self.max_iter = IntPrompt.ask("Max Iterations (Detail)", default=self.max_iter)
            elif choice == 5:
                self.center_r = -0.75
                self.center_i = 0.0
                self.zoom = 1.0
            elif choice == 0:
                console.print("Goodbye!")
                break
            else:
                console.print("[red]Invalid choice[/]")
                time.sleep(1)

def main():
    app = MandelbrotGenerator()
    # Check for direct args or run interactive
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python mandelbrot_generator.py")
        print("Runs an interactive terminal-based Mandelbrot set explorer.")
        return

    app.interactive_loop()

if __name__ == "__main__":
    main()