"""
Autonomous Topic & Content Engine for Dr. Santosh Gupta IVF Website.
Ensures a continuous, zero-downtime backlog of high-value, patient-intent,
SEO & GEO-optimized clinical blog posts tailored to Bengaluru patients.

Features:
1. Dynamic AI Generation: Calls Gemini API (gemini-2.0-flash / gemini-1.5-flash)
   with knowledge of existing topics to invent fresh, non-duplicative, high-converting topics.
2. Resilient Clinical Vault Fallback: If GEMINI_API_KEY is missing or fails,
   falls back to an extensive built-in clinical topic vault with pre-structured clinical content.
3. Queue Health Buffer: Automatically maintains a safety buffer of at least 3-5
   unpublished topics in automation/topics.json so the blog NEVER stalls.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOPICS_FILE = os.path.join(SCRIPT_DIR, "topics.json")
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

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
Her core clinical focus areas:
- Poor Ovarian Reserve & Low AMH (<1.0 ng/mL), DuoStim, Mini-IVF
- Recurrent Implantation Failure (RIF), Uterine PRP, ERA / EMMA / ALICE testing
- Advanced Maternal Age (35+ and 40+), PGT-A genetic screening
- High Sperm DNA Fragmentation (DFI), PICSI, IMSI, severe male factor
- Endometriosis & Adenomyosis, down-regulation protocols
- Recurrent Pregnancy Loss / Miscarriage, Thrombophilia, Reproductive Immunology
- Safe PCOS protocols, OHSS prevention, personalized stimulation

The target audience consists of discerning couples and working professionals in Bengaluru (Koramangala, HSR Layout, Bannerghatta Road, JP Nagar, Indiranagar, Whitefield).

Generate a comprehensive clinical blog topic JSON object.
Format MUST be strictly valid JSON adhering to this schema:
{
  "slug": "url-friendly-slug-with-bengaluru-or-treatment",
  "title": "Engaging, Patient-Focused Medical Title",
  "category": "Category Name",
  "seo_title": "SEO Title (60 chars max) | Dr. Santosh Gupta Bengaluru",
  "meta_description": "150-160 char meta description with target keywords and doctor mention",
  "og_description": "Compelling OG description for social sharing",
  "image": "assets/images/gallery-22.jpg",
  "image_alt": "Detailed alt text with Dr. Santosh Gupta and Bengaluru context",
  "image_title": "Descriptive title for XML sitemap",
  "excerpt": "2-sentence excerpt for blog preview card",
  "cta_headline": "Consultation CTA Headline",
  "cta_text": "Schedule a personalized consultation with Dr. Santosh Gupta at Nova IVF Fertility in Koramangala or Bannerghatta Road, Bengaluru.",
  "published": false,
  "published_date": null,
  "sections": [
    {"type": "intro", "paragraphs": ["Paragraph 1...", "Paragraph 2...", "Paragraph 3..."]},
    {"type": "heading", "title": "Section Title 1"},
    {"type": "paragraphs", "paragraphs": ["Detailed clinical content..."]},
    {"type": "callout", "icon": "fa-solid fa-notes-medical", "title": "Clinical Takeaway", "text": "Crucial medical insight..."},
    {"type": "heading", "title": "Section Title 2"},
    {"type": "cards", "cards": [{"icon": "fa-solid fa-circle-check", "title": "Point 1", "description": "Details..."}, {"icon": "fa-solid fa-circle-check", "title": "Point 2", "description": "Details..."}]},
    {"type": "heading", "title": "Evidence-Based Guidance"},
    {"type": "list", "items": ["<strong>Point:</strong> Explanation...", "<strong>Point:</strong> Explanation..."]},
    {"type": "heading", "title": "Summary & Next Steps"},
    {"type": "paragraphs", "paragraphs": ["Empathetic, reassuring conclusion from Dr. Santosh Gupta..."]}
  ]
}
Return ONLY valid JSON. No markdown fences or conversational filler.
"""

