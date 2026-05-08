const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
app.set('trust proxy', true);
const ROOT = __dirname;
const PORT = process.env.PORT || 3000;

app.use((req, res) => {
  // Traefik/Cloudflare may rewrite Host; prefer X-Forwarded-Host
  const rawHost = req.get('x-forwarded-host') || req.get('host') || req.hostname || '';
  const host = rawHost.split('.')[0];
  const siteDir = path.join(ROOT, host);

  if (host && fs.existsSync(path.join(siteDir, 'index.html'))) {
    res.sendFile(path.join(siteDir, 'index.html'));
  } else {
    const indexPath = path.join(ROOT, 'index.html');
    if (fs.existsSync(indexPath)) {
      res.sendFile(indexPath);
    } else {
      res.status(404).send('Site not found');
    }
  }
});

app.listen(PORT, () => console.log(`W19 preview sites on :${PORT}`));
