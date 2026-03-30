import os

replacements = {
    'icsi-treatment.html': [
        ('alt="ICSI Expert Dr Santosh Gupta"', 'alt="Renowned ICSI expert Dr. Santosh Gupta specializing in advanced embryology and male infertility at Nova IVF"'),
        ('alt="Dr Santosh Gupta Awards"', 'alt="Dr. Santosh Gupta recognized with top honors for excellence in ICSI and severe infertility cases"')
    ],
    'recurrent-pregnancy-loss.html': [
        ('alt="Recurrent Pregnancy Loss Specialist Award"', 'alt="Dr. Santosh Gupta receiving prestigious award for excellence in Recurrent Pregnancy Loss management at ISAR 2025"'),
        ('alt="Dr Santosh Gupta Recognition"', 'alt="Leading specialist Dr. Santosh Gupta recognized for customized protocols treating repeated miscarriages"')
    ],
    'recurrent-implantation-failure-ivf.html': [
        ('alt="Investigating IVF Failure"', 'alt="Leading fertility specialist Dr. Santosh Gupta presenting insights on Recurrent Implantation Failure and IVF success"')
    ],
    'understanding-severe-pcos-fertility.html': [
        ('alt="PCOS and Fertility"', 'alt="Dr. Santosh Gupta explaining PCOS and its impact on female fertility at a medical conference"')
    ],
    'my-journey-dr-santosh-gupta.html': [
        ('alt="Dr. Santosh Gupta"', 'alt="Dr. Santosh Gupta, highly experienced IVF specialist and senior consultant in Bengaluru"')
    ],
    'ovulation-calculator.html': [
        ('alt="Fertility Counseling"', 'alt="Expert fertility counseling session by Dr. Santosh Gupta, top gynecologist in Koramangala Bengaluru"')
    ],
    'male-infertility-icsi-treatment.html': [
        ('alt="Male Infertility and ICSI"', 'alt="Top ICSI treatment specialist Dr. Santosh Gupta discussing advanced male infertility solutions"')
    ],
    'blog.html': [
        ('alt="Dr. Santosh Gupta"', 'alt="Dr. Santosh Gupta, leading fertility specialist in Bengaluru"'),
        ('alt="Investigating IVF Failure"', 'alt="Dr. Santosh Gupta discussing Recurrent Implantation Failure and IVF success"'),
        ('alt="PCOS and Fertility"', 'alt="Insights on PCOS and female fertility by Dr. Santosh Gupta"'),
        ('alt="Male Infertility"', 'alt="Dr. Santosh Gupta discussing medical management and ART solutions for male infertility"')
    ]
}

for file, changes in replacements.items():
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        for old, new in changes:
            content = content.replace(old, new)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
