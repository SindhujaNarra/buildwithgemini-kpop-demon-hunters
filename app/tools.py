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

import json
import urllib.parse
import urllib.request
import uuid
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types as genai_types
from google.cloud import firestore, storage
from google.adk.tools import ToolContext

# Hardcoded GCP Project ID and Cloud Storage Bucket (avoids project-number bug on Agent Platform)
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-1bf51fd01203"
COLLECTION_NAME = "magical_artifacts"
GCS_BUCKET_NAME = "hangzhou-explorer-media-1bf51fd0"


def get_firestore_db() -> firestore.Client:
    """Returns a Firestore client with the hardcoded project ID."""
    return firestore.Client(project=FIRESTORE_PROJECT_ID)


# In-memory session game state store
_GAME_STATE: Dict[str, Any] = {
    "game_mode": "none",
    "treasures": [],
    "harmony_meter": 20,
    "active_demon": "Groove Gremlin Sparky",
    "demon_status": "playful_and_mischievous",
    "clues_found": [],
    "badges": ["Rookie Hunter Ribbon"],
}


def start_game_adventure(game_choice: str) -> Dict[str, Any]:
    """Starts or switches the game mode for Mommy (Sindhu) and Aira.

    Args:
        game_choice: The mode to play. Must be either 'treasure_hunt' or 'demon_dance_battle'.

    Returns:
        A dictionary with the initialization status, characters, and starting mission.
    """
    mode = game_choice.lower().strip()
    if "treasure" in mode:
        _GAME_STATE["game_mode"] = "treasure_hunt"
        _GAME_STATE["treasures"] = []
        _GAME_STATE["clues_found"] = []
        return {
            "status": "success",
            "game_mode": "The Magical Treasure Hunt",
            "idols": ["Rumi (Main Vocal)", "Mira (Lead Dancer)", "Zoey (Rap & Tech)"],
            "allies": ["Mommy (Sindhu) - Team Strategist", "Aira (Age 6) - Star Hunter with Sparkle Power"],
            "music": "kpop_demon_hunters_theme.wav",
            "music_status": "playing",
            "music_track": "K-Pop Demon Hunters: Neon Treasure Anthem",
            "story": (
                "🎶 [Music Starts Playing: The upbeat K-Pop Demon Hunters Theme kicks off with energetic drums and sparkling synths!] 🎶\n\n"
                "Welcome to the Neon Arena! Mischievous spirits hid the 3 Sacred Idol Treasures before "
                "the big world tour concert: the Rainbow Lightstick, the Starlight Mic, and the Glitter Beat Crystal. "
                "Explore locations like 'backstage_dressing_room', 'sound_check_stage', and 'costume_studio' to find clues!"
            ),
            "suggested_action": "Ask Aira which room she wants to search first!",
        }
    else:
        _GAME_STATE["game_mode"] = "demon_dance_battle"
        _GAME_STATE["harmony_meter"] = 25
        _GAME_STATE["demon_status"] = "stealing_the_beat"
        return {
            "status": "success",
            "game_mode": "Demon Dance Battle & Save the Day",
            "music": "kpop_demon_hunters_theme.wav",
            "music_status": "playing",
            "music_track": "K-Pop Demon Hunters: Stage Battle Beat",
            "active_demon": "Groove Gremlin Sparky (stealing the concert's rhythm)",
            "harmony_meter": "25%",
            "idols": ["Rumi", "Mira", "Zoey"],
            "allies": ["Sindhu (Cheer Leader)", "Aira (Sparkle Star)"],
            "story": (
                "🎶 [Music Starts Playing: High-energy K-Pop Demon Hunters Battle Beat starts playing!] 🎶\n\n"
                "Uh oh! Sparky the Groove Gremlin unplugged the concert speakers and is hopping to the beat! "
                "We don't hurt demons—we synchronize our dance moves, shine our sparkle beams, and fill the "
                "Harmony Meter to 100% to turn Sparky into a happy smiling fan!"
            ),
            "suggested_action": "Call perform_dance_combo with Aira's move (e.g. 'sparkle_twinkle_spin') or Mommy & Aira's 'high_five_shield'!",
        }


