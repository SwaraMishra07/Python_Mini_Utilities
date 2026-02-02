import typer
import pandas as pd
import plotext as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
import os
import sys
import math
import shutil
from typing import Optional

# Initialize Typer and Console
app = typer.Typer(help="The Data Painter: Advanced CLI Data Visualization Tool", add_completion=False)
console = Console()

def get_valid_file(file_path: Optional[str]) -> str:
    """Interactively prompts for a file if none is provided."""
    while not file_path or not os.path.exists(file_path):
        if file_path:
            rprint(f"[bold red]Error:[/bold red] File '{file_path}' not found.")
        file_path = Prompt.ask("[bold cyan]Enter path to CSV file[/bold cyan]")
    return file_path

def load_data(file: str, x_col: str, y_col: str, limit: int = None, sort_mode: str = None):
    """Loads, validates, sorts, and limits the dataframe."""
    try:
        df = pd.read_csv(file)
    except Exception as e:
        rprint(f"[bold red]Failed to read CSV:[/bold red] {e}")
        sys.exit(1)

    if x_col not in df.columns or y_col not in df.columns:
        rprint(f"[bold red]Error:[/bold red] Columns not found.")
        rprint(f"Available columns: [yellow]{', '.join(df.columns)}[/yellow]")
        sys.exit(1)

    try:
        df[y_col] = pd.to_numeric(df[y_col])
    except ValueError:
        rprint(f"[bold red]Error:[/bold red] Column '{y_col}' contains non-numeric data.")
        sys.exit(1)

    if sort_mode == "asc":
        df = df.sort_values(by=y_col, ascending=True)
    elif sort_mode == "desc":
        df = df.sort_values(by=y_col, ascending=False)
    elif sort_mode == "x":
        df = df.sort_values(by=x_col, ascending=True)

    if limit and limit > 0:
        df = df.head(limit)

    return df

def draw_custom_ascii_pie(labels, values, title):
    """Fallback Pie Chart Renderer."""
    rprint(f"\n[bold underline]{title}[/bold underline]\n")
    total = sum(values)
    radius = 10
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "white"]
    
    angles = []
    current_angle = 0
    for v in values:
        share = (v / total) * 360
        angles.append((current_angle, current_angle + share))
        current_angle += share

    for y in range(-radius, radius + 1):
        line = ""
        for x in range(-radius * 2, radius * 2 + 1):
            dist = math.sqrt((x/2)**2 + y**2)
            if dist <= radius:
                angle_deg = math.degrees(math.atan2(y, x/2))
                if angle_deg < 0: angle_deg += 360
                
                char_color = "white"
                for i, (start, end) in enumerate(angles):
                    if start <= angle_deg < end:
                        char_color = colors[i % len(colors)]
                        break
                line += f"[{char_color}]█[/{char_color}]"
            else:
                line += " "
        rprint(line)

    rprint("\n[bold]Legend:[/bold]")
    for i, label in enumerate(labels):
        color = colors[i % len(colors)]
        pct = (values[i] / total) * 100
        rprint(f"[{color}]█[/{color}] {label}: {values[i]:,.2f} ({pct:.1f}%)")
    print()

def render_stats(df: pd.DataFrame, y_col: str):
    """Renders a rich table of statistical insights."""
    stats_table = Table(title=f"📊 Analytics: {y_col}", expand=True, border_style="cyan")
    stats_table.add_column("Metric", justify="right", style="magenta")
    stats_table.add_column("Value", justify="left", style="green")
    
    stats_table.add_row("Count", str(len(df)))
    stats_table.add_row("Sum", f"{df[y_col].sum():,.2f}")
    stats_table.add_row("Average (Mean)", f"{df[y_col].mean():,.2f}")
    stats_table.add_row("Median", f"{df[y_col].median():,.2f}")
    stats_table.add_row("Std. Deviation", f"{df[y_col].std():,.2f}")
    stats_table.add_row("Max", f"{df[y_col].max():,.2f}")
    stats_table.add_row("Min", f"{df[y_col].min():,.2f}")

    console.print(Panel(stats_table, border_style="blue"))

