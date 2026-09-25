# K-Pop Demon Hunters: Mommy & Aira's Adventure

![Agent Demo](demo.gif)

An interactive, joyful, and kid-friendly AI agent adventure created with Google Agent Development Kit (ADK) and Gemini. Tailored specifically for Mommy (Sindhu) and her 6-year-old daughter (Aira), players join the 3 idol stars—**Rumi**, **Mira**, and **Zoey**—to solve arena mysteries, search for clues, and turn mischievous gremlins into cheering fans with rhythm and dance power!

---

## What the Agent Does

The agent operates as a live Game Master providing two primary interactive game modes:
1. **The Magical Treasure Hunt**: Explore concert arena rooms (stage, backstage, audio booth, costume studio) to find clues and recover the 3 Sacred Idol Treasures: *Rainbow Lightstick*, *Starlight Mic*, and *Glitter Beat Crystal*.
2. **Demon Dance Battle & Save the Day**: Encounter playful, non-violent demons (such as *Sparky the Groove Gremlin*) who playfully unplugged the stage sound system. Battles are resolved through dance combos, sparkles, high-fives, and team chants that fill the Harmony Meter to 100%!

### Implemented Agent Tools

The agent is powered by 10 wired ADK tools:
- `start_game_adventure`: Initializes or switches adventure game modes (`treasure_hunt` or `demon_dance_battle`).
- `search_location_for_clues`: Explores arena locations for secrets and riddles.
- `perform_dance_combo`: Executes kid-friendly dance moves (Sparkle Jump, Idol Wave, Neon Spin) that boost the Harmony Meter.
- `use_magical_gear`: Uses discovered tools and items during encounters.
- `list_magical_artifacts`: Queries the Firestore database to retrieve stored artifacts and gear.
- `record_magical_artifact`: Persists newly discovered magical items and trophies directly into Firestore.
- `search_kpop_music`: Searches for real K-Pop tracks via Apple iTunes Search API.
- `generate_item_image`: Generates high-quality illustrations of magical items using `gemini-3.1-flash-lite-image` on Vertex AI and uploads the output to Google Cloud Storage.
- `generate_item_video`: Generates short animated video clips using Google Omni (`gemini-omni-flash-preview`), saves artifacts to ADK tool context, and uploads video files to Google Cloud Storage.
- `PreloadMemoryTool`: Loads long-term preferences, favorite idols, and triumph history at the beginning of each session.

*(Note: Code sandbox execution was planned in early concepts but is not implemented in this version).*

---

## Connected Google Cloud Services

The project integrates directly with Google Cloud services:
- **Vertex AI / Gemini Models**:
  - `gemini-3.8-flash`: Powers the core reasoning, storytelling, and conversation.
  - `gemini-3.1-flash-lite-image`: Generates custom visual artwork for lightsticks, gear, and concert props.
  - `gemini-omni-flash-preview`: Generates short MP4 video clips directly in the `global` region.
- **Agent Engine Memory Bank**:
  - Provides cross-session episodic memory to remember Aira's favorite songs, idol members, and triumphs.
  - Integrated via `PreloadMemoryTool` and an asynchronous `after_agent_callback` (`generate_memories_callback`).
- **Google Cloud Firestore**:
  - Acts as the persistent artifact vault, saving and querying magical items, stats, and badges in the `magical_artifacts` collection.
- **Google Cloud Storage (GCS)**:
  - Public cloud media bucket hosting generated item images and video animations.
- **Agent-to-User Interface (A2UI)**:
  - Formats agent outputs with A2UI v0.8 cards, images, and structured metadata via `a2ui_callback`.

---

## Local Setup & Running Instructions

### Prerequisites
- Python 3.10+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- `google-agents-cli` (`uv tool install google-agents-cli`)
- Google Cloud SDK authenticated with access to Vertex AI, Firestore, and Cloud Storage.

### Installation

Clone the repository and install all dependencies:
```bash
uv sync
```

### Running the ADK Playground with Memory Bank

Run the ADK development playground with the Agent Engine Memory Bank attached:
```bash
uv run adk web . --port 8000 --reload_agents --memory_service_uri=agentengine://991977191556251648
```

Open your browser to the local dev UI:
```
http://127.0.0.1:8000/dev-ui/?app=app
```

### Running the Interactive Game Frontend

To run the custom concert arena interactive HUD and chat interface:
```bash
python3 frontend/main.py
```
Then navigate to:
```
http://127.0.0.1:8080/
```

### Running Tests

Execute the unit and integration test suite:
```bash
uv run pytest tests/unit tests/integration
```
