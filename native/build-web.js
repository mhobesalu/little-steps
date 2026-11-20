// Builds native/www from the web app in the repo root, for the App Store and Google Play builds.
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const out = path.join(__dirname, 'www');
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
fs.copyFileSync(path.join(root, 'index.html'), path.join(out, 'index.html'));
fs.cpSync(path.join(root, 'fonts'), path.join(out, 'fonts'), { recursive: true });
console.log('build-web: wrote', out);
