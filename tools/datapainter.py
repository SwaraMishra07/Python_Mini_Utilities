import typer
import pandas as pd
import plotext as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
import os
import sys

# Initialize Typer app and Rich Console
app = typer.Typer(help="The Data Painter: CLI Data Visualization Tool")
console = Console()

def validate_file(file_path: str):
    if not os.path.exists(file_path):
        rprint(f"[bold red]Error:[/bold red] File '{file_path}' not found.")
        sys.exit(1)
    return file_path

@app.command()
def paint(
    file: str = typer.Argument(..., help="Path to the CSV file"),
    x_col: str = typer.Option(..., "--x-axis", "-x", help="Column name for X-axis (Labels)"),
    y_col: str = typer.Option(..., "--y-axis", "-y", help="Column name for Y-axis (Values)"),
    title: str = typer.Option("Data Analysis", "--title", "-t", help="Title of the graph"),
    type: str = typer.Option("bar", "--type", help="Type of chart: 'bar', 'scatter', or 'line'"),
    dark: bool = typer.Option(True, "--dark/--light", help="Use dark mode theme"),
):
    """
    Reads a CSV and paints a graph in your terminal.
    """
    validate_file(file)

    # 1. Loading Data
    with console.status("[bold green]Reading CSV and crunching numbers...[/bold green]"):
        try:
            df = pd.read_csv(file)
        except Exception as e:
            rprint(f"[bold red]Failed to read CSV:[/bold red] {e}")
            sys.exit(1)

        # Validation: Check if columns exist
        if x_col not in df.columns or y_col not in df.columns:
            rprint(f"[bold red]Error:[/bold red] Columns not found.")
            rprint(f"Available columns: [cyan]{', '.join(df.columns)}[/cyan]")
            sys.exit(1)
        
        # Validation: Ensure Y is numeric
        try:
            df[y_col] = pd.to_numeric(df[y_col])
        except ValueError:
             rprint(f"[bold red]Error:[/bold red] Column '{y_col}' contains non-numeric data.")
             sys.exit(1)

    # 2. Prepare Data for Plotting
    x_data = df[x_col].tolist()
    y_data = df[y_col].tolist()
    
    # Create numeric indices (0, 1, 2...) for the X-axis
    # This acts as a safe fallback for Line/Scatter plots to prevent parsing errors
    x_indices = list(range(len(x_data)))

    # 3. Setup Plotext
    plt.clear_figure()
    plt.theme('dark' if dark else 'clear')
    plt.title(title)
    plt.ylabel(y_col)

    # 4. Logic to handle different chart types
    if type == 'bar':
        # Bar charts handle string labels naturally
        plt.bar(x_data, y_data)
        plt.xlabel(x_col)
    
    elif type == 'scatter':
        # Scatter needs numbers on X, so we use indices, then map labels back
        plt.scatter(x_indices, y_data, marker="dot")
        plt.xticks(x_indices, x_data)
        
    elif type == 'line':
        # Line needs numbers on X too
        plt.plot(x_indices, y_data)
        plt.xticks(x_indices, x_data)

    # 5. Render the Graph
    plt.show()

    # 6. Render Statistical Summary
    # We create a pretty table below the graph
    summary_table = Table(title=f"Statistics: {y_col}", expand=True, border_style="cyan")
    summary_table.add_column("Metric", justify="right", style="magenta")
    summary_table.add_column("Value", justify="left", style="green")

    summary_table.add_row("Total Rows", str(len(df)))
    summary_table.add_row("Sum", f"{df[y_col].sum():,.2f}")
    summary_table.add_row("Average", f"{df[y_col].mean():,.2f}")
    summary_table.add_row("Maximum", f"{df[y_col].max():,.2f}")
    summary_table.add_row("Minimum", f"{df[y_col].min():,.2f}")

    console.print(Panel(summary_table, title="Data Insight", border_style="blue"))

if __name__ == "__main__":
    app()