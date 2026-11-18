# Dr. Santosh Gupta IVF Website - Automated Blog Publishing System

## Overview
This automation is engineered to automatically generate and publish patient-centric, SEO- and GEO-optimized clinical blog posts to **www.drsantoshguptaivf.com** every **Monday, Wednesday, and Friday** at **08:30 AM IST** (03:00 UTC).

Every publication performs the following end-to-end actions:
1. **Picks the next clinical topic** from the curated backlog in [`automation/topics.json`](automation/topics.json).
2. **Generates a standalone blog page (`[slug].html`)** with exact typography, color scheme (`medical-blue`, `soft-teal`, `luxury-gold`), animations, Lenis smooth scrolling, and Google `Article` Schema.org JSON-LD markup.
3. **Updates [`blog.html`](blog.html)** by inserting a new responsive card at the top of the blog grid.
4. **Updates [`sitemap.xml`](sitemap.xml)** with the new `<url>` entry, image location, image title, and updates `<lastmod>` on the homepage and blog listing.
5. **Commits and pushes changes directly to GitHub**, triggering GitHub Pages to deploy the updated site automatically.

---

## 1. Automated Schedule (GitHub Actions)
The workflow is located at [`.github/workflows/publish-blog.yml`](.github/workflows/publish-blog.yml).

- **Schedule:** `0 3 * * 1,3,5` (Cron UTC)
  - Every **Monday**, **Wednesday**, and **Friday** at **08:30 AM IST** (03:00 UTC).
- **Automation Engine:** Runs [`automation/publish.py`](automation/publish.py) in Python 3.11.
- **Git Push:** Automatically commits with message `Auto-publish scheduled blog [skip ci]` and pushes to `origin/main`.

### Manual Trigger via GitHub:
You can trigger publication anytime directly from GitHub:
1. Go to the **Actions** tab in the repository: `https://github.com/aaravgupta10/doctor-santosh-site/actions`.
2. Select **Auto-Publish Blog (Mon / Wed / Fri)** from the left sidebar.
3. Click **Run workflow**, optionally specify a topic slug or check "Force publish", and click **Run workflow**.

---

## 2. Running Locally via Terminal
You can run the publishing engine manually on your computer anytime:

```bash
# Preview what will be published without writing any files
python automation/publish.py --dry-run --force

# Publish the next scheduled topic immediately
python automation/publish.py --force

# Publish a specific topic by slug
python automation/publish.py --slug high-sperm-dna-fragmentation-icsi-bengaluru --force

# Publish with a specific publication date
python automation/publish.py --force --date 2026-10-23
```

---

## 3. Autonomous Topic Pipeline & Replenishment
The system maintains an autonomous, self-replenishing pipeline in [`automation/topics.json`](automation/topics.json):

1. **Queue Buffer Monitoring:** Every time `publish.py` executes, it verifies that at least **3 to 5 unpublished topics** are ready in the backlog.
2. **Dual-Engine Auto-Replenishment:**
   - **AI Generation (Gemini 2.0 / 1.5 Flash):** If `GEMINI_API_KEY` is provided, it dynamically crafts new clinical topics avoiding anything already published.
   - **Clinical Vault Fallback:** If the API key is unavailable or fails, it automatically draws from a built-in clinical vault covering advanced reproductive topics (uNK cells, Thrombophilia, Fibroids, DuoStim, Uterine PRP, etc.), ensuring **zero publication downtime**.

### Current Publication Pipeline (21 Topics Total):
| Status | Topic Title | Target Audience / Issue |
| :--- | :--- | :--- |
| **Published** | *Thin Endometrial Lining in IVF: Causes, Treatments & Implantation Solutions* | Implantation / Uterine Lining (<7mm) |
| **Published** | *High Sperm DNA Fragmentation (DFI): Overcoming Hidden Male Infertility with ICSI* | Male Factor Infertility / Paternal DNA |
| **Published** | *Natural Cycle vs. Medicated FET: Which Yields Higher Success in IVF?* | Frozen Embryo Transfer / Corpus Luteum |
| **Published** | *Recurrent Pregnancy Loss: Root Causes, Diagnostic Workup & Proven Solutions* | Miscarriage / Thrombophilia / PGT-A |
| **Published** | *Silent Endometriosis: The Unseen Cause of Unexplained Infertility* | Unexplained Infertility / Laparoscopy |
| **Published** | *Day 3 vs. Day 5 Embryo Transfer: Why Blastocyst Culture Maximizes IVF Success* | Advanced Embryology / Lab Quality |
| **Published** | *DHEA & CoQ10 Before IVF: Can Supplements Improve Egg Quality After 35?* | Women 35+ / Mitochondrial Priming |
| **Published** | *Preventing OHSS in IVF: Modern Protocols for Safe Treatment with PCOS* | PCOS / High Reserve / Agonist Triggers |
| **Published** | *Unexplained Infertility: What to Do When All Your Fertility Tests Are Normal* | Frustrated couples with normal tests |
| **Published** | *The Two-Week Wait (2WW) After Embryo Transfer: Symptoms, Myths & Precautions* | Post-transfer anxiety / Progesterone signs |
| **Published** | *Donor Egg IVF for Women 40+: Emotional Considerations & High Success Rates* | Advanced Age 40+ / POI / Low AMH |
| **Published** | *DuoStim Protocol in IVF: How Double Ovarian Stimulation Maximizes Embryos for Low AMH* | Low AMH / Poor Responders / Double Stimulation |
| **Queued** | *Uterine PRP Therapy for IVF: Restoring Thin Endometrium & Overcoming Implantation Failure* | Refractory Thin Lining (<7mm) / RIF |
| **Queued** | *ERA, EMMA & ALICE Tests in IVF: Pinpointing Your Implantation Window & Uterine Microbiome* | Displaced Window of Implantation / Chronic Endometritis |
| **Queued** | *ICSI, IMSI, or PICSI? Advanced Sperm Selection for High DNA Fragmentation & Male Infertility* | Severe Teratozoospermia / High DFI |
| **Queued** | *Adenomyosis and IVF: Why an Enlarged Uterus Affects Implantation and How to Treat It* | Bulky Uterus / GnRH Down-regulation |
| **Queued** | *PGT-A vs. PGT-M: When Should You Genetically Test Embryos Before IVF Transfer?* | Genetic Screening / Single Gene Defects / Age 35+ |
| **Queued** | *Mini-IVF vs. Conventional IVF: Which Is Best for Diminished Ovarian Reserve After 38?* | Mild Stimulation / Poor Ovarian Responders |
| **Queued** | *Thyroid and Fertility: How Subclinical Hypothyroidism and Anti-TPO Impact IVF Success* | Endocrine Optimization / Anti-TPO Miscarriage |
| **Queued** | *Diagnostic Hysteroscopy Before IVF: Why Inspecting the Uterine Cavity Increases Live Births* | Uterine Polyps / Cavity Evaluation / Endometrial Injury |
| **Queued** | *Social Egg Freezing in Bengaluru: Age, Egg Yield, Costs & What Career Professionals Must Know* | Career Women / Oocyte Vitrification / Preservation |

