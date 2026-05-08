#!/usr/bin/env python3
"""Generate QA-passing preview sites for W19 CRE prospects."""
import csv, os, re

CSV_PATH = os.path.expanduser(
    '~/.paperclip/instances/default/companies/ae654e05-5008-4385-be0a-8157962628e4/shared/sourcing/W19-CRE-prospects.csv'
)
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
STRIPE_LINK = 'https://buy.stripe.com/cNi00j5Pz3TtbNl6rv6c00j'

UNSPLASH = {
    'salon':       'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=1200&fit=crop&q=80',
    'cleaner':     'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1200&fit=crop&q=80',
    'electrician': 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=1200&fit=crop&q=80',
    'mechanic':    'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=1200&fit=crop&q=80',
    'restaurant':  'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200&fit=crop&q=80',
}

BRAND_COLORS = {
    'salon':       '#c0392b',
    'cleaner':     '#27ae60',
    'electrician': '#2980b9',
    'mechanic':    '#e67e22',
    'restaurant':  '#8e44ad',
}

VERTICAL_SERVICES = {
    'salon': [
        ('Precision Haircuts', 'From R150', 'Classic and modern cuts tailored to your face shape and lifestyle.'),
        ('Colour & Balayage', 'From R450', 'Expert colour correction, balayage, and root touch-ups with premium products.'),
        ('Styling & Treatments', 'From R200', 'Blow-drys, deep conditioning treatments, and special occasion styling.'),
        ('Hair Extensions', 'From R800', 'High-quality extensions for length, volume, and bold transformations.'),
    ],
    'cleaner': [
        ('Home Cleaning', 'From R350/visit', 'Weekly or fortnightly domestic cleaning — kitchens, bathrooms, bedrooms and more.'),
        ('Deep Cleaning', 'From R1,200', 'Full top-to-bottom deep clean including inside appliances, behind furniture, and skirting boards.'),
        ('Office & Commercial', 'From R950/month', 'Scheduled after-hours office cleaning to keep your workspace spotless every day.'),
        ('Move-In / Move-Out', 'From R1,500', 'Get your deposit back. Professional empty-property clean with checklist sign-off.'),
    ],
    'electrician': [
        ('Fault Finding & Repairs', 'From R350 call-out', 'Fast diagnosis and repair of tripping circuits, power faults, and wiring issues.'),
        ('Rewiring & Installations', 'From R850', 'Full and partial rewiring, DB board upgrades, and lighting installations.'),
        ('Emergency Call-Outs', 'R450/hour (24/7)', '24-hour emergency electrician available across the Johannesburg/Pretoria area.'),
        ('Certificate of Compliance', 'From R1,200', 'COC issued by a registered electrician — required for property sales and rentals.'),
    ],
    'mechanic': [
        ('Vehicle Diagnostics', 'From R450', 'Full computer diagnostics to identify faults before they become expensive problems.'),
        ('Scheduled Servicing', 'From R650', 'Oil changes, filters, brake checks, and manufacturer-recommended service schedules.'),
        ('Brake & Suspension', 'From R750', 'Brake pad replacement, disc skimming, shock absorber checks and replacements.'),
        ('Fleet Maintenance', 'Custom quote', 'Monthly maintenance contracts for business vehicles — vans, bakkies, and trucks.'),
    ],
    'restaurant': [
        ('A La Carte Dining', 'Mains from R185', 'Seasonal menu featuring locally sourced ingredients and wood-fired flavours.'),
        ('Set Tasting Menu', 'From R450/person', 'Chef-curated 5-course tasting experience with optional wine pairing.'),
        ('Private Dining', 'From R3,500 hire', 'Exclusive venue hire for celebrations, corporate dinners, and private events.'),
        ('Sunday Brunch', 'R275/person', 'Weekly brunch buffet with free-flow mimosas — advance booking required.'),
    ],
}

CTA_BY_VERTICAL = {
    'salon':       'Book a Styling Session',
    'cleaner':     'Book a Free Quote',
    'electrician': 'Request a Call-Out',
    'mechanic':    'Book a Diagnostic',
    'restaurant':  'Reserve a Table',
}

