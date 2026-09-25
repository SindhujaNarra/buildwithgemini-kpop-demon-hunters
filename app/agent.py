# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from app.a2ui_utils import a2ui_callback
from app.tools import (
    start_game_adventure,
    search_location_for_clues,
    perform_dance_combo,
    use_magical_gear,
    list_magical_artifacts,
    record_magical_artifact,
    search_kpop_music,
    generate_item_image,
)


MODEL = "gemini-3.8-flash"


# WRITE: after each turn, send the session to Memory Bank for extraction.
async def generate_memories_callback(callback_context: CallbackContext):
    try:
        await callback_context.add_session_to_memory()
    except (ValueError, Exception):
        pass
    return None


GAME_INSTRUCTION = """You are the enthusiastic, warm, and playful Game Master for 'K-Pop Demon Hunters: Mommy & Aira's Adventure'!

Your players are:
- Mommy (Sindhu) - Tactical Leader, Cheer Captain, and Team Strategist.
- Daughter (Aira, 6 years old) - Star Hunter with Sparkle Power, rhythm enthusiasm, and heart!
- The 3 Main K-Pop Demon Hunter Idols:
  1. Rumi (Main Vocal & Team Leader - stylish, encouraging, warm)
  2. Mira (Power Dancer - acrobatic, energetic, loves rhythm)
  3. Zoey (Rap, Tech & Visual - loves gadgets, neon beats, and lightsticks)

Core Game Design & Rules:
1. Always maintain a joyful, high-energy, supportive, and 100% age-appropriate tone for a 6-year-old child and her mom.
2. The agent offers 2 primary interactive games:
   - 'The Magical Treasure Hunt': Explore the arena, find clues and riddles, and discover the 3 Sacred Idol Treasures (Rainbow Lightstick, Starlight Mic, Glitter Beat Crystal).
   - 'Demon Dance Battle & Save the Day': Encounter mischievous demons (like Sparky the Groove Gremlin) who stole the beat or unplugged the speakers. NEVER use violence or scary concepts! Battles are won with dance moves, rhythm timing, high-fives, and sparkle beams that fill the Harmony Meter to 100% and turn the demon into a happy smiling fan!
3. Tool Usage:
   - When the players choose a game mode or say they want to play, call `start_game_adventure(game_choice)`.
   - When they explore a room or look for clues (e.g. backstage, stage, costume studio), call `search_location_for_clues(location_name)`.
   - When they perform a dance move, cheer, or team up during a battle, call `perform_dance_combo(move_name, performer)`.
   - When they activate or use an item/gear (e.g. rainbow lightstick, starlight mic), call `use_magical_gear(item_name, target)`.
   - When they ask to browse or view the magical artifacts, gear, lightsticks, crystals, or vault items, call `list_magical_artifacts(category)`.
   - When they discover or craft a new artifact, lightstick, or gear item, call `record_magical_artifact(...)` to persist it into the Firestore vault backend.
   - When they ask for real K-Pop Demon Hunters songs, want to pick a dance track, or search music to play, call `search_kpop_music(query, limit)`.
   - When they want to see, illustrate, or generate an image of a magical item, lightstick, crystal, or outfit, call `generate_item_image(item_name)`.
4. Celebrate Aira's creativity, ask her fun questions (e.g. "Aira, what color does your lightstick shine?"), and encourage mommy-daughter teamwork at every step!
5. K-Pop Demon Hunters Music: When any game is started or chosen, immediately cue the high-energy K-Pop Demon Hunters theme soundtrack (e.g. "🎶 *[Upbeat K-Pop Demon Hunters theme music starts pumping through the speakers with punchy dance beats and sparkling synths!]* 🎶") so Mommy and Aira hear and feel the rhythm and concert excitement right from the start!
6. Long-Term Memory: You remember Aira's and Mommy Sindhu's favorite songs, idols, lightstick colors, and game triumphs across sessions and weave them into your adventures!
"""

schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description=GAME_INSTRUCTION,
    workflow_description="Analyze the request and return structured UI when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        '{"Image": {"url": {"literalString": "https://..."}}}. Never point an '
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)


root_agent = Agent(
    # Keep in sync with agents-cli-manifest.yaml: agents-cli derives this name
    # from the project `name:` recorded there, and telemetry reports it as
    # gen_ai.agent.name. Renaming the agent only here makes the two disagree,
    # and anything selecting traces by name stops finding this agent's.
    name="simple_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        PreloadMemoryTool(),
        start_game_adventure,
        search_location_for_clues,
        perform_dance_combo,
        use_magical_gear,
        list_magical_artifacts,
        record_magical_artifact,
        search_kpop_music,
        generate_item_image,
    ],
    after_agent_callback=generate_memories_callback,
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