# Extensive Fallback Vault of clinical topics ready to be generated when AI is offline
CLINICAL_VAULT_TOPICS = [
    {
        "slug": "uterine-natural-killer-cells-ivf-immunology-bengaluru",
        "title": "Uterine Natural Killer (uNK) Cells in IVF: When Does the Immune System Reject Embryos?",
        "category": "Reproductive Immunology",
        "seo_title": "uNK Cells & Immune IVF Failure | Dr. Santosh Gupta Bengaluru",
        "meta_description": "Recurrent IVF failure or unexplained miscarriages? Dr. Santosh Gupta explains Uterine Natural Killer (uNK) cells, immunological rejection, and therapies in Bengaluru.",
        "og_description": "Learn how elevated uterine Natural Killer cells can attack implanting embryos and how immunomodulatory protocols restore IVF success in Bengaluru.",
        "image": "assets/images/gallery-20.jpg",
        "image_alt": "Senior IVF Specialist Dr. Santosh Gupta presenting clinical insights on reproductive immunology and uNK cells in Bengaluru",
        "image_title": "Dr. Santosh Gupta discussing uterine natural killer cells and IVF immunology in Bengaluru",
        "excerpt": "When chromosomally normal embryos fail to implant, an overactive maternal immune system may be attacking the embryo. Discover how uNK testing guides treatment.",
        "cta_headline": "Suspecting Immune Factors in Your IVF Failures?",
        "cta_text": "Schedule a specialized reproductive immunology consultation with Dr. Santosh Gupta at Nova IVF Fertility in Koramangala or Bannerghatta Road, Bengaluru.",
        "published": False,
        "published_date": None,
        "sections": [
            {
                "type": "intro",
                "paragraphs": [
                    "An embryo is biologically unique: because half of its genetic material originates from the father, it is an 'allograft'—a foreign entity that the maternal immune system must tolerate rather than attack. In normal conception, the uterus undergoes a miraculous state of immune tolerance.",
                    "However, in a subset of women experiencing Recurrent Implantation Failure (RIF) or recurrent early pregnancy losses, this immune tolerance breaks down. The maternal immune system mistakenly identifies the trophoblast cells of the embryo as harmful invaders.",
                    "At Nova IVF Fertility in Bengaluru, Senior IVF Consultant Dr. Santosh Gupta investigates the role of <strong>Uterine Natural Killer (uNK) cells, TH1/TH2 cytokine ratios, and autoantibodies</strong> to design personalized immunological treatment protocols."
                ]
            },
            {
                "type": "heading",
                "title": "What Are Uterine Natural Killer (uNK) Cells?"
            },
            {
                "type": "paragraphs",
                "paragraphs": [
                    "Unlike peripheral blood Natural Killer (pNK) cells that circulate to destroy viruses and cancer cells, <strong>Uterine Natural Killer (uNK) cells</strong> reside specifically within the endometrial lining. Under normal conditions, they are essential for remodeling the spiral arteries that nourish the placenta.",
                    "However, when uNK cell density is excessively high or when their cytotoxicity is improperly regulated, they secrete pro-inflammatory cytokines like TNF-alpha and Interferon-gamma. These cytokines induce micro-thrombosis at the implantation site and trigger apoptosis (programmed cell death) in the invading blastocyst."
                ]
            },
            {
                "type": "callout",
                "icon": "fa-solid fa-shield-virus",
                "title": "uNK Biopsy vs Blood Tests",
                "text": "Peripheral blood NK cell levels do not always mirror what is happening inside the uterus. A luteal-phase endometrial biopsy with CD56+ immunohistochemistry provides the most accurate assessment of uterine immune activity."
            },
            {
                "type": "heading",
                "title": "Evidence-Based Immunomodulatory Therapies"
            },
            {
                "type": "cards",
                "cards": [
                    {
                        "icon": "fa-solid fa-droplet",
                        "title": "Intralipid Infusions",
                        "description": "Fat emulsion infusions containing soybean oil and egg phospholipids that safely down-regulate excessive NK cell cytotoxicity without compromising maternal immunity."
                    },
                    {
                        "icon": "fa-solid fa-pills",
                        "title": "Low-Dose Corticosteroids",
                        "description": "Oral prednisolone or methylprednisolone administered from early cycle to dampen uterine inflammatory cytokine cascades during the implantation window."
                    },
                    {
                        "icon": "fa-solid fa-shield-halved",
                        "title": "Low-Dose Aspirin & LMWH",
                        "description": "Anti-platelet and anti-coagulant therapies that prevent micro-vascular clotting in fragile decidual spiral arteries."
                    },
                    {
                        "icon": "fa-solid fa-sun",
                        "title": "Vitamin D3 Optimization",
                        "description": "Correcting vitamin D deficiency, which acts as a potent biological immunomodulator shifting the uterus from inflammatory TH1 to receptive TH2 dominance."
                    }
                ]
            },
            {
                "type": "heading",
                "title": "Dr. Santosh Gupta's Clinical Verdict"
            },
            {
                "type": "paragraphs",
                "paragraphs": [
                    "Reproductive immunology is an advanced field requiring scientific caution. We do not recommend aggressive immune therapies blindly; rather, we reserve these targeted protocols for patients with proven recurrent implantation failure or unexplained miscarriages.",
                    "If you have suffered multiple failed transfers with top-quality embryos, evaluating your endometrial immune environment can unlock the answers you need. We welcome you to our Bengaluru clinics for a thorough, evidence-based review."
                ]
            }
        ]
    },
    {
        "slug": "thrombophilia-heparin-aspirin-ivf-miscarriage-bengaluru",
        "title": "Inherited Thrombophilia and IVF: How Low Molecular Weight Heparin Prevents Pregnancy Loss",
        "category": "High-Risk Pregnancy & RPL",
        "seo_title": "Thrombophilia & LMWH in IVF | Dr. Santosh Gupta Bengaluru",
        "meta_description": "Repeated miscarriages or IVF failures? Dr. Santosh Gupta explains how inherited thrombophilia causes micro-clots in the placenta and how Heparin & Aspirin restore live births.",
        "og_description": "Understand how Factor V Leiden, Protein C/S deficiency, and MTHFR gene mutations cause pregnancy loss and how LMWH (Clexane/Enoxaparin) saves pregnancies in Bengaluru.",
        "image": "assets/images/gallery-2.jpg",
        "image_alt": "Senior fertility specialist Dr. Santosh Gupta addressing a medical conference on recurrent pregnancy loss and thrombophilia protocols",
        "image_title": "Dr. Santosh Gupta presenting thrombophilia and recurrent miscarriage protocols in Bengaluru",
        "excerpt": "Silent clotting disorders often cause early embryo loss by cutting off micro-capillaries in the placenta. Learn how Low Molecular Weight Heparin protects your pregnancy.",
        "cta_headline": "Experienced Recurrent Miscarriages or Failed Transfers?",
        "cta_text": "Schedule a detailed recurrent pregnancy loss evaluation with Dr. Santosh Gupta at Nova IVF Fertility in Koramangala or Bannerghatta Road, Bengaluru.",
        "published": False,
        "published_date": None,
        "sections": [
            {
                "type": "intro",
                "paragraphs": [
                    "For couples attempting conception, nothing is more bewildering than achieving a positive pregnancy test, only to lose the heartbeat at 6, 8, or 10 weeks. When this trauma happens more than once, genetic, anatomical, and hematological investigations are paramount.",
                    "One of the most treatable root causes of recurrent pregnancy loss and late implantation failure is <strong>Thrombophilia</strong>—a group of genetic and acquired conditions that predispose blood to form microscopic clots too easily.",
                    "At Nova IVF Fertility in Bengaluru, Senior IVF Specialist Dr. Santosh Gupta screens for inherited and acquired thrombophilias to administer targeted anticoagulant therapy that preserves early placental circulation."
                ]
            },
            {
                "type": "heading",
                "title": "How Thrombophilia Sabotages Implantation and Pregnancy"
            },
            {
                "type": "paragraphs",
                "paragraphs": [
                    "During the early weeks of pregnancy, the developing embryo invades the maternal uterine wall, transforming narrow maternal spiral arteries into wide, low-resistance vascular channels. This nascent placental circulation involves capillaries so microscopic that even a tiny micro-thrombus (blood clot) can completely cut off oxygen and nutrient delivery to the embryo.",
                    "In women with thrombophilia, the delicate balance between clotting and clot-dissolving factors is skewed toward hypercoagulability. Micro-thrombi develop at the maternal-fetal interface, causing embryonic demise, subchorionic hematomas, or fetal growth restriction."
                ]
            },
            {
                "type": "callout",
                "icon": "fa-solid fa-syringe",
                "title": "Low Molecular Weight Heparin (LMWH)",
                "text": "Daily subcutaneous injections of Enoxaparin (Clexane) or Dalteparin, combined with low-dose aspirin, prevent micro-clotting and promote trophoblast invasion with extraordinary safety for both mother and fetus."
            },
            {
                "type": "heading",
                "title": "Key Thrombophilia Markers We Screen in Bengaluru"
            },
            {
                "type": "cards",
                "cards": [
                    {
                        "icon": "fa-solid fa-dna",
                        "title": "Factor V Leiden & Prothrombin Gene",
                        "description": "Common inherited mutations that impair the body's natural anticoagulant mechanisms, dramatically increasing thrombosis risk."
                    },
                    {
                        "icon": "fa-solid fa-vial-virus",
                        "title": "Antiphospholipid Syndrome (APLA)",
                        "description": "Acquired autoimmune antibodies (Lupus Anticoagulant, Anticardiolipin, Anti-Beta2 Glycoprotein) that attack maternal blood vessel linings."
                    },
                    {
                        "icon": "fa-solid fa-shield-halved",
                        "title": "Protein C, Protein S & Antithrombin III",
                        "description": "Deficiencies in these natural anticoagulant proteins lead to unopposed fibrin formation in the placental bed."
                    },
                    {
                        "icon": "fa-solid fa-chart-line",
                        "title": "MTHFR & Homocysteine",
                        "description": "Elevated serum homocysteine levels due to MTHFR gene variants that cause vascular endothelial inflammation and micro-clotting."
                    }
                ]
            },
            {
                "type": "heading",
                "title": "Dr. Santosh Gupta's Guidance"
            },
            {
                "type": "paragraphs",
                "paragraphs": [
                    "If you have endured repeated miscarriages, do not lose hope. In the vast majority of cases where thrombophilia is identified, instituting a precise regimen of low-dose aspirin and LMWH from the day of embryo transfer or positive beta-hCG transforms a history of pregnancy loss into a healthy live birth.",
                    "Visit us at our Koramangala or Bannerghatta Road clinics in Bengaluru to review your history and establish a protective clinical roadmap."
                ]
            }
        ]
    },
    {
        "slug": "uterine-fibroids-myomectomy-ivf-implantation-bengaluru",
        "title": "Uterine Fibroids and Fertility: Which Fibroids Must Be Removed Before Starting IVF?",
        "category": "Gynecological Surgery",
        "seo_title": "Fibroids & IVF: When is Surgery Needed? | Dr. Santosh Gupta",
        "meta_description": "Diagnosed with fibroids before IVF? Dr. Santosh Gupta explains which fibroids reduce implantation rates (submucosal vs intramural) and when myomectomy is necessary in Bengaluru.",
        "og_description": "A clear clinical guide on uterine fibroids and fertility: understand FIGO classifications, surgical vs non-surgical management, and IVF success in Bengaluru.",
        "image": "assets/images/gallery-23.jpg",
        "image_alt": "Senior Gynecologist and IVF Specialist Dr. Santosh Gupta receiving felicitation for endoscopic surgical excellence in Bengaluru",
        "image_title": "Dr. Santosh Gupta discussing uterine fibroids and fertility surgery in Bengaluru",
        "excerpt": "Not all fibroids cause infertility. Learn which fibroid locations directly obstruct implantation and how minimally invasive surgery prepares the uterus for IVF.",
        "cta_headline": "Have You Been Diagnosed with Uterine Fibroids?",
        "cta_text": "Get an expert gynecological and fertility opinion from Dr. Santosh Gupta at Nova IVF Fertility in Koramangala or Bannerghatta Road, Bengaluru.",
        "published": False,
        "published_date": None,
        "sections": [
            {
                "type": "intro",
                "paragraphs": [
                    "Uterine fibroids (leiomyomas) are non-cancerous muscular tumors of the uterus found in up to 30% to 50% of women in their 30s and 40s. Many women are alarmed when a routine ultrasound reveals fibroids, immediately wondering: 'Can I still get pregnant? Do I need major surgery before doing IVF?'",
                    "The answer depends entirely on one golden rule: <strong>Location is far more important than size</strong>.",
                    "A large 6 cm subserosal fibroid protruding outward toward the abdomen may have zero impact on your ability to conceive, whereas a tiny 1 cm submucosal fibroid bulging into the endometrial cavity can completely sabotage embryo implantation."
                ]
            },
            {
                "type": "heading",
                "title": "The Three Main Types of Uterine Fibroids"
            },
            {
                "type": "cards",
                "cards": [
                    {
                        "icon": "fa-solid fa-triangle-exclamation",
                        "title": "Submucosal Fibroids (Inside Cavity)",
                        "description": "Develop just beneath the inner uterine lining and distort the cavity. <strong>Must always be removed</strong> before IVF because they cut implantation rates in half and increase miscarriage risk."
                    },
                    {
                        "icon": "fa-solid fa-circle-question",
                        "title": "Intramural Fibroids (Inside Muscle)",
                        "description": "Located within the muscular uterine wall. If larger than 4 to 5 cm or if they indent the endometrial lining, laparoscopic myomectomy is strongly recommended."
                    },
                    {
                        "icon": "fa-solid fa-circle-check",
                        "title": "Subserosal Fibroids (Outside Uterus)",
                        "description": "Grow on the outer surface of the uterus. They rarely interfere with embryo implantation or pregnancy and generally do not require surgical intervention."
                    }
                ]
            },
            {
                "type": "callout",
                "icon": "fa-solid fa-wand-magic-sparkles",
                "title": "Hysteroscopic Myomectomy",
                "text": "Submucosal fibroids can be removed in a gentle day-care procedure via hysteroscopy through the natural vaginal canal—no cuts, no stitches, and quick recovery."
            },
            {
                "type": "heading",
                "title": "How Dr. Santosh Gupta Determines the Best Approach"
            },
            {
                "type": "paragraphs",
                "paragraphs": [
                    "At Nova IVF Fertility in Bengaluru, we use high-definition 3D saline-infusion sonography (SIS) and diagnostic hysteroscopy to map the exact relationship between your fibroids and the endometrial lining.",
                    "If surgery is indicated, minimally invasive hysteroscopic or laparoscopic myomectomy preserves your uterine muscle strength for future labor and delivers an optimal uterine cavity for embryo transfer."
                ]
            }
        ]
    }
]


