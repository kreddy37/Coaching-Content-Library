"""Discord bot for saving content to the library."""
import re
import logging
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
import httpx

from ..config import settings
from ..models.content import ContentSource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL patterns for different platforms
URL_PATTERNS = {
    ContentSource.YOUTUBE: [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+',
    ],
    ContentSource.REDDIT: [
        r'(?:https?://)?(?:www\.)?reddit\.com/r/[\w]+/comments/[\w]+',
    ],
    ContentSource.INSTAGRAM: [
        r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel)/[\w-]+',
    ],
    ContentSource.TIKTOK: [
        r'(?:https?://)?(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
        r'(?:https?://)?vm\.tiktok\.com/[\w]+',
    ],
}


class ContentBot(commands.Bot):
    """Discord bot for content library management."""

    def __init__(self):
        """Initialize the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True

        super().__init__(command_prefix="!", intents=intents)

        self.api_base_url = settings.api_base_url

    async def setup_hook(self):
        """Setup hook called before bot connects to Discord."""
        # Sync commands with Discord
        await self.tree.sync()
        logger.info("Commands synced")

    async def on_ready(self):
        """Event handler for when bot is ready."""
        logger.info(f"Bot logged in as {self.user}")
        logger.info(f"Connected to {len(self.guilds)} guilds")

    async def on_message(self, message: discord.Message):
        """Event handler for messages.

        Detects URLs and offers to save them to the library.
        """
        # Ignore bot messages
        if message.author.bot:
            return

        # Check for URLs in message
        url, source = self.detect_url(message.content)
        if url and source:
            await self.handle_url_detected(message, url, source)

        # Process commands
        await self.process_commands(message)

    def detect_url(self, content: str) -> tuple[Optional[str], Optional[ContentSource]]:
        """Detect and extract URL from message content.

        Args:
            content: Message content

        Returns:
            Tuple of (URL, ContentSource) if found, (None, None) otherwise
        """
        for source, patterns in URL_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.group(0), source

        return None, None

    async def handle_url_detected(
        self,
        message: discord.Message,
        url: str,
        source: ContentSource
    ):
        """Handle detected URL by offering to save it.

        Args:
            message: Discord message containing URL
            url: Detected URL
            source: Content source platform
        """
        # Create embed
        embed = discord.Embed(
            title="Content URL Detected",
            description=f"Found a {source.value} link!",
            color=discord.Color.blue()
        )
        embed.add_field(name="URL", value=url, inline=False)
        embed.add_field(
            name="Action",
            value="Would you like to save this to your library?",
            inline=False
        )

        # Create view with save button
        view = SaveContentView(self, url, source, message.author.id)

        await message.reply(embed=embed, view=view)


class SaveContentView(discord.ui.View):
    """View with save button for detected URLs."""

    def __init__(
        self,
        bot: ContentBot,
        url: str,
        source: ContentSource,
        user_id: int
    ):
        """Initialize the view.

        Args:
            bot: Bot instance
            url: Content URL
            source: Content source
            user_id: ID of user who posted the URL
        """
        super().__init__(timeout=None)  # No timeout - persistent view
        self.bot = bot
        self.url = url
        self.source = source
        self.user_id = user_id

    @discord.ui.button(
        label="Save to Library",
        style=discord.ButtonStyle.primary,
        custom_id="save_content_button"
    )
    async def save_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        """Handle save button click."""
        # Verify it's the same user
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "Only the user who posted this link can save it.",
                ephemeral=True
            )
            return

        # Open metadata modal - pass message and view for cleanup after save
        modal = MetadataModal(self.bot, self.url, self.source, interaction.message, self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(
        label="Ignore",
        style=discord.ButtonStyle.secondary,
        custom_id="ignore_content_button"
    )
    async def ignore_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        """Handle ignore button click."""
        # Verify it's the same user
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "Only the user who posted this link can ignore it.",
                ephemeral=True
            )
            return

        await interaction.response.send_message("Okay, ignoring this link.", ephemeral=True)

        # Disable the buttons after ignoring
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        self.stop()


class MetadataModal(discord.ui.Modal, title="Add Drill Metadata"):
    """Modal for collecting drill metadata."""

    drill_tags = discord.ui.TextInput(
        label="Drill Tags (comma-separated)",
        placeholder="e.g., butterfly, lateral-movement, warmup",
        required=False,
        max_length=200
    )

    drill_description = discord.ui.TextInput(
        label="Drill Description",
        placeholder="Describe the drill and its purpose",
        required=False,
        style=discord.TextStyle.paragraph,
        max_length=1000
    )

    difficulty = discord.ui.TextInput(
        label="Difficulty Level",
        placeholder="beginner, intermediate, or advanced",
        required=False,
        max_length=50
    )

    equipment = discord.ui.TextInput(
        label="Required Equipment",
        placeholder="e.g., pucks, cones, net",
        required=False,
        max_length=200
    )

    age_group = discord.ui.TextInput(
        label="Age Group",
        placeholder="e.g., bantam, 12-14, peewee",
        required=False,
        max_length=50
    )

    def __init__(
        self,
        bot: ContentBot,
        url: str,
        source: ContentSource,
        message: discord.Message,
        view: SaveContentView
    ):
        """Initialize the modal.

        Args:
            bot: Bot instance
            url: Content URL
            source: Content source
            message: The message containing the save buttons
            view: The SaveContentView instance
        """
        super().__init__()
        self.bot = bot
        self.url = url
        self.source = source
        self.message = message
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        await interaction.response.defer(thinking=True)

        # Build request payload
        payload = {
            "url": self.url,
            "source": self.source.value
        }

        # Add metadata if provided
        if self.drill_tags.value:
            # Parse comma-separated tags into list
            tags = [tag.strip() for tag in self.drill_tags.value.split(',') if tag.strip()]
            payload["drill_tags"] = tags
        if self.drill_description.value:
            payload["drill_description"] = self.drill_description.value
        if self.difficulty.value:
            payload["difficulty"] = self.difficulty.value
        if self.equipment.value:
            payload["equipment"] = self.equipment.value
        if self.age_group.value:
            payload["age_group"] = self.age_group.value

        # Call API to save content
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.bot.api_base_url}/api/v1/content",
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                content_data = response.json()

            # Create success embed
            embed = discord.Embed(
                title="Content Saved",
                description=f"Successfully saved to your library!",
                color=discord.Color.green()
            )
            embed.add_field(name="Title", value=content_data.get("title", "N/A"), inline=False)
            embed.add_field(name="Source", value=content_data.get("source", "N/A"), inline=True)
            embed.add_field(name="Author", value=content_data.get("author", "N/A"), inline=True)

            if content_data.get("drill_tags"):
                tags_str = ", ".join(content_data["drill_tags"])
                embed.add_field(name="Tags", value=tags_str, inline=True)
            if content_data.get("difficulty"):
                embed.add_field(name="Difficulty", value=content_data["difficulty"], inline=True)

            await interaction.followup.send(embed=embed)

            # Disable buttons after successful save
            for item in self.view.children:
                item.disabled = True
            await self.message.edit(view=self.view)
            self.view.stop()

        except httpx.HTTPStatusError as e:
            error_msg = f"Failed to save content: {e.response.status_code}"
            try:
                error_detail = e.response.json().get("detail", "Unknown error")
                error_msg = f"{error_msg} - {error_detail}"
            except:
                pass

            await interaction.followup.send(
                f"❌ {error_msg}",
                ephemeral=True
            )

        except Exception as e:
            logger.error(f"Error saving content: {e}")
            await interaction.followup.send(
                f"❌ Unexpected error: {str(e)}",
                ephemeral=True
            )


def main():
    """Run the Discord bot."""
    if not settings.discord_bot_token:
        logger.error("DISCORD_BOT_TOKEN not set in environment")
        return

    bot = ContentBot()
    bot.run(settings.discord_bot_token)


if __name__ == "__main__":
    main()
