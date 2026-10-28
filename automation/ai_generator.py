"""
AI Content Generator for Dr. Santosh Gupta IVF Website.
Can generate new patient-centric topics using the Gemini API (or compatible LLM)
and append them to automation/topics.json.

Uses Python standard library (urllib.request) - requires zero external pip dependencies.
"""

import os
import sys
import json
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOPICS_FILE = os.path.join(SCRIPT_DIR, "topics.json")
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
LLMS_FILE = os.path.join(ROOT_DIR, "llms.md")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

AVAILABLE_IMAGES = [
    "assets/images/gallery-2.jpg",
    "assets/images/gallery-3.jpg",
    "assets/images/gallery-4.jpg",
    "assets/images/gallery-5.jpg",
    "assets/images/gallery-6.jpg",
    "assets/images/gallery-8.jpg",
    "assets/images/gallery-10.jpg",
    "assets/images/gallery-11.jpg",
    "assets/images/gallery-13.jpeg",
    "assets/images/gallery-14.jpeg",
    "assets/images/gallery-16.jpeg",
    "assets/images/gallery-17.jpeg",
    "assets/images/gallery-18.jpeg",
    "assets/images/gallery-19.jpg",
    "assets/images/gallery-20.jpg",
    "assets/images/gallery-21.jpg",
    "assets/images/gallery-22.jpg",
    "assets/images/gallery-23.jpg",
    "assets/images/gallery-24.jpg"
]

SYSTEM_PROMPT = """You are an expert medical writer and SEO/GEO strategist writing on behalf of Dr. Santosh Gupta.
Dr. Santosh Gupta is a Senior IVF Specialist and Gynecologist with 25+ years experience, consulting at Nova IVF Fertility in Koramangala and Bannerghatta Road, Bengaluru.
Her philosophy emphasizes customized care, transparency, and ethics over factory-line protocols.
Her core areas: Poor Ovarian Reserve, Recurrent Implantation Failure, Advanced Maternal Age (35+), PGT-A, Severe PCOS, Endometriosis, Male Factor ICSI.

Generate a comprehensive clinical blog topic JSON object for patients in Bengaluru.
Format MUST be valid JSON adhering to the exact schema:
{
  "slug": "url-friendly-slug-with-bengaluru-or-treatment",
  "title": "Engaging, Patient-Focused Medical Title",
  "category": "Category Name",
  "seo_title": "SEO Title (60 chars max) | Dr. Santosh Gupta Bengaluru",
  "meta_description": "150-160 char meta description with target keywords and doctor mention",
  "og_description": "Compelling OG description",
  "image": "assets/images/gallery-18.jpeg",
  "image_alt": "Detailed alt text with Dr. Santosh Gupta and Bengaluru context",
  "image_title": "Descriptive title for XML sitemap",
  "excerpt": "2-sentence excerpt for blog preview card",
  "cta_headline": "Consultation CTA Headline",
  "cta_text": "Consultation CTA Body referencing Koramangala and Bannerghatta Road",
  "published": false,
  "published_date": null,
  "sections": [
    {"type": "intro", "paragraphs": ["Paragraph 1...", "Paragraph 2...", "Paragraph 3..."]},
    {"type": "heading", "title": "Section Title"},
    {"type": "paragraphs", "paragraphs": ["Detailed clinical content..."]},
    {"type": "callout", "icon": "fa-solid fa-dna", "title": "Callout Title", "text": "Callout content..."},
    {"type": "heading", "title": "Section Title 2"},
    {"type": "cards", "cards": [{"icon": "fa-solid fa-star", "title": "Point 1", "description": "Details..."}, {"icon": "fa-solid fa-star", "title": "Point 2", "description": "Details..."}]},
    {"type": "heading", "title": "Clinical Solutions"},
    {"type": "list", "items": ["<strong>Point:</strong> Explanation...", "<strong>Point:</strong> Explanation..."]},
    {"type": "heading", "title": "Summary & Patient Guidance"},
    {"type": "paragraphs", "paragraphs": ["Reassuring conclusion..."]}
  ]
}
Return ONLY pure JSON. No markdown backticks or commentary.
"""