@app.command()
def paint(
    file: Optional[str] = typer.Argument(None, help="Path to the CSV file"),
    x_col: str = typer.Option(None, "--x-axis", "-x", help="Column for X-axis (Labels)"),
    y_col: str = typer.Option(None, "--y-axis", "-y", help="Column for Y-axis (Values)"),
    chart_type: str = typer.Option("bar", "--type", help="Chart type: bar, barh, line, scatter, hist, pie"),
    title: str = typer.Option("Data Analysis", "--title", "-t", help="Title of the graph"),
    limit: int = typer.Option(0, "--limit", "-l", help="Limit number of rows (e.g. 20)"),
    sort: str = typer.Option(None, "--sort", help="Sort mode: 'asc', 'desc', or 'x'"),
    theme: str = typer.Option("dark", "--theme", help="Theme: dark, light, clear"),
):
    """
    🎨 Interactive CLI tool to visualize CSV data.
    """
    
    if hasattr(plt, "__file__") and "site-packages" not in plt.__file__:
            rprint(f"[bold red]WARNING: Local plotext file detected at {plt.__file__}. Delete it![/bold red]")

    # 1. Interactive Prompting
    if not file:
        rprint("[bold yellow]Welcome to Data Painter Interactive Mode![/bold yellow]")
        file = get_valid_file(file)
    
    temp_df = pd.read_csv(file, nrows=0) 
    headers = list(temp_df.columns)

    if not x_col:
        rprint(f"Columns: [dim]{', '.join(headers)}[/dim]")
        x_col = Prompt.ask("Choose [bold magenta]X-axis[/bold magenta] column", choices=headers)
    
    if not y_col:
        y_col = Prompt.ask("Choose [bold magenta]Y-axis[/bold magenta] column (Numeric)", choices=headers)

    # 2. Process Data
    with console.status("[bold green]Processing data...[/bold green]"):
        df = load_data(file, x_col, y_col, limit, sort)

    x_data = df[x_col].tolist()
    y_data = df[y_col].tolist()
    x_indices = list(range(len(x_data)))

    # 3. Plotting Logic
    plt.clear_figure()
    plt.theme(theme)
    plt.title(title)
    
    # Get Terminal Size for smart scaling
    term_w, term_h = shutil.get_terminal_size()
    should_use_plotext = True

    if chart_type == 'bar':
        plt.bar(x_data, y_data)
        plt.xlabel(x_col)
    
    elif chart_type == 'barh':
        # Smart sizing for horizontal bars
        smart_height = min(len(x_data) + 5, term_h - 5) 
        smart_width = int(term_w * 0.8) 
        
        plt.plot_size(smart_width, smart_height)
        plt.bar(x_data, y_data, orientation="horizontal")
        plt.xlabel(y_col) 
        plt.ylabel(x_col) 
        
    elif chart_type == 'pie':
        try:
            plt.pie(y_data, labels=x_data)
            plt.title(f"Distribution of {y_col} by {x_col}")
        except AttributeError:
            rprint("[dim]Switching to Custom ASCII Pie Engine...[/dim]")
            draw_custom_ascii_pie(x_data, y_data, f"Distribution of {y_col} by {x_col}")
            should_use_plotext = False

    elif chart_type == 'line':
        plt.plot(x_indices, y_data)
        plt.xticks(x_indices, x_data) 
        plt.xlabel(x_col) 

    elif chart_type == 'scatter':
        plt.scatter(x_indices, y_data)
        plt.xticks(x_indices, x_data)
        plt.xlabel(x_col)

    elif chart_type == 'hist':
        plt.hist(y_data, bins=20) 
        plt.xlabel(y_col)
        plt.title(f"Frequency Distribution of {y_col}")

    else:
        # Fallback Strategy: Warn user, show valid options, and default to Bar
        rprint(f"[bold yellow]⚠️  Warning:[/bold yellow] Unknown chart type '{chart_type}'.")
        rprint(f"Available options: [cyan]bar, barh, pie, line, scatter, hist[/cyan]")
        rprint("[dim]Defaulting to Bar Chart...[/dim]")
        
        plt.bar(x_data, y_data)
        plt.xlabel(x_col)

    # 4. Render Output
    if should_use_plotext:
        plt.show()

    render_stats(df, y_col)

if __name__ == "__main__":
    app()