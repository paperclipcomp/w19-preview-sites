const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
app.set('trust proxy', true);
const ROOT = __dirname;
const PORT = process.env.PORT || 3000;

// Debug endpoint — shows received headers to diagnose Traefik/Cloudflare routing
app.get('/__debug', (req, res) => {
  res.json({
    host: req.get('host'),
    x_forwarded_host: req.get('x-forwarded-host'),
    x_forwarded_for: req.get('x-forwarded-for'),
    x_real_ip: req.get('x-real-ip'),
    hostname: req.hostname,
    all_headers: req.headers,
    resolved_slug: (req.get('x-forwarded-host') || req.get('host') || req.hostname || '').split(',')[0].trim().split('.')[0],
  });
});

app.use((req, res) => {
  // X-Forwarded-Host may contain multiple values (comma-separated) if both CF and Traefik set it
  // Take the first value, then the first subdomain segment
  const rawHostFull = req.get('x-forwarded-host') || req.get('host') || req.hostname || '';
  const rawHost = rawHostFull.split(',')[0].trim();
  const host = rawHost.split('.')[0];
  const siteDir = path.join(ROOT, host);

  console.log(`[route] rawHostFull=${rawHostFull} rawHost=${rawHost} host=${host} exists=${fs.existsSync(path.join(siteDir, 'index.html'))}`);

  if (host && fs.existsSync(path.join(siteDir, 'index.html'))) {
    res.sendFile(path.join(siteDir, 'index.html'));
  } else {
    const indexPath = path.join(ROOT, 'fallback.html');
    if (fs.existsSync(indexPath)) {
      res.sendFile(indexPath);
    } else {
      res.status(404).send('Site not found');
    }
  }
});

app.listen(PORT, () => console.log(`W19 preview sites on :${PORT}`));
