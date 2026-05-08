import csv, os, re

csv_path = os.path.expanduser('~/.paperclip/instances/default/companies/ae654e05-5008-4385-be0a-8157962628e4/shared/sourcing/W19-CRE-prospects.csv')
prospects = []
with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        prospects.append(row)

# Unsplash images by vertical
UNSPLASH = {
    'salon': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&fit=crop&q=80',
    'cleaner': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800&fit=crop&q=80',
    'electrician': 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=800&fit=crop&q=80',
    'mechanic': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&fit=crop&q=80',
    'restaurant': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&fit=crop&q=80',
}

VERTICAL_SERVICES = {
    'salon': [
        ('Precision Haircuts', 'From classic cuts to modern styles — tailored to your face shape and lifestyle.'),
        ('Colour & Balayage', 'Expert colour correction, balayage, and root touch-ups using premium products.'),
        ('Styling & Treatments', 'Blow-drys, deep conditioning, and special occasion styling.'),
    ],
    'cleaner': [
        ('Home Cleaning', 'Weekly or fortnightly domestic cleaning — flexible schedules to suit you.'),
        ('Deep Cleaning', 'One-off deep cleans for kitchens, bathrooms, carpets and more.'),
        ('Office & Commercial', 'Regular cleaning contracts for offices, retail spaces and commercial units.'),
    ],
    'electrician': [
        ('Electrical Repairs', 'Fast, certified repairs for faults, tripping circuits, and power outages.'),
        ('Rewiring & Installations', 'Full and partial rewiring, fuse board upgrades, and lighting installations.'),
        ('Emergency Call-Outs', '24/7 emergency electrician available across our service area.'),
    ],
    'mechanic': [
        ('Diagnostics & Servicing', 'Full vehicle diagnostics, oil changes, and routine servicing.'),
        ('MOT & Repairs', 'Pre-MOT checks, brake repairs, suspension work, and more.'),
        ('Fleet Maintenance', 'Regular maintenance contracts for vans, lorries, and company vehicles.'),
    ],
    'restaurant': [
        ('Steak & Grill', 'Premium cuts of aged beef, flame-grilled to your exact preference.'),
        ('Fine Dining Menu', 'Seasonal tasting menus with locally sourced ingredients.'),
        ('Private Dining', 'Exclusive hire options for celebrations, corporate events, and parties.'),
    ],
}

