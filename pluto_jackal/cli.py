import click
import os


@click.group()
def cli():
    """Pluto-Jackal: AI Runtime CLI"""
    pass


@cli.command()
@click.option(
    "--agents", default="founding", help="Initialize agents: founding/core/custom"
)
def init(agents):
    """Initialize Pluto-Jackal agents."""
    click.echo(f"🚀 Initializing Pluto-Jackal agents: {agents}")
    os.makedirs("runtime/agents", exist_ok=True)
    click.echo("✅ Agents initialized and ready.")


@cli.command()
def run():
    """Run Pluto-Jackal runtime."""
    click.echo("🤖 Starting Pluto-Jackal runtime...")
    click.echo("✅ Pluto-Jackal is now running.")


if __name__ == "__main__":
    cli()
