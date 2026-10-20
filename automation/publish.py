#!/usr/bin/env python3
"""
Blog Publishing Engine for Dr. Santosh Gupta IVF Website.
Automatically publishes SEO & GEO-optimized blog posts on Mondays, Wednesdays, and Fridays.

Actions performed:
1. Picks the next scheduled clinical topic from topics.json.
2. Generates the full HTML article matching site typography, schema, and layout.
3. Updates blog.html by injecting the new preview card at the top of the grid.
4. Updates sitemap.xml with the new URL, image metadata, and refreshed lastmod dates.
5. Updates topics.json marking the topic as published.
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timezone

# Add automation directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import template

TOPICS_FILE = os.path.join(SCRIPT_DIR, "topics.json")
BLOG_HTML_FILE = os.path.join(ROOT_DIR, "blog.html")
SITEMAP_FILE = os.path.join(ROOT_DIR, "sitemap.xml")


def get_date_info(date_str=None):
    """Parses date string or uses current local date."""
    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        dt = datetime.now()
    
    return {
        "dt": dt,
        "iso": dt.strftime("%Y-%m-%d"),
        "long": dt.strftime("%B %d, %Y"),
        "short": dt.strftime("%b %d, %Y"),
        "weekday": dt.weekday() # Monday=0, Wednesday=2, Friday=4
    }


def load_topics():
    if not os.path.exists(TOPICS_FILE):
        raise FileNotFoundError(f"Topics file not found at {TOPICS_FILE}")
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_topics(topics):
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)


def find_next_topic(topics, specific_slug=None):
    if specific_slug:
        for t in topics:
            if t.get("slug") == specific_slug:
                return t
        raise ValueError(f"Topic with slug '{specific_slug}' not found in topics.json")
    
    for t in topics:
        if not t.get("published", False):
            return t

    # If all existing topics are published, try autonomous AI replenishment
    try:
        import ai_generator
        print("[INFO] All pre-queued topics published! Attempting autonomous replenishment...")
        new_topic = ai_generator.auto_replenish_queue()
        if new_topic:
            return new_topic
    except Exception as e:
        print(f"[WARNING] Could not auto-replenish topics: {e}")
            
    return None



def update_blog_html(topic, date_info, dry_run=False):
    """Inserts the new card at the top of the blog-grid in blog.html."""
    with open(BLOG_HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already present
    slug_ref = f'{topic["slug"]}.html'
    if slug_ref in content:
        print(f"  [INFO] Article {slug_ref} is already linked in blog.html. Skipping card injection.")
        return False

    grid_marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 blog-grid">'
    if grid_marker not in content:
        raise ValueError(f"Could not find blog grid marker in {BLOG_HTML_FILE}")

    card_html = template.generate_blog_card_html(topic, date_info)
    replacement = f'{grid_marker}\n{card_html}\n'
    new_content = content.replace(grid_marker, replacement, 1)

    if not dry_run:
        with open(BLOG_HTML_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  [OK] Injected new card into {BLOG_HTML_FILE}")
    else:
        print(f"  [DRY-RUN] Would inject new card into {BLOG_HTML_FILE}")

    return True


def update_sitemap(topic, date_info, dry_run=False):
    """Adds new URL entry to sitemap.xml and updates lastmod for home and blog."""
    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    slug_ref = f'https://www.drsantoshguptaivf.com/{topic["slug"]}.html'
    if slug_ref in content:
        print(f"  [INFO] URL {slug_ref} is already in sitemap.xml. Skipping sitemap insertion.")
        return False

    # Generate XML entry
    xml_entry = template.generate_sitemap_url_entry(topic, date_info)

    # Insert before </urlset>
    if "</urlset>" not in content:
        raise ValueError("Could not find </urlset> tag in sitemap.xml")

    # Also update lastmod for root and blog.html
    today_iso = date_info["iso"]
    
    # Update root lastmod
    content = re.sub(
        r'(<loc>https://www.drsantoshguptaivf.com/</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        rf'\g<1>{today_iso}\g<2>',
        content
    )
    # Update blog.html lastmod
    content = re.sub(
        r'(<loc>https://www.drsantoshguptaivf.com/blog\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)',
        rf'\g<1>{today_iso}\g<2>',
        content
    )

    replacement = f'{xml_entry}\n\n</urlset>'
    new_content = content.replace("</urlset>", replacement, 1)

    if not dry_run:
        with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  [OK] Added URL and refreshed dates in {SITEMAP_FILE}")
    else:
        print(f"  [DRY-RUN] Would add URL and refresh dates in {SITEMAP_FILE}")

    return True


def publish(date_str=None, specific_slug=None, force=False, dry_run=False):
    date_info = get_date_info(date_str)
    weekday = date_info["weekday"]
    weekday_name = date_info["dt"].strftime("%A")

    print(f"=== Dr. Santosh Gupta IVF Blog Automation ===")
    print(f"Date: {date_info['long']} ({weekday_name})")

    # Verify if today is Monday (0), Wednesday (2), or Friday (4)
    is_scheduled_day = weekday in (0, 2, 4)
    if not is_scheduled_day and not force and not specific_slug:
        print(f"[NOTE] Today is {weekday_name}. Publishing is scheduled for Mondays, Wednesdays, and Fridays.")
        print(f"Use --force to publish today, or run with --slug <slug>.")
        return False

    topics = load_topics()
    topic = find_next_topic(topics, specific_slug)

    if not topic:
        print("[WARNING] No unpublished topics remaining in topics.json!")
        print("Please add new topics or check automation/topics.json.")
        return False

    slug = topic["slug"]
    print(f"\nPublishing topic: '{topic['title']}'")
    print(f"Slug: {slug}.html")
    print(f"Category: {topic.get('category', 'Fertility Insights')}")

    # 1. Generate Article HTML
    article_html = template.generate_article_html(topic, date_info)
    target_article_path = os.path.join(ROOT_DIR, f"{slug}.html")

    if not dry_run:
        with open(target_article_path, "w", encoding="utf-8") as f:
            f.write(article_html)
        print(f"  [OK] Generated blog page: {target_article_path}")
    else:
        print(f"  [DRY-RUN] Would generate blog page: {target_article_path}")

    # 2. Update blog.html
    update_blog_html(topic, date_info, dry_run=dry_run)

    # 3. Update sitemap.xml
    update_sitemap(topic, date_info, dry_run=dry_run)

    # 4. Mark topic as published in topics.json
    if not dry_run:
        topic["published"] = True
        topic["published_date"] = date_info["iso"]
        save_topics(topics)
        print(f"  [OK] Marked topic as published in {TOPICS_FILE}")
    else:
        print(f"  [DRY-RUN] Would mark topic as published in {TOPICS_FILE}")

    print(f"\n[SUCCESS] Successfully published '{topic['title']}'!")
    print(f"Canonical URL: https://www.drsantoshguptaivf.com/{slug}.html\n")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish scheduled blog posts for Dr. Santosh Gupta IVF website")
    parser.add_argument("--date", help="Publication date in YYYY-MM-DD format (default: today)")
    parser.add_argument("--slug", help="Publish a specific topic slug from topics.json")
    parser.add_argument("--force", action="store_true", help="Force publication regardless of weekday schedule")
    parser.add_argument("--dry-run", action="store_true", help="Simulate publishing without writing files")

    args = parser.parse_args()
    success = publish(
        date_str=args.date,
        specific_slug=args.slug,
        force=args.force,
        dry_run=args.dry_run
    )
    sys.exit(0 if success else 1)
