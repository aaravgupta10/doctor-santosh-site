"""HTML template generator for Dr. Santosh Gupta IVF Blog Automation.
Matches the exact styling, Tailwind color palette, Lenis smooth scrolling,
schema markup, and responsive components of the existing blog posts.
"""

def render_section(section):
    sec_type = section.get("type")
    
    if sec_type == "intro":
        paras = "".join(f"<p>{p}</p>" for p in section.get("paragraphs", []))
        return f'<div class="reveal-element space-y-4">\n{paras}\n</div>'
        
    elif sec_type == "heading":
        title = section.get("title", "")
        return f'<h2 class="font-serif text-2xl md:text-3xl font-bold text-medical-blue mt-12 mb-4 reveal-element">{title}</h2>'
        
    elif sec_type == "paragraphs":
        paras = "".join(f"<p>{p}</p>" for p in section.get("paragraphs", []))
        return f'<div class="reveal-element space-y-4">\n{paras}\n</div>'
        
    elif sec_type == "callout":
        icon = section.get("icon", "fa-solid fa-notes-medical")
        title = section.get("title", "")
        text = section.get("text", "")
        return f'''<div class="bg-soft-teal/30 p-6 md:p-8 rounded-xl border-l-4 border-luxury-gold my-8 reveal-element">
    <p class="font-bold text-medical-blue mb-2 text-lg"><i class="{icon} text-luxury-gold mr-2"></i> {title}</p>
    <p class="text-base m-0 text-gray-700">{text}</p>
</div>'''

    elif sec_type == "cards":
        cards = section.get("cards", [])
        rendered_cards = []
        for c in cards:
            c_icon = c.get("icon", "fa-solid fa-circle-check")
            c_title = c.get("title", "")
            c_desc = c.get("description", "")
            rendered_cards.append(f'''    <div class="p-6 bg-gray-50 rounded-xl border border-gray-200">
        <h3 class="font-serif text-lg font-bold text-medical-blue mb-2 flex items-center">
            <i class="{c_icon} text-luxury-gold mr-2"></i> {c_title}
        </h3>
        <p class="text-sm text-gray-600">{c_desc}</p>
    </div>''')
        cards_html = "\n".join(rendered_cards)
        return f'<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6 reveal-element">\n{cards_html}\n</div>'

    elif sec_type == "list":
        items = section.get("items", [])
        rendered_items = "\n".join(f'    <li>{item}</li>' for item in items)
        return f'<ul class="space-y-3 mt-4 ml-4 list-disc list-inside text-gray-700 reveal-element">\n{rendered_items}\n</ul>'

    return ""


def generate_article_html(topic, date_info):
    """
    Renders the complete HTML document for a blog article.
    date_info should be a dict with:
      - iso: "2026-10-21"
      - long: "October 21, 2026"
      - short: "Oct 21, 2026"
    """
    slug = topic["slug"]
    title = topic["title"]
    category = topic.get("category", "Fertility Insights")
    seo_title = topic.get("seo_title", f"{title} | Dr. Santosh Gupta Bengaluru")
    meta_desc = topic.get("meta_description", "")
    og_desc = topic.get("og_description", meta_desc)
    image = topic.get("image", "assets/images/gallery-18.jpeg")
    image_alt = topic.get("image_alt", f"Dr. Santosh Gupta - {title}")
    cta_headline = topic.get("cta_headline", "Planning Your Fertility Journey in Bengaluru?")
    cta_text = topic.get("cta_text", "Schedule a personalized consultation with Senior IVF Specialist Dr. Santosh Gupta at Nova IVF Fertility in Koramangala or Bannerghatta Road, Bengaluru.")
    
    sections = topic.get("sections", [])
    body_content = "\n\n".join(render_section(s) for s in sections)

    html = f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta name="description"
        content="{meta_desc}">
    <meta property="og:title" content="{seo_title}">
    <meta property="og:description"
        content="{og_desc}">
    <meta property="og:type" content="article">

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{seo_title}</title>
    <link rel="canonical" href="https://www.drsantoshguptaivf.com/{slug}.html" />

    <link rel="icon" href="assets/images/favicon_circle.png" type="image/png">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'medical-blue': '#2C5F78',
                        'soft-teal': '#E0F2F1',
                        'luxury-gold': '#D4AF37',
                        'dark-text': '#333333',
                        'light-text': '#666666',
                    }},
                    fontFamily: {{
                        'serif': ['"Playfair Display"', 'serif'],
                        'sans': ['"Lato"', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>

    <style>
        /* Lenis Smooth Scrolling */
        html.lenis,
        html.lenis body {{
            height: auto;
            width: 100%;
        }}

        .lenis.lenis-smooth {{
            scroll-behavior: auto !important;
        }}

        .lenis.lenis-smooth [data-lenis-prevent] {{
            overscroll-behavior: contain;
        }}

        .lenis.lenis-stopped {{
            overflow: hidden;
        }}

        .lenis.lenis-scrolling iframe {{
            pointer-events: none;
        }}

        /* Reveal Animations */
        .reveal-element {{
            opacity: 0;
            transform: translateY(40px);
            transition: all 1s ease-out;
        }}

        .reveal-element.active {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "author": {{
        "@type": "Person",
        "name": "Dr. Santosh Gupta",
        "url": "https://www.drsantoshguptaivf.com/#physician"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Dr. Santosh Gupta IVF",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://www.drsantoshguptaivf.com/assets/images/favicon_circle.png"
        }}
      }},
      "datePublished": "{date_info['iso']}",
      "description": "{meta_desc}"
    }}
    </script>