def search_location_for_clues(location_name: str) -> Dict[str, Any]:
    """Searches a specific concert venue location for treasure hunt clues or hidden artifacts.

    Args:
        location_name: The room to explore, such as 'backstage_dressing_room', 'sound_check_stage', 'costume_studio', or 'neon_rooftop'.

    Returns:
        A dictionary containing found clues, discovered treasures, and riddles.
    """
    loc = location_name.lower().replace(" ", "_")
    locations_data = {
        "backstage_dressing_room": {
            "clue": "Underneath the sparkling makeup mirror, something is glowing in pastel pink!",
            "treasure": "Rainbow Lightstick of Harmony",
            "riddle": "What is pink, shines bright like a star, and helps Aira cheer for her favorite idol?",
        },
        "sound_check_stage": {
            "clue": "Behind the big speaker stacks, a golden microphone is humming a sweet melody!",
            "treasure": "Starlight Microphone",
            "riddle": "When you sing into this, does your voice sound quiet like a mouse or joyful like an idol?",
        },
        "costume_studio": {
            "clue": "Inside a sequin jacket pocket, a magical crystal is pulsing with rhythm beats!",
            "treasure": "Glitter Beat Crystal",
            "riddle": "Can you tap your feet three times to unlock the crystal's sparkle?",
        },
        "neon_rooftop": {
            "clue": "Up on the roof, colorful lightstick balloons are floating towards the starry night sky!",
            "treasure": "Superstar Friendship Banner",
            "riddle": "Who makes the best demon hunter team in the whole world? (Hint: Mommy & Aira!)",
        },
    }

    match = locations_data.get(loc)
    if not match:
        return {
            "status": "not_found",
            "location": location_name,
            "message": f"You and Aira checked the {location_name}. It's safe and quiet here, but try 'backstage_dressing_room', 'sound_check_stage', or 'costume_studio'!",
        }

    if match["treasure"] not in _GAME_STATE["treasures"]:
        _GAME_STATE["treasures"].append(match["treasure"])
        _GAME_STATE["clues_found"].append(match["clue"])

    all_found = len(_GAME_STATE["treasures"]) >= 3
    if all_found and "Master Treasure Hunter" not in _GAME_STATE["badges"]:
        _GAME_STATE["badges"].append("Master Treasure Hunter")

    return {
        "status": "found",
        "location": location_name,
        "clue": match["clue"],
        "treasure_unlocked": match["treasure"],
        "fun_riddle": match["riddle"],
        "total_treasures_collected": len(_GAME_STATE["treasures"]),
        "all_treasures_found": all_found,
    }


def perform_dance_combo(move_name: str, performer: str) -> Dict[str, Any]:
    """Executes a joyful dance, song, or sparkle combo move against a mischievous demon to fill the Harmony Meter.

    Args:
        move_name: The name of the move, e.g. 'sparkle_twinkle_spin', 'high_five_harmony', 'heart_laser_beam', or 'super_chorus'.
        performer: Who executes the move: 'Aira', 'Sindhu', 'Mommy and Aira', or 'Hunter Idols'.

    Returns:
        A dictionary with the move impact, sparkle points gained, and the updated Harmony Meter.
    """
    meter = _GAME_STATE.get("harmony_meter", 25)
    boost = 30
    if "high_five" in move_name.lower() or "mommy" in performer.lower():
        boost = 40  # Extra power for mother-daughter teamwork!

    new_meter = min(100, meter + boost)
    _GAME_STATE["harmony_meter"] = new_meter

    if new_meter >= 100:
        _GAME_STATE["demon_status"] = "happy_reformed_fan"
        if "Concert Savior Badge" not in _GAME_STATE["badges"]:
            _GAME_STATE["badges"].append("Concert Savior Badge")
        victory = True
        effect = (
            f"✨ Spectacular combo! {performer} performed '{move_name}'! A wave of pink sparkles and musical notes "
            "showered the arena! Sparky the Gremlin's eyes lit up with hearts, and he put on a neon headband and started cheering! "
            "You saved the concert and made a new best friend!"
        )
    else:
        victory = False
        effect = (
            f"🌟 Awesome move! {performer} rocked '{move_name}'! Sparkles burst across the floor! "
            f"The demon stopped misbehaving and is starting to tap his feet to the rhythm!"
        )

    return {
        "status": "success",
        "move": move_name,
        "performer": performer,
        "harmony_meter": f"{new_meter}%",
        "effect_description": effect,
        "demon_saved": victory,
    }


