# PM review — Final Draft English website version

2026-09-11

## Source authority

- Website content now follows `FUTEX SOW - FINAL DRAFT (9_8).docx`, with the final **Website Guidelines** section controlling page headlines, messages, metrics, application content, and calls to action.
- The previous implementation rule that treated `ThermoVerse_網站內容規劃.md` as the content authority has been superseded where the two sources conflict.
- Project Overview, Team Roles and Responsibilities, and the June–September 2026 Taiwan milestone table supply the About Us facts.

## Implemented for local review

- Home uses the required headline and balances immediate Energy Services with LATCHES innovation. It includes all four facility challenges, all four services, LATCHES metrics, three asset classes with EUI, measured-data uses, and documented Partners and Awards.
- Technology uses the required ceiling headline and covers the zero-footprint/fire-code/floor-area proposition, 102 BTU/SF PCM capacity, four-hour setpoint claim, predictive edge control, ceiling/wall installation, 8× installation claim, BACnet-native BAS integration, and the required FAQ topics.
- Use Cases & Services reproduces the Final Draft application matrix for commercial, industrial, and multifamily properties. Both required CTAs are present, and the POC non-agreement condition remains explicit.
- About Us now includes the documented Detroit positioning, company background, named team roles, ICTGC/IAPS/LMT/Build for NextGen milestones, FAITHE values, FACES Workforce Program, and Detroit/Taiwan location context. No unsupported founder biography was added.
- Contact explicitly routes immediate Energy Services separately from LATCHES partnership interest. It retains four required fields, five inquiry types, optional unchecked marketing consent, conditional POC fields, source/language fields, and preview-only behavior with no submission or storage claim.
- All five pages retain the approved white, spacious, thin-line visual system in ThermoVerse coral and deep blue-gray, with translucent pill controls.

## Still required for the contracted final website

- Traditional Chinese pages and page-preserving language switching.
- Production CRM storage, notification, administrator access, lead status/notes, search/filter, and CSV export.
- Company-approved privacy notice, lawful collection purpose, retention terms, marketing-consent wording, notification recipient, and response time.
- Company written approval of technical, performance, safety, code-compliance, energy-saving, emissions, incentive, and carbon-credit claims.
- Final supporting links/assets for awards, partners, certifications, team photography, and public contact details.
- Production integration and publication.

This remains an English local review version and is not approval for publication or completion of the bilingual/CRM scope.

## 2026-09-11 — Animated hero

- Replaced the static hero image with a full-width, text-free 30-second Canvas animation; preserved the existing approved homepage copy below the animation.
- Added `hero-animation.html`, `assets/hero/scene.js`, and `assets/hero/embed.js`. Uses projected 3D geometry with no external packages or network assets.
- Sequence: aerial city, office-floor cutaway with occupants, thermal visualization, ceiling storage and heat particles, cyan sensor/data network, unlabelled control-room display with a falling peak curve, return to city.
- Added an icon-only pause/play control, reduced-motion static view, and offscreen/tab-hidden animation suspension.
- Checked seven desktop timeline positions, the 390px mobile homepage, pause control, and browser errors: no JavaScript errors and no horizontal overflow. Conceptual geometry and curves are illustrative, not an installation drawing or measured savings data.
- Standalone preview: `hero-animation.html`; current local preview server uses port 8879. This is a stylized browser animation, not photorealistic generated footage. No publication performed.

## 2026-09-11 — Photo opening and overhead power grid, revision 2

- Uses the user-supplied `1000_F_234415650_VF4KNCN0qCUchFeleqiIB8zsSvE8MGQh.jpg` as the opening, stored unchanged at `assets/hero/city-opening.jpg`. Source watermarks remain visible; the animation adds no typography.
- Tracks the right-hand blue glass tower during the photo zoom, traces its visible facade floors, then dissolves into a six-floor conceptual office cutaway. The interior is illustrative, not a surveyed reconstruction of the photographed building.
- Added a luminous overhead power-grid plane, white/cyan energy ribbons, and orange/white ceiling heat-flow beams based on the second reference image. Its pixels are not embedded.
- Preserves the thermal-storage, building-controls and loop-return sequence. Updated desktop timeline screenshots and mobile checks show no script errors or horizontal overflow.
- Revised export: `../output/hero-preview/ThermoVerse-Hero-v2.webm`; original export retained.