def generate_with_gemini(user_prompt):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY environment variable not set.")
        print("To generate with AI, set your GEMINI_API_KEY or use the rich pre-authored topics in topics.json.")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"text": f"Generate a patient-facing clinical blog topic addressing: {user_prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json"
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            candidate = result["candidates"][0]["content"]["parts"][0]["text"]
            # Clean possible markdown wrap
            cleaned = candidate.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            topic_obj = json.loads(cleaned.strip())
            return topic_obj
    except Exception as e:
        print(f"[ERROR] Failed to generate content with Gemini API: {e}")
        return None


def add_topic_to_queue(topic_obj):
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = json.load(f)

    # Check for duplicate slug
    existing_slugs = {t["slug"] for t in topics}
    if topic_obj["slug"] in existing_slugs:
        topic_obj["slug"] = f"{topic_obj['slug']}-2"

    topics.append(topic_obj)

    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Appended new topic '{topic_obj['title']}' to {TOPICS_FILE}")


CLINICAL_TOPIC_SEEDS = [
    "Low AMH in women under 30: premature ovarian insufficiency vs diminished reserve treatment paths in Bengaluru",
    "Uterine PRP (Platelet-Rich Plasma) for recurrent implantation failure and refractory thin endometrium",
    "Endometrial Receptivity Analysis (ERA), EMMA and ALICE: testing the uterine microbiome before IVF transfer",
    "ICSI vs IMSI vs PICSI: advanced sperm selection technologies for high DFI and severe male infertility",
    "Subclinical hypothyroidism and anti-TPO antibodies: impact on embryo implantation and miscarriage risk",
    "Mild stimulation Mini-IVF vs Conventional IVF: optimal protocols for poor ovarian responders over 38",
    "Laparoscopic ovarian drilling vs IVF for clomiphene-resistant PCOS: risks, indications and success",
    "Managing cortisol and sleep hygiene during IVF: evidence-based lifestyle guidance for Bengaluru professionals",
    "Hysteroscopic metroplasty for uterine septum: restoring reproductive anatomy after repeated miscarriages",
    "PGT-M vs PGT-A: genetic testing to prevent inherited single-gene conditions and chromosomal aneuploidies in India"
]


def auto_replenish_queue():
    """
    Called by publish.py if all topics in topics.json have been published.
    Generates a new clinical topic using Gemini API and appends it to the queue.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("[INFO] GEMINI_API_KEY not found in environment. Cannot auto-generate new topics via AI.")
        return None

    # Load existing topics to check slugs and titles
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            topics = json.load(f)
    else:
        topics = []

    existing_titles = {t["title"].lower() for t in topics}

    # Find the first seed prompt not yet covered
    chosen_prompt = CLINICAL_TOPIC_SEEDS[0]
    for seed in CLINICAL_TOPIC_SEEDS:
        if not any(seed.lower()[:20] in title for title in existing_titles):
            chosen_prompt = seed
            break

    print(f"[AUTONOMOUS AI] Generating new clinical topic from seed: '{chosen_prompt}'...")
    new_topic = generate_with_gemini(chosen_prompt)
    if new_topic:
        add_topic_to_queue(new_topic)
        return new_topic

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ai_generator.py '<patient topic or concern>' or '--auto-replenish'")
        print("Example: python ai_generator.py 'What to do when AMH is under 0.5 ng/ml'")
        sys.exit(1)

    if sys.argv[1] == "--auto-replenish":
        auto_replenish_queue()
    else:
        prompt = sys.argv[1]
        print(f"Generating clinical topic for: '{prompt}'...")
        new_topic = generate_with_gemini(prompt)
        if new_topic:
            add_topic_to_queue(new_topic)