def use_magical_gear(item_name: str, target: str = "arena") -> Dict[str, Any]:
    """Uses an unlocked magical artifact/gear from the inventory to solve a puzzle or boost a dance battle.

    Args:
        item_name: Name or slug of the item (e.g. 'rainbow_lightstick', 'starlight_mic', 'glitter_beat_crystal').
        target: Where or on whom to use the item (e.g. 'dark_backstage', 'mischievous_demon', 'stage_door').

    Returns:
        A dictionary describing the action outcome, sparkle effect, and harmony boost.
    """
    clean_id = item_name.strip().lower().replace(" ", "_")
    
    # Try fetching from Firestore first, fallback to standard catalog
    item_doc = get_magical_artifact(clean_id)
    if item_doc.get("status") == "success" and item_doc.get("artifact"):
        artifact = item_doc["artifact"]
        name = artifact.get("name", item_name)
        bonus = artifact.get("harmony_bonus", 25)
        power = artifact.get("power_type", "Magical Sparkle")
    else:
        name = item_name.title()
        bonus = 25
        power = "Sparkle Star Power"

    current_meter = _GAME_STATE.get("harmony_meter", 20)
    updated_meter = min(100, current_meter + bonus)
    _GAME_STATE["harmony_meter"] = updated_meter

    action_text = (
        f"✨ Aira and Sindhu activated the [{name}]! It released a dazzling wave of {power} towards {target}! "
        f"The room illuminated with neon sparkles, boosting the Harmony Meter by +{bonus} points to {updated_meter}%!"
    )

    return {
        "status": "success",
        "item_used": name,
        "target": target,
        "power_unleashed": power,
        "harmony_boost": f"+{bonus}",
        "new_harmony_meter": f"{updated_meter}%",
        "story_result": action_text,
    }


def check_team_inventory() -> Dict[str, Any]:
    """Checks Sindhu and Aira's current game badges, collected treasures, and harmony stats.

    Returns:
        A dictionary listing current badges, treasures found, and team status.
    """
    artifacts_data = list_magical_artifacts()
    unlocked_artifacts = [
        item["name"]
        for item in artifacts_data.get("artifacts", [])
        if item.get("unlocked", False)
    ]
    return {
        "team_name": "Mommy Sindhu & Superstar Aira",
        "game_mode": _GAME_STATE.get("game_mode", "ready"),
        "badges": _GAME_STATE.get("badges", []),
        "treasures_collected": _GAME_STATE.get("treasures", []),
        "unlocked_vault_artifacts": unlocked_artifacts,
        "harmony_meter": f"{_GAME_STATE.get('harmony_meter', 20)}%",
        "friendship_level": "Best Friends Forever (Max Star Tier)",
    }


# ============================================================================
# Firestore Backend Function Tools (Collection: magical_artifacts)
# ============================================================================

def list_magical_artifacts(category: str = "") -> Dict[str, Any]:
    """Reads all magical artifacts, lightsticks, crystals, and gear from the Firestore database.

    Args:
        category: Optional filter by item category ('lightstick', 'crystal', 'song_sheet', 'badge', 'audio_relic').

    Returns:
        A dictionary with the count and list of artifacts stored in Firestore.
    """
    try:
        db = get_firestore_db()
        coll_ref = db.collection(COLLECTION_NAME)
        if category:
            query = coll_ref.where("category", "==", category.strip().lower())
            docs = query.stream()
        else:
            docs = coll_ref.stream()

        artifacts: List[Dict[str, Any]] = []
        for doc in docs:
            data = doc.to_dict()
            data["doc_id"] = doc.id
            artifacts.append(data)

        return {
            "status": "success",
            "backend": f"Firestore ({FIRESTORE_PROJECT_ID})",
            "collection": COLLECTION_NAME,
            "filter_category": category if category else "all",
            "count": len(artifacts),
            "artifacts": artifacts,
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to read from Firestore: {str(e)}",
            "artifacts": [],
        }


