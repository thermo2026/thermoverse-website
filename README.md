# ThermoVerse

> **Where Building Intelligence Meets Grid Resilience**

ThermoVerse is an urban energy storage company headquartered in Detroit, Michigan. The company combines immediate building Energy Services (BPI assessments, ASHRAE audits, MEP consulting, and retrofits) with the development of **LATCHES** (Large-Area Transactive Cooling & Heat Energy Storage)—a BACnet-native, zero-footprint solid-state thermal battery designed for dense cities.

---

## 📁 Repository Structure

```text
ThermoVerse/
├── website/                         # Official prototype static website
│   ├── index.html                   # Home page (Hero animation, 4 challenges, 2 solutions, 3 applications)
│   ├── technology.html              # LATCHES technology & engineering specifications
│   ├── use-cases.html               # Use cases (Commercial, Industrial, Multifamily) & POC Site Partner intake
│   ├── about.html                   # Company mission, Taiwan milestones, team, and FACES workforce program
│   ├── contact.html                 # Service & POC inquiry routing form
│   ├── privacy.html                 # Privacy policy placeholder
│   ├── styles.css                   # Global styles & responsive design
│   ├── script.js                    # Mobile navigation toggle & client interactions
│   └── assets/                      # Next-gen WebP image assets & video media
│       ├── hero/                    # Interactive city canvas scene
│       └── partners/                # Institutional partner badges (DOE, ORNL, etc.)
├── HANDOFF.md                       # Comprehensive design specifications, changelog & SOW tracker
├── ThermoVerse_網站內容規劃.md        # Website content architecture and wireframes
├── ThermoVerse_產品與名詞入門.md      # Domain glossary and product positioning guide
└── .gitignore                       # Standard ignore rules (build artifacts, temporary libs, OS files)
```

---

## 🚀 Quick Start (Local Preview)

To run the website locally without any external dependencies:

```bash
# Option 1: Serve directly with Python from root
python3 -m http.server 8000 --directory website

# Option 2: Run from within the website directory
cd website
python3 -m http.server 8000
```

Then open your browser to [http://localhost:8000](http://localhost:8000).

---

## 🌐 GitHub Pages Deployment

This site is built with pure standards-compliant HTML5, CSS3, and JavaScript, requiring no build step or package manager.

To deploy via **GitHub Pages**:
1. Push this repository to GitHub.
2. In your repository settings:
   - Go to **Settings** > **Pages**.
   - Under **Build and deployment** > **Source**, choose **GitHub Actions** (recommended) or deploy from the `main` branch.
   - Alternatively, copy the contents of `website/` to root or a `docs/` directory to serve directly via GitHub Pages static branch mode.

---

## 📄 Documentation & References

- [HANDOFF.md](HANDOFF.md): Detailed changelog of UI/UX updates, WebP conversions, and delivery milestones.
- [website/CONTENT_COVERAGE.md](website/CONTENT_COVERAGE.md): Content mapping and guidelines coverage matrix.
- [website/PM_REVIEW.md](website/PM_REVIEW.md): PM checklist and acceptance verification.