def make_html(p):
    name = p['name'].strip('"')
    slug = re.sub(r'[^a-z0-9-]+', '-', name.lower()).strip('-')
    vertical = p['vertical']
    city = p['city']
    pain_hook = p['pain_hook']
    first_name = p['owner_first_name'] or 'there'

    brand = {'salon':'#c0392b','cleaner':'#27ae60','electrician':'#2980b9','mechanic':'#f39c12','restaurant':'#8e44ad'}.get(vertical, '#2c3e50')
    img = UNSPLASH.get(vertical, 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800&fit=crop&q=80')
    services = VERTICAL_SERVICES.get(vertical, [
        ('Service One', 'Quality service delivered professionally.'),
        ('Service Two', 'Customer-focused approach to every job.'),
        ('Service Three', 'Reliable and fairly priced.'),
    ])
    cta = {'salon':'Book Appointment','cleaner':'Book a Clean','electrician':'Get a Quote','mechanic':'Book Service','restaurant':'Reserve a Table'}.get(vertical, 'Enquire Now')

    services_html = '\n'.join([
        f'    <div class="service-card"><h3>{s[0]}</h3><p>{s[1]}</p></div>'
        for s in services
    ])

    logo_text = name.split('.')[0].replace('-', ' ').title()

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — Professional {vertical.title()} in {city}</title>
<style>
:root{{--brand:{brand};}}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,-apple-system,sans-serif}}
body{{color:#333;line-height:1.6}}
header{{position:sticky;top:0;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,0.1);z-index:1000}}
.header-inner{{max-width:1140px;margin:0 auto;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between}}
.logo{{font-weight:800;font-size:1.4rem;color:var(--brand);text-decoration:none}}
.hero{{background:linear-gradient(135deg,rgba(0,0,0,0.6),rgba(0,0,0,0.6)),url({img});background-size:cover;background-position:center;color:#fff;padding:6rem 2rem;text-align:center}}
.hero h1{{font-size:2.5rem;margin-bottom:1rem;text-shadow:0 2px 4px rgba(0,0,0,0.3)}}
.hero p{{font-size:1.1rem;max-width:600px;margin:0 auto 2rem}}
.btn{{display:inline-block;padding:0.9rem 2rem;border-radius:8px;text-decoration:none;font-weight:600;transition:all 0.3s}}
.btn-primary{{background:#fff;color:var(--brand)}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 10px 20px rgba(0,0,0,0.2)}}
section{{padding:4rem 2rem;max-width:1140px;margin:0 auto}}
.pain-hook{{background:#f8f9fa;border-left:5px solid var(--brand);padding:1.5rem;margin:2rem auto;max-width:800px;border-radius:0 8px 8px 0}}
.services{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem}}
.service-card{{background:#fff;padding:2rem;border-radius:12px;box-shadow:0 4px 6px rgba(0,0,0,0.07);border-top:4px solid var(--brand);transition:transform 0.2s}}
.service-card:hover{{transform:translateY(-4px)}}
.service-card h3{{color:var(--brand);margin-bottom:0.5rem;font-size:1.1rem}}
.contact-form{{background:#f8f9fa;padding:2rem;border-radius:12px;margin-top:2rem}}
.form-row{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}}
input,textarea,select{{width:100%;padding:0.8rem;border:1px solid #ddd;border-radius:6px;font-size:1rem;font-family:inherit}}
input[type="submit"]{{background:var(--brand);color:#fff;border:none;cursor:pointer;font-weight:600;padding:1rem 2.5rem;width:auto}}
input[type="submit"]:hover{{opacity:0.9}}
.honeypot{{position:absolute;left:-5000px}}
footer{{background:#1a1a2e;color:#fff;text-align:center;padding:2rem;margin-top:4rem}}
.tag{{display:inline-block;background:var(--brand);color:#fff;padding:0.2rem 0.8rem;border-radius:20px;font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:1rem}}
@media(max-width:768px){{
.hero h1{{font-size:1.8rem}}
.form-row{{grid-template-columns:1fr}}
.services{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <a href="#" class="logo">{logo_text}</a>
  </div>
</header>

<section class="hero">
  <div class="tag">{vertical.title()} · {city}</div>
  <h1>Your New Website</h1>
  <p>Hi {first_name}, this is a preview of what Creativ Agentz could build for {name}. A modern, mobile-friendly site that turns browsers into customers.</p>
  <a href="#contact" class="btn btn-primary">{cta}</a>
</section>

<section>
  <div class="pain-hook">
    <h3>💡 Your Growth Opportunity</h3>
    <p>{pain_hook} A professional website with online booking fixes this instantly.</p>
  </div>
</section>

<section>
  <p class="tag" style="display:block;text-align:center;margin:0 auto 0.5rem;width:fit-content">What We Offer</p>
  <h2 style="text-align:center;margin-bottom:0.5rem">Popular Services</h2>
  <p style="text-align:center;color:#666;margin-bottom:2rem">These would be customised to match your exact services.</p>
  <div class="services">
{services_html}
  </div>
</section>

<section>
  <p class="tag" style="display:block;text-align:center;margin:0 auto 0.5rem;width:fit-content">Why Creativ Agentz</p>
  <h2 style="text-align:center;margin-bottom:0.5rem">What You Get</h2>
  <div class="services">
    <div class="service-card"><h3>📱 Mobile-First Design</h3><p>Over 70% of local searches happen on mobile. Your site will look stunning and load fast on every device.</p></div>
    <div class="service-card"><h3>🔍 Google Optimised</h3><p>Built with schema markup, fast loading, and local SEO so customers in {city} find you first.</p></div>
    <div class="service-card"><h3>✅ Online Booking</h3><p>Let customers book or request quotes 24/7 — never miss a lead again.</p></div>
  </div>
</section>

<section id="contact">
  <p class="tag" style="display:block;text-align:center;margin:0 auto 0.5rem;width:fit-content">Let's Talk</p>
  <h2 style="text-align:center;margin-bottom:0.5rem">Get in Touch</h2>
  <p style="text-align:center;color:#666;margin-bottom:2rem">Interested in your own site? We'd love to hear from you.</p>
  <div class="contact-form">
    <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
      <input type="text" name="_gotcha" class="honeypot" />
      <div class="form-row">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Email Address" required>
      </div>
      <div class="form-row">
        <input type="tel" name="phone" placeholder="Phone Number">
        <select name="service">
          <option value="">Interested in...</option>
          <option value="new-website">New Website</option>
          <option value="redesign">Website Redesign</option>
          <option value="booking">Online Booking System</option>
          <option value="seo">SEO & Google Ranking</option>
        </select>
      </div>
      <textarea name="message" rows="4" placeholder="Tell us about your business..."></textarea>
      <p style="margin-top:1rem"><input type="submit" value="Send Message"></p>
    </form>
  </div>
</section>

<footer>
  <p>© 2026 {logo_text} — {city}</p>
  <p style="font-size:0.8rem;opacity:0.7;margin-top:0.5rem">Preview site built by <a href="https://creativagentz.com" style="color:var(--brand)">Creativ Agentz</a> · This is a demo preview</p>
</footer>

</body>
</html>
'''

for p in prospects:
    slug = re.sub(r'[^a-z0-9-]+', '-', p['name'].strip('"').lower()).strip('-')
    dir_path = f'/home/paperclip/.paperclip/instances/default/projects/ae654e05-5008-4385-be0a-8157962628e4/w19-preview-sites/{slug}'
    os.makedirs(dir_path, exist_ok=True)
    html = make_html(p)
    with open(f'{dir_path}/index.html', 'w') as f:
        f.write(html)
    print(f"Generated: {slug}")

print(f"\nDone! {len(prospects)} rich preview sites generated.")