def get_magical_artifact(item_id: str) -> Dict[str, Any]:
    """Reads the details of a specific magical artifact from the Firestore database.

    Args:
        item_id: The unique identifier of the artifact (e.g. 'rainbow_lightstick', 'starlight_mic', 'glitter_beat_crystal').

    Returns:
        A dictionary with the artifact's properties, powers, and unlocked status.
    """
    try:
        db = get_firestore_db()
        doc_ref = db.collection(COLLECTION_NAME).document(item_id.strip())
        doc = doc_ref.get()
        if not doc.exists:
            return {
                "status": "not_found",
                "item_id": item_id,
                "message": f"Artifact '{item_id}' not found in the Firestore vault.",
            }
        data = doc.to_dict()
        data["doc_id"] = doc.id
        return {
            "status": "success",
            "item_id": item_id,
            "artifact": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve artifact '{item_id}' from Firestore: {str(e)}",
        }


def record_magical_artifact(
    item_id: str,
    name: str,
    category: str,
    description: str,
    power_type: str,
    harmony_bonus: int = 25,
    location_found: str = "Neon Arena",
    owner: str = "Aira & Sindhu",
    unlocked: bool = True,
) -> Dict[str, Any]:
    """Writes a new magical artifact or gear item into the Firestore database backend.

    Args:
        item_id: Unique slug ID for the artifact (e.g. 'neon_glitter_baton').
        name: Display name (e.g. 'Neon Glitter Baton').
        category: Item category ('lightstick', 'crystal', 'song_sheet', 'badge', 'gear').
        description: Friendly description of what the item does and looks like.
        power_type: Special sparkle or musical power type (e.g. 'Sparkle Rhythm Boost').
        harmony_bonus: Points added to the harmony meter (default 25).
        location_found: Room or stage where discovered.
        owner: Team members who can wield it (default 'Aira & Sindhu').
        unlocked: Whether the item is unlocked and ready to use.

    Returns:
        A dictionary confirming the artifact was saved to Firestore.
    """
    try:
        db = get_firestore_db()
        doc_data = {
            "item_id": item_id.strip(),
            "name": name.strip(),
            "category": category.strip().lower(),
            "description": description.strip(),
            "power_type": power_type.strip(),
            "harmony_bonus": int(harmony_bonus),
            "location_found": location_found.strip(),
            "owner": owner.strip(),
            "unlocked": bool(unlocked),
        }
        doc_ref = db.collection(COLLECTION_NAME).document(item_id.strip())
        doc_ref.set(doc_data)
        return {
            "status": "success",
            "message": f"Magical artifact '{name}' successfully saved in Firestore vault!",
            "artifact": doc_data,
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to write artifact '{name}' to Firestore: {str(e)}",
        }


def unlock_magical_artifact(item_id: str, location_found: str = "") -> Dict[str, Any]:
    """Updates an existing artifact in Firestore to mark it as unlocked when Aira and Sindhu find it.

    Args:
        item_id: The ID of the artifact to unlock.
        location_found: The location where it was discovered.

    Returns:
        A dictionary confirming the artifact has been unlocked.
    """
    try:
        db = get_firestore_db()
        doc_ref = db.collection(COLLECTION_NAME).document(item_id.strip())
        doc = doc_ref.get()
        if not doc.exists:
            return {
                "status": "not_found",
                "item_id": item_id,
                "message": f"Cannot unlock '{item_id}' because it does not exist in Firestore.",
            }

        updates: Dict[str, Any] = {"unlocked": True}
        if location_found:
            updates["location_found"] = location_found.strip()

        doc_ref.update(updates)
        updated_data = doc_ref.get().to_dict()
        return {
            "status": "success",
            "message": f"Artifact '{item_id}' is now unlocked and available in the inventory!",
            "artifact": updated_data,
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to unlock artifact in Firestore: {str(e)}",
        }


