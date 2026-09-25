"""Seed script for K-Pop Demon Hunters Firestore backend.

Project ID is explicitly hardcoded as a string: 'qwiklabs-gcp-03-1bf51fd01203'.
"""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-1bf51fd01203"
COLLECTION_NAME = "magical_artifacts"

SEED_ITEMS = [
    {
        "item_id": "rainbow_lightstick",
        "name": "Rainbow Lightstick",
        "category": "lightstick",
        "description": "Glows with 7 vibrant neon colors when Aira and Sindhu cheer, lighting up hidden clue paths backstage.",
        "power_type": "Prism Sparkle",
        "location_found": "backstage_dressing_room",
        "unlocked": True,
        "harmony_bonus": 30,
        "owner": "Aira & Sindhu",
    },
    {
        "item_id": "starlight_mic",
        "name": "Starlight Mic",
        "category": "audio_relic",
        "description": "Amplifies Rumi and Aira's singing voices to gently calm down mischievous rhythm demons.",
        "power_type": "Vocal Harmony",
        "location_found": "sound_check_stage",
        "unlocked": True,
        "harmony_bonus": 25,
        "owner": "Rumi & Aira",
    },
    {
        "item_id": "glitter_beat_crystal",
        "name": "Glitter Beat Crystal",
        "category": "crystal",
        "description": "Pulsates with the energetic beat of K-Pop Demon Hunters, keeping everyone in rhythm during dance battles.",
        "power_type": "Rhythm Sync",
        "location_found": "neon_rooftop",
        "unlocked": False,
        "harmony_bonus": 35,
        "owner": "Mira & Zoey",
    },
    {
        "item_id": "secret_song_sheet",
        "name": "Golden Secret Song Sheet",
        "category": "song_sheet",
        "description": "Lyrics to the legendary melody that turns troublesome demons into smiling concert fans.",
        "power_type": "Lyric Inspiration",
        "location_found": "costume_studio",
        "unlocked": False,
        "harmony_bonus": 20,
        "owner": "Team Hunters",
    },
    {
        "item_id": "high_five_shield_badge",
        "name": "Mommy & Aira High-Five Ribbon",
        "category": "badge",
        "description": "Awarded for exceptional mother-daughter cooperation and sparkle energy during dance battles.",
        "power_type": "Teamwork Shield",
        "location_found": "concert_main_stage",
        "unlocked": True,
        "harmony_bonus": 40,
        "owner": "Sindhu & Aira",
    },
]


def seed():
    print(f"Connecting to Firestore for project: {PROJECT_ID}")
    db = firestore.Client(project=PROJECT_ID)
    collection = db.collection(COLLECTION_NAME)

    for item in SEED_ITEMS:
        doc_id = item["item_id"]
        doc_ref = collection.document(doc_id)
        doc_ref.set(item)
        print(f"  ✓ Seeded artifact: {item['name']} ({doc_id})")

    print(f"Successfully seeded {len(SEED_ITEMS)} items into '{COLLECTION_NAME}' collection.")


if __name__ == "__main__":
    seed()
