import click
import requests
import json

API_URL = "http://localhost:8000"  # Change this if your API runs on a different host/port

@click.group()
def cli():
    """Command Line Interface for interacting with the battery gauge API."""
    pass

@cli.command()
@click.argument('data')
def create_token(data):
    """Create a JWT token with the provided DATA."""
    response = requests.post(f"{API_URL}/token", json=json.loads(data))
    if response.status_code == 200:
        click.echo(f"Token: {response.json()['token']}")
    else:
        try:
            error_message = response.json().get("detail", "An error occurred")
        except ValueError:
            error_message = response.content.decode('utf-8')  # Fallback to raw content if not JSON
        click.echo(f"Error: {error_message}")
        exit(1)

@cli.command()
@click.argument('token')
def verify_token(token):
    """Verify the provided JWT TOKEN."""
    response = requests.post(f"{API_URL}/verify", json={"token": token})
    if response.status_code == 200:
        click.echo(f"Payload: {response.json()}")
    else:
        try:
            error_message = response.json().get("detail", "An error occurred")
        except ValueError:
            error_message = response.content.decode('utf-8')  # Fallback to raw content if not JSON
        click.echo(f"Error: {error_message}")
        exit(1)

if __name__ == "__main__":
    cli()
