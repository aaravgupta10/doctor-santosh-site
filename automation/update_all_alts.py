"""Script to update all image alt tags across Dr. Santosh Gupta IVF website
with high-value SEO and GEO-targeted keywords (Koramangala, Bannerghatta Road, Bengaluru, Nova IVF Fertility).
"""

import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Exact replacements per file
REPLACEMENTS = {
    "gallery.html": [
        ('alt="Most experienced IVF specialist in Koramangala, Bangalore receiving award"',
         'alt="Dr. Santosh Gupta, Senior IVF Specialist in Koramangala Bengaluru, receiving award for excellence in reproductive medicine"'),
        ('alt="IUI, ICSI & Inferitlity specilist Santosh Gupta delivering talk at ISAR conference, Bengaluru"',
         'alt="Dr. Santosh Gupta, leading IUI, ICSI and Infertility Specialist, delivering keynote at ISAR conference in Bengaluru"'),
        ('alt="Recurrent pregnancy loss and male infertility specialist Dr Santosh Gupta awarded for her efforts at ISAR 2025"',
         'alt="Recurrent pregnancy loss and IVF specialist Dr. Santosh Gupta honored for clinical excellence at ISAR conference in Bengaluru"'),
        ('alt="Best IVF specialist - Santosh Gupta collecting award at path to parenthood - an initiative by newsprime"',
         'alt="Top IVF Specialist Dr. Santosh Gupta receiving Path to Parenthood award for excellence in Bengaluru fertility care"'),
        ('alt="ICSI and Adavanced Embryology expert Dr Santosh Gupta of Nova IVF Koramangala"',
         'alt="ICSI and Advanced Embryology specialist Dr. Santosh Gupta at Nova IVF Fertility, Koramangala Bengaluru"'),
        ('alt="Senior Dr Santosh Gupta delivering talk at Fertivision 2024 by Indian Fertility Society"',
         'alt="Senior IVF Specialist Dr. Santosh Gupta presenting clinical insights at Fertivision, Indian Fertility Society"'),
        ('alt="The most experienced IVF specialist & Gynecologist - Dr. Santosh Gupta recieving prize for hardwork"',
         'alt="Dr. Santosh Gupta, leading IVF Specialist and Gynecologist in Bengaluru, receiving prestigious recognition for excellence in reproductive care"'),
        ('alt="Dr Santosh Gupta - Best Gynecologist in Koramangala, Bengaluru giving speech as cheif guest"',
         'alt="Dr. Santosh Gupta, Best Gynecologist and IVF Consultant in Koramangala Bengaluru, speaking as Chief Guest at medical seminar"'),
        ('alt="Dr. Santosh Gupta partnering with BSOG to teach the top IVF specialists of the future"',
         'alt="Senior IVF Consultant Dr. Santosh Gupta mentoring clinicians with BSOG on advanced reproductive technologies in Bengaluru"'),
        ('alt="Dr. Santosh Gupta - Best IVF specialist in Bannerghatta, Bengaluru"',
         'alt="Dr. Santosh Gupta, Best IVF Specialist at Nova IVF Fertility Bannerghatta Road, Bengaluru"'),
        ('alt="Dr Santosh Gupta - Best Infertility specialist awarded at KISAR 2025"',
         'alt="Dr. Santosh Gupta awarded Best Infertility and IVF Specialist in Bengaluru at KISAR conference"'),
        ('alt="Dr. Santosh Gupta - Top Fertility Specialist, discussing advanced IVF treatments on live broadcast by Newsprime"',
         'alt="Senior IVF Specialist Dr. Santosh Gupta discussing high-success fertility treatments on live broadcast in Bengaluru"'),
        ('alt="Expert gynecologist and fertility doctor Dr. Santosh Gupta sharing insights on recurrent pregnancy loss"',
         'alt="Dr. Santosh Gupta, Senior IVF Specialist in Bengaluru, sharing clinical protocols for recurrent pregnancy loss and thin endometrium"'),
        ('alt="Live Q&A session with leading IVF specialist Dr. Santosh Gupta focusing on male and female infertility solutions"',
         'alt="Live medical session with Dr. Santosh Gupta discussing embryo pooling, male infertility, and personalized IVF in Bengaluru"'),
        ('alt="Dr. Santosh Gupta educating patients on PCOS, IUI, and ICSI treatments during a live medical broadcast"',
         'alt="Dr. Santosh Gupta educating patients on PCOS fertility protocols, IUI, and ICSI at Nova IVF Fertility Bengaluru"'),
        ('alt="Senior IVF specialist Dr. Santosh Gupta at Nova IVF Fertility center"',
         'alt="Senior IVF Specialist Dr. Santosh Gupta counseling patients on low AMH and ovarian reserve at Nova IVF Fertility Bengaluru"'),
        ('alt="Dr. Santosh Gupta presenting advanced reproductive technology solutions"',
         'alt="Dr. Santosh Gupta presenting PGT-A genetic screening and advanced IVF solutions at a medical symposium in Bengaluru"'),
        ('alt="Dr. Santosh Gupta - Leading Infertility and IVF specialist in Bengaluru"',
         'alt="Dr. Santosh Gupta, leading Senior IVF Specialist serving Koramangala and Bannerghatta Road, Bengaluru"'),
        ('alt="Full view"',
         'alt="Dr. Santosh Gupta fertility clinical gallery high resolution view in Bengaluru"')
    ],
    "index.html": [
        ('alt="Dr. Santosh Gupta, leading IVF specialist in Koramangala and Bannerghatta, Bengaluru"',
         'alt="Dr. Santosh Gupta, leading Senior IVF Specialist at Nova IVF Fertility in Koramangala and Bannerghatta Road, Bengaluru"'),
        ('alt="State-of-the-art fertility clinic and IVF center led by Dr. Santosh Gupta"',
         'alt="State-of-the-art fertility center and advanced IVF embryology lab led by Dr. Santosh Gupta in Bengaluru"'),
        ('alt="Dr. Santosh Gupta, the best IVF doctor in Bengaluru, receiving an award for excellence in fertility treatments"',
         'alt="Dr. Santosh Gupta, Senior IVF Specialist in Bengaluru, honored with award for excellence in reproductive medicine and patient care"'),
        ('alt="Leading fertility specialist Dr. Santosh Gupta presenting insights on Recurrent Implantation Failure and IVF success at medical conference"',
         'alt="Leading fertility specialist Dr. Santosh Gupta presenting insights on Recurrent Implantation Failure (RIF) and blastocyst transfer in Bengaluru"'),
        ('alt="Dr. Santosh Gupta explaining PCOS and its impact on female fertility at Fertivision event"',
         'alt="Senior Gynecologist Dr. Santosh Gupta explaining severe PCOS management and IVF protocols at Fertivision in Bengaluru"'),
        ('alt="Dr. Santosh Gupta, highly experienced IVF specialist, ICSI expert, and senior consultant in Bengaluru"',
         'alt="Dr. Santosh Gupta, Senior IVF Specialist with 25+ years experience at Nova IVF Fertility, Koramangala and Bannerghatta Road, Bengaluru"')
    ],
    "blog.html": [
        ('alt="Dr. Santosh Gupta presenting genetic testing and advanced IVF options at a fertility conference"',
         'alt="Dr. Santosh Gupta presenting PGT-A genetic screening and advanced blastocyst testing protocols in Bengaluru"'),
        ('alt="Dr. Santosh Gupta, leading fertility specialist in Bengaluru"',
         'alt="Dr. Santosh Gupta, leading Senior IVF Specialist serving Koramangala and Bannerghatta Road, Bengaluru"'),
        ('alt="Dr. Santosh Gupta discussing Recurrent Implantation Failure and IVF success"',
         'alt="Leading fertility specialist Dr. Santosh Gupta presenting insights on Recurrent Implantation Failure (RIF) and IVF success in Bengaluru"'),
        ('alt="Insights on PCOS and female fertility by Dr. Santosh Gupta"',
         'alt="Dr. Santosh Gupta explaining severe PCOS fertility protocols and tailored ovarian stimulation in Bengaluru"'),
        ('alt="Dr. Santosh Gupta discussing medical management and ART solutions for male infertility"',
         'alt="Senior IVF Specialist Dr. Santosh Gupta discussing ICSI and advanced male factor infertility solutions in Bengaluru"')
    ],
    "iui-treatment.html": [
        ('alt="Top IUI treatment specialist Dr. Santosh Gupta partnering with medical professionals to advance fertility care"',
         'alt="Top IUI treatment specialist Dr. Santosh Gupta partnering with medical professionals to advance fertility care in Bengaluru"'),
        ('alt="State-of-the-art intrauterine insemination (IUI) clinic and personalized care by Dr. Santosh Gupta"',
         'alt="Personalized Intrauterine Insemination (IUI) treatment by Senior Fertility Consultant Dr. Santosh Gupta in Koramangala, Bengaluru"')
    ],
    "laproscopy-hysteroscopy.html": [
        ('alt="Advanced Laparoscopy and Hysteroscopy minimally invasive surgery specialist Dr. Santosh Gupta"',
         'alt="Advanced Laparoscopy and Hysteroscopy minimally invasive fertility surgeon Dr. Santosh Gupta in Bengaluru"'),
        ('alt="Dr. Santosh Gupta consulting patients at her state-of-the-art fertility and IVF clinic"',
         'alt="Senior Gynecologist Dr. Santosh Gupta consulting patients on laparoscopic and hysteroscopic fertility correction in Bengaluru"')
    ],
    "recurrent-implantation-failure-ivf.html": [
        ('alt="Leading fertility specialist Dr. Santosh Gupta presenting insights on Recurrent Implantation Failure and IVF success"',
         'alt="Senior IVF Specialist Dr. Santosh Gupta presenting clinical protocols for Recurrent Implantation Failure (RIF) in Bengaluru"')
    ],
    "understanding-severe-pcos-fertility.html": [
        ('alt="Dr. Santosh Gupta explaining PCOS and its impact on female fertility at a medical conference"',
         'alt="Senior Fertility Consultant Dr. Santosh Gupta explaining severe PCOS treatment protocols and OHSS prevention in Bengaluru"')
    ],
    "male-infertility-icsi-treatment.html": [
        ('alt="Top ICSI treatment specialist Dr. Santosh Gupta discussing advanced male infertility solutions"',
         'alt="Top ICSI and male infertility specialist Dr. Santosh Gupta explaining advanced embryology protocols at Nova IVF Fertility Bengaluru"')
    ]
}


def run():
    total_updated = 0
    for filename, pairs in REPLACEMENTS.items():
        file_path = os.path.join(ROOT_DIR, filename)
        if not os.path.exists(file_path):
            print(f"Skipping {filename} (not found)")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        file_updated = 0
        for old, new in pairs:
            if old in content:
                content = content.replace(old, new)
                file_updated += 1
            else:
                print(f"  [Notice] Target text not found in {filename}: {old[:50]}...")

        if file_updated > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[OK] Updated {file_updated} alt tags in {filename}")
            total_updated += file_updated

    print(f"\nTotal alt tags updated: {total_updated}")


if __name__ == "__main__":
    run()
