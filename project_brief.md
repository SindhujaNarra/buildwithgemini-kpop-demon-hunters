# My agent: K-Pop Demon Hunters: Mommy & Aira's Adventure

One-liner: A family-friendly conversational interactive game agent that takes Sindhu (Mommy) and Aira (6 years old) into the K-pop Demon Hunter world alongside the 3 main idols to solve a magical treasure hunt and team up to defeat mischievous demons and save the day.

## Game Concept & Adventures
1. **The Cast**:
   - The 3 Main K-Pop Demon Hunter Idols
   - Mommy (Sindhu) - Tactical Leader & Cheer Booster
   - Daughter (Aira, age 6) - Star Hunter with Sparkle Power
2. **Game 1: The Magical Treasure Hunt**:
   - Clue-by-clue quest around the concert arena and enchanted studio.
   - Collect magical artifacts: Glowing Lightsticks, Melody Crystals, and Secret Song Sheets.
3. **Game 2: Demon Dance Battle & Save the Day**:
   - Age-appropriate, playful encounters with mischievous groove demons (e.g., Rhythm Thief, Shadow Glitter Sprite).
   - Defeat demons using teamwork, synchronized dance moves, high-fives, and sparkle beams to turn them back into cute friendly spirits.

Tool coverage:
- Memory: Remembers Aira and Sindhu's team profile, gathered treasures/inventory, star badges earned, and friendship levels with each idol.
- Tools:
  - `inspect_area_clue(location)`: Searches for treasure clues and reveals riddles.
  - `use_magical_item(item_name)`: Uses collected gear (like Neon Lightstick or Rhythm Charm) to solve puzzles.
  - `perform_combo_move(move_name, participants)`: Executes cooperative hunter dance moves during encounters.
  - `check_inventory()`: Displays current badges, crystals, and treasures found.
- Catalog/UI: Rich A2UI display cards for:
  - Character Dossier Cards (Aira, Sindhu, and the 3 idols with special abilities).
  - Treasure & Lightstick Collection Cards.
  - Mischievous Demon Profile Cards (silly weaknesses, favorite beats).
- Image gen: Vibrant, age-appropriate anime/K-pop styled illustrations:
  - Aira and Sindhu in custom glowing stage hunter outfits.
  - Cute, colorful demon spirits and magical treasure chests.
  - Epic and joyful concert victory celebration scenes.
- Sandbox: Fun mini-game computation (decoding rhythm patterns, tallying sparkle stars, and puzzle math).

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits): Code sandbox for mini-game rhythm puzzles and star score calculation.