</head>

<body class="overflow-x-hidden font-sans text-dark-text bg-soft-teal/20 antialiased flex flex-col min-h-screen">

    <nav class="absolute top-0 left-0 w-full z-50 py-6 bg-white/90 backdrop-blur-md border-b border-gray-100 shadow-sm">
        <div class="max-w-7xl mx-auto px-6 lg:px-8">
            <div class="flex justify-between items-center">

                <a href="index.html" class="flex items-center space-x-2">
                    <i class="fa-solid fa-user-doctor text-luxury-gold text-2xl"></i>
                    <span class="font-serif text-2xl font-bold tracking-wide text-medical-blue">
                        Dr. Santosh <span class="text-luxury-gold">Gupta</span>
                    </span>
                </a>

                <div class="hidden md:flex space-x-4 lg:space-x-5 xl:space-x-7 items-center">
                    <a href="index.html"
                        class="text-medical-blue hover:text-luxury-gold font-medium tracking-wide transition">Home</a>
                    <a href="gallery.html"
                        class="text-gray-600 hover:text-luxury-gold font-medium transition">Gallery</a>
                    <a href="index.html#about"
                        class="text-medical-blue hover:text-luxury-gold font-medium tracking-wide transition">About</a>
                    <a href="index.html#treatments"
                        class="text-medical-blue hover:text-luxury-gold font-medium tracking-wide transition">Treatments</a>
                    <a href="second-opinion-ivf-fertility.html"
                        class="text-medical-blue hover:text-luxury-gold font-medium tracking-wide transition">2nd Opinion</a>
                    <a href="blog.html"
                        class="text-luxury-gold font-bold tracking-wide transition border-b-2 border-luxury-gold pb-1">Blog</a>
                    <a href="index.html#reviews"
                        class="text-medical-blue hover:text-luxury-gold font-medium tracking-wide transition">Reviews</a>
                    <a href="index.html#faq"
                        class="text-medical-blue hover:text-luxury-gold font-medium tracking-wide transition">FAQs</a>
                    <a href="index.html#contact"
                        class="px-6 py-2 bg-medical-blue text-white hover:bg-luxury-gold transition rounded-full font-bold uppercase text-xs tracking-widest shadow-lg">
                        Book Consultation
                    </a>
                </div>

                <div class="md:hidden">
                    <button id="mobile-menu-btn" class="text-medical-blue text-2xl focus:outline-none">
                        <i class="fa-solid fa-bars"></i>
                    </button>
                </div>
            </div>

            <div id="mobile-menu"
                class="hidden md:hidden mt-4 bg-white/95 backdrop-blur-sm rounded-xl shadow-xl p-4 absolute left-4 right-4 border border-gray-100">
                <div class="flex flex-col space-y-4">
                    <a href="index.html" class="text-medical-blue font-medium hover:text-luxury-gold">Home</a>
                    <a href="index.html#about" class="text-medical-blue font-medium hover:text-luxury-gold">About</a>
                    <a href="gallery.html" class="text-medical-blue font-medium hover:text-luxury-gold">Gallery</a>
                    <a href="index.html#treatments"
                        class="text-medical-blue font-medium hover:text-luxury-gold">Treatments</a>
                    <a href="second-opinion-ivf-fertility.html" class="text-medical-blue font-medium hover:text-luxury-gold">2nd Opinion</a>
                    <a href="blog.html" class="text-luxury-gold font-bold">Blog</a>
                    <a href="index.html#reviews" class="text-medical-blue font-medium hover:text-luxury-gold">Reviews</a>
                    <a href="index.html#faq" class="text-medical-blue font-medium hover:text-luxury-gold">FAQs</a>
                    <a href="index.html#contact"
                        class="text-center w-full py-3 bg-medical-blue text-white rounded-lg hover:bg-luxury-gold">Book
                        Consultation</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="flex-grow pt-32 pb-20">
        <div
            class="max-w-4xl mx-auto px-6 lg:px-8 bg-white p-8 md:p-16 rounded-2xl shadow-xl border border-gray-100 mt-8">

            <div class="mb-10 border-b border-gray-100 pb-8 text-center md:text-left reveal-element">
                <a href="blog.html"
                    class="inline-block text-gray-400 hover:text-luxury-gold text-sm font-bold tracking-widest uppercase mb-6 transition">
                    <i class="fa-solid fa-arrow-left mr-2"></i> Back to Blog
                </a>
                <span
                    class="text-luxury-gold font-bold tracking-widest uppercase text-xs md:text-sm mb-4 block">{category}</span>
                <h1 class="font-serif text-3xl md:text-5xl font-bold text-medical-blue leading-tight mb-6">
                    {title}
                </h1>
                <div class="flex items-center justify-center md:justify-start text-gray-500 text-sm">
                    <i class="fa-solid fa-user-doctor text-luxury-gold mr-2"></i>
                    <span class="font-bold mr-6">By Dr. Santosh Gupta</span>
                    <i class="fa-regular fa-calendar mr-2"></i>
                    <span>{date_info['long']}</span>
                </div>
            </div>

            <div class="mb-12 rounded-xl overflow-hidden shadow-md bg-gray-100 h-72 md:h-[450px] reveal-element delay-100">
                <img src="{image}" alt="{image_alt}"
                    class="w-full h-full object-cover hover:scale-105 transition duration-700" style="object-position: center 40%;">
            </div>

            <article class="text-gray-600 leading-relaxed space-y-6 font-sans text-base md:text-lg">
{body_content}
            </article>

            <div
                class="mt-16 bg-medical-blue text-white p-8 md:p-12 rounded-2xl text-center shadow-lg relative overflow-hidden reveal-element">
                <div class="absolute top-0 right-0 -mr-10 -mt-10 w-40 h-40 bg-white/10 rounded-full blur-3xl"></div>
                <div class="relative z-10">
                    <h3 class="font-serif text-2xl md:text-3xl font-bold mb-4">{cta_headline}</h3>
                    <p class="text-blue-100 mb-8 text-base max-w-2xl mx-auto">{cta_text}</p>
                    <a href="index.html#contact"
                        class="inline-block px-8 py-4 bg-white text-medical-blue font-bold rounded-lg hover:bg-luxury-gold hover:text-white transition uppercase tracking-widest text-sm shadow-xl">
                        Schedule Your Consultation
                    </a>
                </div>
            </div>

        </div>
    </main>

    <footer class="bg-gray-900 text-white py-12 border-t border-gray-800">
        <div class="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">

            <div class="text-center md:text-left">
                <a href="index.html" class="inline-block">
                    <span class="font-serif text-2xl font-bold tracking-wide">
                        Dr. Santosh <span class="text-luxury-gold">Gupta</span>
                    </span>
                </a>
                <p class="text-gray-500 text-sm mt-2">© 2026 Dr. Santosh Gupta Fertility.</p>

                <p class="text-gray-400 text-xs mt-1 max-w-xs mx-auto md:mx-0 leading-relaxed">
                    Senior Consultant at Nova IVF Fertility<br>
                    Serving <strong>Koramangala</strong> & <strong>Bannerghatta Road</strong>, Bengaluru.
                </p>
            </div>

            <div class="flex flex-wrap justify-center gap-x-6 gap-y-3 text-sm text-gray-400 font-medium">
                <a href="index.html" class="hover:text-luxury-gold transition">Home</a>
                <a href="index.html#about" class="hover:text-luxury-gold transition">About</a>
                <a href="gallery.html" class="hover:text-luxury-gold transition">Gallery</a>
                <a href="index.html#treatments" class="hover:text-luxury-gold transition">Treatments</a>
                <a href="blog.html" class="hover:text-luxury-gold transition">Blog</a>
                <a href="index.html#reviews" class="hover:text-luxury-gold transition">Reviews</a>
                <a href="index.html#faq" class="hover:text-luxury-gold transition">FAQs</a>
            </div>

            <div class="flex space-x-4">
                <a href="https://www.facebook.com/share/1DD9aXkwjm/?mibextid=wwXIfr" target="_blank"
                    class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center text-gray-400 hover:bg-luxury-gold hover:text-white transition duration-300">
                    <i class="fa-brands fa-facebook-f"></i>
                </a>
                <a href="https://www.instagram.com/drsantosh_gupta_ivf_specialist?igsh=dGR0MWRxYnd6cjc4&utm_source=qr"
                    target="_blank"
                    class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center text-gray-400 hover:bg-luxury-gold hover:text-white transition duration-300">
                    <i class="fa-brands fa-instagram"></i>
                </a>
                <a href="https://www.linkedin.com/in/santosh-gupta-ab594523b/?originalSubdomain=in" target="_blank"
                    class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center text-gray-400 hover:bg-luxury-gold hover:text-white transition duration-300">
                    <i class="fa-brands fa-linkedin-in"></i>
                </a>
            </div>
        </div>
    </footer>

    <a href="https://wa.me/919845446536?text=Hello%20Dr.%20Santosh,%20I%20visited%20your%20website%20and%20have%20a%20query."
        target="_blank"
        class="fixed bottom-6 right-6 bg-green-500 text-white w-14 h-14 rounded-full flex items-center justify-center shadow-lg hover:bg-green-600 transition-all duration-300 z-50 animate-bounce">
        <i class="fa-brands fa-whatsapp text-3xl"></i>
    </a>

    <script>
        // Mobile Menu Toggle
        const btn = document.getElementById('mobile-menu-btn');
        const menu = document.getElementById('mobile-menu');

        btn.addEventListener('click', () => {{
            menu.classList.toggle('hidden');
        }});

        // Intersection Observer for scroll reveal
        document.addEventListener('DOMContentLoaded', () => {{
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('active');
                        observer.unobserve(entry.target);
                    }}
                }});
            }}, {{ threshold: 0.1 }});

            const elementsToReveal = document.querySelectorAll('.reveal-element');
            elementsToReveal.forEach(el => observer.observe(el));
        }});
    </script>

    <script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
    <script>
        const lenis = new Lenis({{
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            direction: 'vertical',
            gestureDirection: 'vertical',
            smooth: true,
            mouseMultiplier: 1,
            smoothTouch: false,
            touchMultiplier: 2,
            infinite: false,
        }});

        function raf(time) {{
            lenis.raf(time);
            requestAnimationFrame(raf);
        }}

        requestAnimationFrame(raf);
    </script>