# ============================================================================
# Free Public API Function Tool (iTunes Public Music Search API)
# ============================================================================

def search_kpop_music(query: str = "kpop demon hunters", limit: int = 3) -> Dict[str, Any]:
    """Searches real K-Pop songs and music audio previews from the public iTunes API.

    Args:
        query: Search term for the song, group, or theme (e.g. 'kpop demon hunters', 'golden', 'bts', 'blackpink').
        limit: Number of music tracks to return (default 3, max 5).

    Returns:
        A dictionary with real track names, artists, album collection, preview audio URLs, and album artwork.
    """
    encoded_query = urllib.parse.quote(query.strip())
    safe_limit = max(1, min(int(limit), 5))
    url = f"https://itunes.apple.com/search?term={encoded_query}&entity=song&limit={safe_limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "KPopDemonHunters/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            tracks = []
            for track in data.get("results", []):
                tracks.append({
                    "track_name": track.get("trackName"),
                    "artist_name": track.get("artistName"),
                    "album": track.get("collectionName"),
                    "preview_url": track.get("previewUrl"),
                    "artwork_url": track.get("artworkUrl100"),
                })
            return {
                "status": "success",
                "api": "iTunes Search API (Public / Free)",
                "query": query,
                "count": len(tracks),
                "tracks": tracks,
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search K-pop music: {str(e)}",
            "tracks": [],
        }


# ============================================================================
# Image Generation Function Tool (gemini-3.1-flash-lite-image in global region)
# ============================================================================

async def generate_item_image(
    item_name: str,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Generates a vibrant illustration for a K-Pop Demon Hunters magical item, gear, or character outfit.

    Uses the gemini-3.1-flash-lite-image model in the global region, saves the image
    to the session artifacts (Playground panel), and uploads to Google Cloud Storage.

    Args:
        item_name: Name or description of the magical item, lightstick, crystal, or outfit (e.g. 'Rainbow Lightstick', 'Starlight Mic', 'Glitter Beat Crystal', 'Aira Sparkle Stage Outfit').
        tool_context: Optional session tool context injected by the framework.

    Returns:
        A dictionary with the public Cloud Storage HTTPS URL, item name, and artifact status.
    """
    prompt = (
        f"A vibrant, colorful, family-friendly anime K-Pop Demon Hunters illustration of '{item_name}'. "
        "Magical sparkling neon aesthetic, glowing crystal and lightstick effects, high quality idol stage prop, "
        "whimsical, cheerful, and 100% child-friendly."
    )

    client = genai.Client(vertexai=True, project=FIRESTORE_PROJECT_ID, location="global")
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=prompt,
        config=genai_types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    image_bytes = None
    mime_type = "image/jpeg"
    for part in response.parts:
        if part.inline_data:
            image_bytes = part.inline_data.data
            mime_type = part.inline_data.mime_type or "image/jpeg"
            break

    if not image_bytes:
        return {
            "status": "error",
            "message": f"Model failed to generate image bytes for '{item_name}'.",
        }

    clean_slug = item_name.strip().lower().replace(" ", "_").replace("/", "_")
    unique_suffix = uuid.uuid4().hex[:8]
    ext = "jpg" if "jpeg" in mime_type else "png"
    object_name = f"artifacts/{clean_slug}_{unique_suffix}.{ext}"
    filename = f"{clean_slug}.{ext}"

    # (1) Save artifact with tool_context.save_artifact so it shows up in Playground's Artifacts panel
    artifact_saved = False
    if tool_context is not None:
        try:
            artifact_part = genai_types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            await tool_context.save_artifact(filename=filename, artifact=artifact_part)
            artifact_saved = True
        except Exception as e:
            print(f"Warning: could not save artifact to tool_context: {e}")

    # (2) Upload the same image bytes to the public Cloud Storage bucket
    storage_client = storage.Client(project=FIRESTORE_PROJECT_ID)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(object_name)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{object_name}"

    return {
        "status": "success",
        "item_name": item_name,
        "public_url": public_url,
        "filename": filename,
        "artifact_saved": artifact_saved,
        "message": f"✨ Generated vibrant image for '{item_name}'! View it at: {public_url}",
    }