---

## 4. How to Add New Topics to the Queue
To add a new article to the schedule, open [`automation/topics.json`](automation/topics.json) and append a new JSON object:

```json
{
  "slug": "your-article-slug-bengaluru",
  "title": "Your Clinical Article Title",
  "category": "Age & Fertility Solutions",
  "seo_title": "Your SEO Title | Dr. Santosh Gupta Bengaluru",
  "meta_description": "150-160 characters summary with keywords and doctor mention.",
  "og_description": "Compelling social description.",
  "image": "assets/images/gallery-18.jpeg",
  "image_alt": "Detailed image alt text describing Dr. Santosh Gupta in Bengaluru.",
  "image_title": "Sitemap image title",
  "excerpt": "Brief 2-sentence preview shown on blog.html.",
  "cta_headline": "Have Questions About Your Fertility Journey?",
  "cta_text": "Schedule a consultation with Dr. Santosh Gupta at Nova IVF Fertility in Koramangala or Bannerghatta Road, Bengaluru.",
  "published": false,
  "published_date": null,
  "sections": [
    {
      "type": "intro",
      "paragraphs": ["First intro paragraph...", "Second intro paragraph..."]
    },
    {
      "type": "heading",
      "title": "Clinical Section Title"
    },
    {
      "type": "paragraphs",
      "paragraphs": ["Clinical discussion paragraph..."]
    },
    {
      "type": "callout",
      "icon": "fa-solid fa-notes-medical",
      "title": "Doctor's Advice",
      "text": "Important takeaway for patients."
    },
    {
      "type": "cards",
      "cards": [
        {
          "icon": "fa-solid fa-circle-check",
          "title": "Card Title 1",
          "description": "Card description..."
        }
      ]
    },
    {
      "type": "list",
      "items": [
        "<strong>Step 1:</strong> Description...",
        "<strong>Step 2:</strong> Description..."
      ]
    }
  ]
}
```

---

## 5. Optional: AI Topic Generation with Gemini
If you want to dynamically generate complete clinical topics with Google Gemini:

1. Obtain a Google Gemini API Key from Google AI Studio.
2. Add it to your GitHub Repository Secrets as `GEMINI_API_KEY` (or set `export GEMINI_API_KEY="your-key"` in your local terminal).
3. Run:
```bash
python automation/ai_generator.py "How we manage recurrent implantation failure with uterine PRP in Bengaluru"
```
The script will format the prompt, generate a clinical article conforming to Dr. Santosh Gupta's credentials and locations, and automatically append it to [`automation/topics.json`](automation/topics.json).

---

## 6. SEO & GEO Optimization Checklist Preserved in Every Post
- **Local GEO Citations:** Nova IVF Fertility, Koramangala (Sony World Signal), Bannerghatta Road (Hulimavu Gate / Arekere), Bengaluru.
- **Author Entity:** Dr. Santosh Gupta (Senior IVF Specialist & Gynecologist, 25+ years experience, MS OBG, Fellowship in Reproductive Medicine RGUHS).
- **Search Intent:** Tailored to complex cases that patients in Bengaluru face (e.g. 35+ advanced maternal age, low AMH, high DFI, silent endometriosis, thin endometrium, blastocyst culture).
- **Google Rich Results:** Schema.org `Article` JSON-LD markup with doctor name, organization logo, publish date, and canonical URL.
- **Sitemap & Search Discovery:** `<image:image>` tags with localized keywords to index doctor photographs on Google Images.