</body>

</html>
'''
    return html


def generate_blog_card_html(topic, date_info):
    """
    Renders the blog preview card for insertion into blog.html.
    """
    slug = topic["slug"]
    title = topic["title"]
    category = topic.get("category", "Fertility Insights")
    excerpt = topic.get("excerpt", "")
    image = topic.get("image", "assets/images/gallery-18.jpeg")
    image_alt = topic.get("image_alt", title)
    date_short = date_info["short"]

    card_html = f'''                <div
                    class="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition duration-300 transform hover:-translate-y-1 group border border-gray-100 overflow-hidden flex flex-col h-full reveal-element">
                    <div class="h-56 overflow-hidden relative bg-gray-100 flex items-center justify-center">
                        <img src="{image}" alt="{image_alt}"
                            class="w-full h-full object-cover group-hover:scale-105 transition duration-700" style="object-position: center 40%;">
                    </div>
                    <div class="p-8 flex flex-col flex-grow">
                        <span class="text-luxury-gold text-xs font-bold uppercase tracking-widest mb-3 block">{category}</span>
                        <h2
                            class="font-serif text-2xl font-bold text-medical-blue mb-4 group-hover:text-luxury-gold transition leading-snug">
                            {title}
                        </h2>
                        <p class="text-gray-500 text-sm leading-relaxed mb-6 flex-grow">
                            {excerpt}
                        </p>
                        <div class="flex items-center justify-between border-t border-gray-100 pt-4 mt-auto">
                            <span class="text-xs text-gray-400 font-medium"><i class="fa-regular fa-calendar mr-1"></i>
                                {date_short}</span>
                            <a href="{slug}.html"
                                class="text-medical-blue font-bold text-sm uppercase tracking-wide group-hover:underline flex items-center">
                                Read More <i class="fa-solid fa-arrow-right text-xs ml-2"></i>
                            </a>
                        </div>
                    </div>
                </div>'''
    return card_html


def generate_sitemap_url_entry(topic, date_info):
    """
    Generates XML <url> block for sitemap.xml.
    """
    slug = topic["slug"]
    image = topic.get("image", "assets/images/gallery-18.jpeg")
    image_title = topic.get("image_title", topic["title"])
    date_iso = date_info["iso"]

    xml_entry = f'''   <url>
      <loc>https://www.drsantoshguptaivf.com/{slug}.html</loc>
      <lastmod>{date_iso}</lastmod>
      <priority>0.80</priority>
      <image:image>
         <image:loc>https://www.drsantoshguptaivf.com/{image}</image:loc>
         <image:title>{image_title}</image:title>
      </image:image>
   </url>'''
    return xml_entry
