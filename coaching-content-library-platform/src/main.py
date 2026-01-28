"""CLI entry point using Typer."""
import json
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table

from .config import settings
from .models.content import ContentItem, ContentSource, ContentType
from .ingestors.youtube import YouTubeIngestor
from .ingestors.reddit import RedditIngestor
from .storage.sqlite import SQLiteRepository

app = typer.Typer(help="Goalie Drill Aggregator - Discover and save goalie training content")
console = Console()

# Global paths
DATA_DIR = Path("data")
LAST_SEARCH_FILE = DATA_DIR / "last_search.json"


def ensure_data_directory():
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_last_search(results: list[ContentItem]):
    """Save search results to last_search.json."""
    ensure_data_directory()
    # Convert ContentItem objects to dict for JSON serialization
    results_data = [item.model_dump(mode='json') for item in results]
    with open(LAST_SEARCH_FILE, 'w') as f:
        json.dump(results_data, f, indent=2, default=str)


def load_last_search() -> list[ContentItem]:
    """Load search results from last_search.json."""
    if not LAST_SEARCH_FILE.exists():
        console.print("[red]No previous search results found. Run a search first.[/red]")
        raise typer.Exit(1)

    with open(LAST_SEARCH_FILE, 'r') as f:
        results_data = json.load(f)

    # Convert dict back to ContentItem objects
    return [ContentItem(**item) for item in results_data]