def generate_with_gemini(user_prompt, covered_titles=None):
    """
    Calls Gemini API with fallbacks across models.
    Returns parsed JSON topic object or None.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("[INFO] GEMINI_API_KEY environment variable is empty.")
        return None

    # Models to attempt in priority order
    models_to_try = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]

    context_prompt = ""
    if covered_titles:
        context_prompt = (
            f"\n\nCRITICAL REQUIREMENT: The following topics have ALREADY been published on the site. "
            f"You MUST NOT duplicate any of them:\n- " + "\n- ".join(list(covered_titles)[:20]) + "\n\n"
        )

    full_user_instruction = (
        f"{context_prompt}Generate a new, highly specific, high-intent clinical blog topic addressing: {user_prompt}. "
        f"Ensure it adheres strictly to the JSON schema."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"text": full_user_instruction}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json"
        }
    }
    data = json.dumps(payload).encode("utf-8")

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidate = result["candidates"][0]["content"]["parts"][0]["text"]
                cleaned = candidate.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                topic_obj = json.loads(cleaned.strip())
                if validate_topic_schema(topic_obj):
                    print(f"[AI SUCCESS] Generated topic using model '{model_name}': '{topic_obj['title']}'")
                    return topic_obj
        except urllib.error.HTTPError as e:
            print(f"[WARNING] Model {model_name} returned HTTP {e.code}: {e.reason}")
        except Exception as e:
            print(f"[WARNING] Model {model_name} failed: {e}")

    return None


def validate_topic_schema(topic):
    """Ensures the generated topic object conforms to the publishing engine requirements."""
    required_keys = ["slug", "title", "category", "seo_title", "meta_description", "sections"]
    for k in required_keys:
        if k not in topic or not topic[k]:
            return False

    if not isinstance(topic["sections"], list) or len(topic["sections"]) < 3:
        return False

    # Ensure valid image
    if topic.get("image") not in AVAILABLE_IMAGES:
        topic["image"] = "assets/images/gallery-22.jpg"

    topic["published"] = False
    topic["published_date"] = None
    return True


def add_topic_to_queue(topic_obj):
    """Appends a new topic to automation/topics.json, avoiding duplicate slugs."""
    if not os.path.exists(TOPICS_FILE):
        topics = []
    else:
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            topics = json.load(f)

    existing_slugs = {t["slug"] for t in topics}
    base_slug = topic_obj["slug"]
    slug = base_slug
    counter = 2
    while slug in existing_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1
    topic_obj["slug"] = slug

    topics.append(topic_obj)

    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)

    print(f"[QUEUE UPDATE] Appended '{topic_obj['title']}' (Slug: {slug}) to {TOPICS_FILE}")
    return topic_obj


def auto_replenish_queue(min_buffer=3):
    """
    Maintains a safety buffer of unpublished topics in topics.json.
    If unpublished count < min_buffer:
      1. Tries Gemini AI with dynamically invented clinical prompts.
      2. If AI fails or API key is not valid, automatically falls back to CLINICAL_VAULT_TOPICS.
    Returns the next ready topic or None.
    """
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            topics = json.load(f)
    else:
        topics = []

    unpublished = [t for t in topics if not t.get("published", False)]
    print(f"[QUEUE CHECK] Current status: {len(topics)} total topics, {len(unpublished)} unpublished.")

    if len(unpublished) >= min_buffer:
        print(f"[QUEUE HEALTHY] Buffer satisfied ({len(unpublished)} >= {min_buffer}). No replenishment needed.")
        return unpublished[0]

    needed = min_buffer - len(unpublished)
    print(f"[QUEUE ACTION] Replenishing {needed} topics to maintain safe publication pipeline...")

    existing_slugs = {t["slug"] for t in topics}
    existing_titles = {t["title"].lower() for t in topics}

    added = 0
    # 1. First attempt via Gemini API if key is available
    if os.environ.get("GEMINI_API_KEY", "").strip():
        # High-intent prompts to generate fresh topics
        candidate_seeds = [
            "Endometrial scratch injury vs natural receptivity for repeated IVF failure",
            "Growth hormone (GH) co-treatment in poor ovarian responders with low AMH",
            "Sperm DNA fragmentation remediation: varicocelectomy vs antioxidant therapy vs TESA",
            "Asherman syndrome hysteroscopic adhesiolysis and hormonal recovery protocols",
            "Managing high BMI and metabolic syndrome before IVF stimulation in Bengaluru",
            "Fertility preservation for breast cancer patients: random start stimulation and aromatase inhibitors"
        ]
        for seed in candidate_seeds:
            if added >= needed:
                break
            new_topic = generate_with_gemini(seed, covered_titles=existing_titles)
            if new_topic:
                add_topic_to_queue(new_topic)
                existing_titles.add(new_topic["title"].lower())
                added += 1

    # 2. If AI didn't fulfill the buffer, draw from Clinical Vault
    if added < needed:
        print("[VAULT FALLBACK] Drawing high-value clinical topics from built-in Clinical Vault...")
        for vault_topic in CLINICAL_VAULT_TOPICS:
            if added >= needed:
                break
            if vault_topic["slug"] in existing_slugs or vault_topic["title"].lower() in existing_titles:
                continue
            add_topic_to_queue(dict(vault_topic))
            existing_slugs.add(vault_topic["slug"])
            existing_titles.add(vault_topic["title"].lower())
            added += 1

    # Reload topics
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        refreshed = json.load(f)
    refreshed_unpub = [t for t in refreshed if not t.get("published", False)]
    print(f"[QUEUE STATUS] Replenishment complete. Unpublished topics available: {len(refreshed_unpub)}")

    return refreshed_unpub[0] if refreshed_unpub else None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-replenish":
        auto_replenish_queue()
    elif len(sys.argv) > 1:
        prompt = sys.argv[1]
        print(f"Generating clinical topic for: '{prompt}'...")
        res = generate_with_gemini(prompt)
        if res:
            add_topic_to_queue(res)
        else:
            print("AI generation failed. Run with --auto-replenish to use vault fallback.")
    else:
        print("Usage: python ai_generator.py --auto-replenish OR python ai_generator.py '<prompt>'")