def base_name(domain):
    """Extract base business name from domain for email placeholder."""
    # e.g. orizoeservices.co.za → orizoeservices
    parts = domain.split('.')
    if len(parts) >= 2:
        return parts[0]
    return domain

def make_html(p):
    name_raw  = p['name'].strip('"').strip()
    slug      = re.sub(r'[^a-z0-9-]+', '-', name_raw.lower()).strip('-')
    vertical  = p['vertical'].lower()
    city      = p['city']
    pain_hook = p['pain_hook']
    first     = p['owner_first_name']

    brand     = BRAND_COLORS.get(vertical, '#2c3e50')
    img       = UNSPLASH.get(vertical, UNSPLASH['cleaner'])
    services  = VERTICAL_SERVICES.get(vertical, VERTICAL_SERVICES['cleaner'])
    cta       = CTA_BY_VERTICAL.get(vertical, 'Get a Free Quote')

    # Derive display name (title-case base domain part)
    base      = base_name(name_raw)
    display   = ' '.join(w.capitalize() for w in re.split(r'[^a-z0-9]+', base) if w)

    email_ph  = f'info@{base}.co.za'

    services_html = '\n'.join(
        f'''      <div class="service-card">
        <div class="price-tag">{svc[1]}</div>
        <h3>{svc[0]}</h3>
        <p>{svc[2]}</p>
      </div>'''
        for svc in services
    )

    return f'''<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{display} | Preview Site by Creativ Agentz</title>
<meta name="description" content="Preview website for {display} — {vertical} services in {city}. Built by Creativ Agentz.">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LocalBusiness","name":"{display}","address":{{"@type":"PostalAddress","addressLocality":"{city}","addressCountry":"ZA"}}}}
</script>
<style>
:root{{--brand:{brand};--dark:#1a1a2e;--light:#f8f9fa}}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,-apple-system,sans-serif}}
body{{color:#333;line-height:1.6;background:#fff}}
/* Nav */
header{{position:sticky;top:0;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.1);z-index:1000}}
.nav-inner{{max-width:1140px;margin:0 auto;padding:.9rem 2rem;display:flex;align-items:center;justify-content:space-between}}
.logo{{font-weight:800;font-size:1.4rem;color:var(--brand);text-decoration:none}}
.nav-cta{{background:var(--brand);color:#fff;padding:.6rem 1.4rem;border-radius:8px;text-decoration:none;font-weight:600;font-size:.9rem}}
/* Hero */
.hero{{background:linear-gradient(135deg,rgba(0,0,0,.65),rgba(0,0,0,.45)),url({img}) center/cover no-repeat;color:#fff;padding:5rem 2rem;text-align:center}}
.badge{{display:inline-block;background:var(--brand);color:#fff;padding:.3rem .9rem;border-radius:20px;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:1.2rem}}
.hero h1{{font-size:clamp(1.8rem,5vw,3rem);font-weight:800;margin-bottom:1rem;line-height:1.2}}
.hero p{{font-size:1.1rem;max-width:620px;margin:0 auto 2rem;opacity:.92}}
.btn-group{{display:flex;flex-wrap:wrap;gap:1rem;justify-content:center}}
.btn{{display:inline-block;padding:.9rem 2rem;border-radius:8px;text-decoration:none;font-weight:600;transition:transform .2s,box-shadow .2s}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.2)}}
.btn-primary{{background:#fff;color:var(--brand)}}
.btn-stripe{{background:var(--brand);color:#fff;border:2px solid rgba(255,255,255,.3)}}
/* Pain hook */
.pain-section{{background:var(--light);padding:2.5rem 2rem}}
.pain-inner{{max-width:860px;margin:0 auto;border-left:5px solid var(--brand);padding:1.4rem 1.6rem;background:#fff;border-radius:0 10px 10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06)}}
.pain-inner h3{{color:var(--brand);margin-bottom:.5rem;font-size:1.05rem}}
/* Services */
.services-section{{padding:4rem 2rem}}
.section-inner{{max-width:1140px;margin:0 auto}}
.section-label{{display:block;text-align:center;background:var(--brand);color:#fff;padding:.25rem .8rem;border-radius:20px;font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin:0 auto .6rem;width:fit-content}}
h2{{text-align:center;font-size:1.8rem;margin-bottom:.4rem}}
.subtitle{{text-align:center;color:#666;margin-bottom:2.5rem;font-size:.95rem}}
.services-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem}}
.service-card{{background:#fff;padding:1.6rem;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,.07);border-top:4px solid var(--brand);transition:transform .2s}}
.service-card:hover{{transform:translateY(-4px)}}
.price-tag{{background:var(--brand);color:#fff;padding:.2rem .6rem;border-radius:6px;font-size:.75rem;font-weight:700;display:inline-block;margin-bottom:.6rem}}
.service-card h3{{font-size:1rem;margin-bottom:.4rem;color:var(--dark)}}
.service-card p{{font-size:.88rem;color:#555;line-height:1.5}}
/* Why us */
.why-section{{background:var(--dark);color:#fff;padding:4rem 2rem}}
.why-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem;margin-top:2rem}}
.why-card{{padding:1.4rem;border-radius:10px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12)}}
.why-card h3{{margin-bottom:.4rem;font-size:1rem}}
.why-card p{{font-size:.85rem;opacity:.8;line-height:1.5}}
/* Contact */
.contact-section{{padding:4rem 2rem;background:var(--light)}}
.contact-box{{max-width:760px;margin:0 auto;background:#fff;border-radius:14px;padding:2.4rem;box-shadow:0 4px 20px rgba(0,0,0,.08)}}
.contact-meta{{display:flex;flex-wrap:wrap;gap:1.2rem;margin-bottom:2rem}}
.contact-item{{display:flex;align-items:center;gap:.5rem;font-size:.95rem}}
.contact-item a{{color:var(--brand);text-decoration:none;font-weight:600}}
.form-row{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}}
input,textarea,select{{width:100%;padding:.8rem;border:1px solid #ddd;border-radius:6px;font-size:.95rem;font-family:inherit}}
input:focus,textarea:focus,select:focus{{outline:none;border-color:var(--brand)}}
.honeypot{{position:absolute;left:-9999px}}
.submit-btn{{background:var(--brand);color:#fff;border:none;cursor:pointer;font-weight:700;padding:1rem 2.5rem;border-radius:8px;font-size:1rem;transition:opacity .2s}}
.submit-btn:hover{{opacity:.88}}
/* Footer */
footer{{background:var(--dark);color:#fff;text-align:center;padding:2rem 1.5rem}}
footer p{{font-size:.85rem;opacity:.75;margin-top:.5rem}}
.popia-notice{{font-size:.78rem;opacity:.6;margin-top:.8rem;max-width:700px;margin-left:auto;margin-right:auto;line-height:1.5}}
/* Responsive */
@media(max-width:640px){{
.hero{{padding:3rem 1.5rem}}
.form-row{{grid-template-columns:1fr}}
.nav-cta{{display:none}}
}}
</style>
</head>
<body>

<header>
  <div class="nav-inner">
    <a href="#" class="logo">{display}</a>
    <a href="#contact" class="nav-cta">{cta}</a>
  </div>
</header>

<section class="hero">
  <span class="badge">{vertical.title()} · {city}</span>
  <h1>Your Business Deserves a Better Website.</h1>
  <p>Hi {first}, this is a preview of what Creativ Agentz could build for <strong>{display}</strong>. A modern, mobile-first site that turns visitors into paying customers — live in 5 business days.</p>
  <div class="btn-group">
    <a href="#contact" class="btn btn-primary">{cta}</a>
    <a href="{STRIPE_LINK}" class="btn btn-stripe" target="_blank" rel="noopener">💳 Claim Your Site — from R3,999</a>
  </div>
</section>

<section class="pain-section">
  <div class="pain-inner">
    <h3>💡 Your Growth Opportunity</h3>
    <p>{pain_hook}. A professional website with online booking and Google-optimised pages fixes this — and Creativ Agentz can have yours live in days, not weeks.</p>
  </div>
</section>

<section class="services-section">
  <div class="section-inner">
    <span class="section-label">Services</span>
    <h2>What {display} Could Offer Online</h2>
    <p class="subtitle">These service pages would be customised to match your exact offerings and pricing in ZAR.</p>
    <div class="services-grid">
{services_html}
    </div>
  </div>
</section>

<section class="why-section">
  <div class="section-inner">
    <span class="section-label" style="background:rgba(255,255,255,.15);color:#fff">Why Creativ Agentz</span>
    <h2 style="color:#fff">What You Get With Your New Site</h2>
    <div class="why-grid">
      <div class="why-card">
        <h3>📱 Mobile-First Design</h3>
        <p>Over 70% of local searches happen on mobile. Your site will look stunning and load fast on every device.</p>
      </div>
      <div class="why-card">
        <h3>🔍 Local SEO Built-In</h3>
        <p>Schema markup, fast Core Web Vitals, and local keyword optimisation so customers in {city} find you first.</p>
      </div>
      <div class="why-card">
        <h3>📅 Online Booking</h3>
        <p>Let customers book or request quotes 24/7 without calling. Never miss a lead again.</p>
      </div>
      <div class="why-card">
        <h3>🚀 Live in 5 Days</h3>
        <p>We build, host, and deploy — you just approve. No technical knowledge needed.</p>
      </div>
    </div>
  </div>
</section>

<section class="contact-section" id="contact">
  <div class="section-inner">
    <span class="section-label">Contact</span>
    <h2>Get in Touch with {display}</h2>
    <p class="subtitle">Fill in the form below and we'll be in touch within one business day.</p>
    <div class="contact-box">
      <div class="contact-meta">
        <span class="contact-item">📞 <a href="tel:+27000000000">+27 (your number)</a></span>
        <span class="contact-item">✉️ <a href="mailto:{email_ph}">{email_ph}</a></span>
        <span class="contact-item">📍 {city}, South Africa</span>
      </div>
      <form action="mailto:{email_ph}" method="POST" enctype="text/plain">
        <input type="text" name="_gotcha" class="honeypot" tabindex="-1" autocomplete="off">
        <div class="form-row">
          <input type="text" name="name" placeholder="Your Name" required>
          <input type="email" name="email" placeholder="Email Address" required>
        </div>
        <div class="form-row">
          <input type="tel" name="phone" placeholder="Phone Number">
          <select name="service">
            <option value="">Service of interest...</option>
            <option>New Website (from R3,999)</option>
            <option>Website Redesign</option>
            <option>Online Booking System</option>
            <option>Google SEO Package</option>
          </select>
        </div>
        <textarea name="message" rows="4" placeholder="Tell us about your business and what you need..." style="margin-bottom:1rem"></textarea>
        <button type="submit" class="submit-btn">Send Message →</button>
      </form>
    </div>
  </div>
</section>

<footer>
  <p>© 2026 {display} — {city}, South Africa</p>
  <p>Preview site built by <a href="https://creativagentz.com" style="color:var(--brand)">Creativ Agentz</a> · This is a demo — not the live site</p>
  <p class="popia-notice">In accordance with the Protection of Personal Information Act (POPIA), Act 4 of 2013, personal information submitted via this form is collected solely for the purpose of responding to your enquiry and will not be shared with third parties without your consent. You have the right to access, correct, or request deletion of your information at any time by contacting us at {email_ph}.</p>
</footer>

</body>
</html>
'''

def main():
    with open(CSV_PATH, newline='') as f:
        rows = list(csv.DictReader(f))

    for p in rows:
        name_raw = p['name'].strip('"').strip()
        slug     = re.sub(r'[^a-z0-9-]+', '-', name_raw.lower()).strip('-')
        dir_path = os.path.join(OUT_DIR, slug)
        os.makedirs(dir_path, exist_ok=True)
        html = make_html(p)
        with open(os.path.join(dir_path, 'index.html'), 'w') as fh:
            fh.write(html)
        print(f'  ✓ {slug}')

    print(f'\nDone — {len(rows)} sites generated.')

if __name__ == '__main__':
    main()