@app.command()
def search(
    query: str,
    source: str = typer.Option("all", help="Source to search: youtube, reddit, or all"),
    max_results: int = typer.Option(10, help="Maximum number of results to return"),
    subreddits: Optional[str] = typer.Option(None, help="Comma-separated subreddit names (Reddit only)"),
):
    """
    Search for goalie drill content.

    Examples:
        python -m src.main search "butterfly drill" --source youtube --max-results 10
        python -m src.main search "goalie tips" --source reddit --subreddits hockeygoalies,hockeyplayers
    """
    ensure_data_directory()

    all_results = []

    try:
        # Search YouTube
        if source in ["youtube", "all"]:
            console.print(f"[cyan]Searching YouTube for: {query}[/cyan]")
            youtube = YouTubeIngestor(settings.youtube_api_key)
            youtube_results = youtube.search(query, max_results=max_results)
            all_results.extend(youtube_results)
            console.print(f"[green]Found {len(youtube_results)} YouTube videos[/green]")

        # Search Reddit
        if source in ["reddit", "all"]:
            console.print(f"[cyan]Searching Reddit for: {query}[/cyan]")
            reddit = RedditIngestor(
                settings.reddit_client_id,
                settings.reddit_client_secret,
                settings.reddit_user_agent
            )

            # Parse subreddits if provided
            subreddit_list = None
            if subreddits:
                subreddit_list = [s.strip() for s in subreddits.split(',')]

            reddit_results = reddit.search(
                query,
                max_results=max_results,
                subreddits=subreddit_list
            )
            all_results.extend(reddit_results)
            console.print(f"[green]Found {len(reddit_results)} Reddit posts[/green]")

        if not all_results:
            console.print("[yellow]No results found.[/yellow]")
            return

        # Save results
        save_last_search(all_results)

        # Display results in a table
        table = Table(title=f"Search Results: {query}")
        table.add_column("Index", justify="right", style="cyan")
        table.add_column("Source", style="magenta")
        table.add_column("Title", style="white", max_width=50)
        table.add_column("Author", style="blue")
        table.add_column("Views/Score", justify="right", style="green")

        for idx, item in enumerate(all_results):
            # Truncate title if too long
            title = item.title
            if len(title) > 47:
                title = title[:47] + "..."

            # Get engagement metric (views for YouTube, score for Reddit)
            engagement = ""
            if item.view_count is not None:
                engagement = f"{item.view_count:,}"
            elif item.like_count is not None:
                engagement = f"{item.like_count:,}"

            table.add_row(
                str(idx),
                item.source.value,
                title,
                item.author or "N/A",
                engagement
            )

        console.print(table)
        console.print(f"\n[dim]Results saved. Use 'save <index>' to save items to your collection.[/dim]")

    except Exception as e:
        console.print(f"[red]Error during search: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def save(
    index: int,
    tags: Optional[str] = typer.Option(None, help="Comma-separated tags"),
    collection: Optional[str] = typer.Option(None, help="Collection name"),
    notes: Optional[str] = typer.Option(None, help="Notes about this content"),
):
    """
    Save a content item from the last search results.

    Examples:
        python -m src.main save 1 --tags goalie,butterfly --collection warmups
        python -m src.main save 0 --notes "Great drill for lateral movement"
    """
    try:
        # Load last search results
        results = load_last_search()

        # Validate index
        if index < 0 or index >= len(results):
            console.print(f"[red]Invalid index. Must be between 0 and {len(results) - 1}[/red]")
            raise typer.Exit(1)

        # Get the item
        item = results[index]

        # Parse tags if provided
        if tags:
            item.tags = [t.strip() for t in tags.split(',')]

        # Set collection if provided
        if collection:
            item.collection_id = collection

        # Set notes if provided
        if notes:
            item.notes = notes

        # Save to repository
        repo = SQLiteRepository(settings.database_path)
        repo.save(item)

        console.print(f"[green]✓ Saved: {item.title}[/green]")
        console.print(f"  Source: {item.source.value}")
        console.print(f"  URL: {item.url}")
        if item.tags:
            console.print(f"  Tags: {', '.join(item.tags)}")
        if item.collection_id:
            console.print(f"  Collection: {item.collection_id}")

    except Exception as e:
        console.print(f"[red]Error saving item: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def list(
    source: Optional[str] = typer.Option(None, help="Filter by source: youtube, reddit"),
    tags: Optional[str] = typer.Option(None, help="Filter by tags (comma-separated, matches ANY)"),
    collection: Optional[str] = typer.Option(None, help="Filter by collection name"),
    query: Optional[str] = typer.Option(None, help="Search in title and description"),
):
    """
    List saved content items.

    Examples:
        python -m src.main list
        python -m src.main list --source youtube --tags goalie
        python -m src.main list --collection warmups
    """
    try:
        repo = SQLiteRepository(settings.database_path)

        # Convert source string to enum if provided
        source_enum = None
        if source:
            try:
                source_enum = ContentSource(source.capitalize())
            except ValueError:
                console.print(f"[red]Invalid source: {source}. Must be youtube or reddit[/red]")
                raise typer.Exit(1)

        # Parse tags if provided
        tags_list = None
        if tags:
            tags_list = [t.strip() for t in tags.split(',')]

        # Search saved items
        items = repo.search_saved(
            query=query,
            source=source_enum,
            tags=tags_list,
            collection_id=collection
        )

        if not items:
            console.print("[yellow]No saved items found matching your filters.[/yellow]")
            return

        # Display results in a table
        table = Table(title=f"Saved Content ({len(items)} items)")
        table.add_column("Source", style="magenta")
        table.add_column("Title", style="white", max_width=40)
        table.add_column("Author", style="blue")
        table.add_column("Tags", style="cyan")
        table.add_column("Saved At", style="green")

        for item in items:
            # Truncate title if too long
            title = item.title
            if len(title) > 37:
                title = title[:37] + "..."

            # Format tags
            tags_str = ", ".join(item.tags) if item.tags else "-"
            if len(tags_str) > 20:
                tags_str = tags_str[:20] + "..."

            # Format saved_at
            saved_at_str = "-"
            if item.saved_at:
                saved_at_str = item.saved_at.strftime("%Y-%m-%d")

            table.add_row(
                item.source.value,
                title,
                item.author or "N/A",
                tags_str,
                saved_at_str
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing items: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def delete(
    source: str,
    content_id: str,
):
    """
    Delete a saved content item.

    Examples:
        python -m src.main delete youtube dQw4w9WgXcQ
        python -m src.main delete reddit abc123
    """
    try:
        # Convert source string to enum
        try:
            source_enum = ContentSource(source.capitalize())
        except ValueError:
            console.print(f"[red]Invalid source: {source}. Must be youtube or reddit[/red]")
            raise typer.Exit(1)

        # Get the item first to show what will be deleted
        repo = SQLiteRepository(settings.database_path)
        item = repo.get_by_id(source_enum, content_id)

        if not item:
            console.print(f"[red]No saved item found with source={source} and id={content_id}[/red]")
            raise typer.Exit(1)

        # Show what will be deleted
        console.print(f"\n[yellow]About to delete:[/yellow]")
        console.print(f"  Title: {item.title}")
        console.print(f"  Source: {item.source.value}")
        console.print(f"  URL: {item.url}")

        # Confirm deletion
        if not typer.confirm("\nAre you sure you want to delete this item?"):
            console.print("[dim]Deletion cancelled.[/dim]")
            return

        # Delete the item
        success = repo.delete(source_enum, content_id)

        if success:
            console.print("[green]✓ Item deleted successfully[/green]")
        else:
            console.print("[red]Failed to delete item[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error deleting item: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
