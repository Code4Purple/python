launch.py		The one command you run every time
config.py 		Edit this to change anything on the site
generator.py 		Builds the HTML (no need to touch)
requirements.txt	For manual pip install if preferred


To use it anywhere:

Unzip the folder
Run python launch.py
Browser opens automatically at localhost:8080

It auto-installs jinja2 (the only dependency) on first run, so it works on any machine with Python 3.8+.
Your workflow from here:

Edit brand name, colors, copy → config.py
Add/remove features, FAQ entries, pricing tiers → config.py
Run python launch.py → rebuilt site appears instantly
When ready to go live → drag the dist/ folder to Netlify (free, takes 30 seconds)
