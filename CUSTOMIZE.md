# Customize and install this profile theme

## Important: the ZIP is only the delivery container

You do **not** put the ZIP file inside your GitHub README repository. Extract it first, then copy the extracted files into the root of the public profile repository named exactly like your GitHub username.

For `naveenkarasu`, the repository root should look like this:

```text
naveenkarasu/
├── README.md
├── CUSTOMIZE.md
├── assets/
├── profile-3d-contrib/
├── scripts/
└── .github/
    └── workflows/
        └── profile-assets.yml
```

`README.md` uses relative paths such as `./assets/skills.svg`, so `README.md` and `assets/` must be siblings at the repository root.

## No broken first-run images

This package includes placeholders for both generated contribution sections:

- `profile-3d-contrib/profile-night-green.svg`
- `profile-3d-contrib/profile-green.svg`
- `assets/contribution-snake-dark.svg`
- `assets/contribution-snake-light.svg`

That means the profile renders immediately after upload. The first successful workflow run replaces the placeholders with your real contribution data.

## NIGHTSHIFT pieces intentionally adopted

The visual identity stays with the current anime + terminal + pixel + capsule/aura mockup. Two NIGHTSHIFT implementation ideas are brought in because they improve the profile without changing its personality:

1. **Light/dark mode:** GitHub `<picture>` elements select matching dark or light SVG panels automatically. The anime night-city hero remains dark in both themes as the visual anchor.
2. **Least-privilege workflow:** the workflow is read-only by default. The `build` job receives only `contents: read`; only the short `publish` job receives `contents: write` so it can commit refreshed images.

## Skill categories

The source of truth is the `skills = [...]` block in `scripts/build_static_assets.py`. The included categories are:

```text
LANGUAGES & SCRIPTING
FRAMEWORKS & TOOLS
CLOUD & PLATFORMS
SIEM & DETECTION
ANALYSIS & SCANNING
SECURITY DOMAINS
```

The included `SIEM & DETECTION` category contains Splunk, Microsoft Sentinel, ELK Stack, QRadar, Sigma, and MITRE ATT&CK.

Edit the arrays rather than hand-editing `assets/skills.svg`, then regenerate:

```bash
python scripts/build_static_assets.py
```

The script creates both `skills.svg` and `skills-light.svg`.

## Featured projects

Edit the three `project_card(...)` calls near the bottom of `scripts/build_static_assets.py`. Replace title, repository, tags, description, thumbnail, and accent color as needed. Running the script regenerates both dark and light project cards.

## Dynamic portrait, stats, and activity

`generate_ascii_profile.py` downloads the GitHub account avatar and renders both:

- `assets/ascii-profile.svg`
- `assets/ascii-profile-light.svg`

`generate_github_data.py` writes both theme variants for GitHub stats and recent public activity.

## 3D contribution graph

The workflow uses `github-profile-3d-contrib` and keeps two generated files in the README:

- dark mode → `profile-night-green.svg`
- light mode → `profile-green.svg`

The repository placeholders are replaced automatically on the first workflow run.

## Contribution snake

The workflow generates two snake files with the same cyber palette:

- `assets/contribution-snake-dark.svg`
- `assets/contribution-snake-light.svg`

## First run

After committing the package to the profile repository:

1. Open **Actions**.
2. Select **Refresh profile visuals**.
3. Choose **Run workflow**.
4. After the workflow commits the generated assets, refresh the GitHub profile.

The workflow also runs once a day.

## Color system

Dark mode:

```text
Background       #050B12
Panel            #07131D
Panel secondary  #091925
Border           #0B5A70
Neon green       #00F5A0
Cyan             #22D3EE
Blue             #3B82F6
Purple           #8B5CF6
Pink             #EC4899
Text             #E6F1F5
Muted text       #94A3B8
```

Light mode:

```text
Background       #F6F8FA
Panel            #FFFFFF
Panel secondary  #EFF6F8
Border           #7AA7B7
Green            #00875F
Cyan             #007C91
Blue             #0969DA
Purple           #6639BA
Pink             #BF3989
Text             #17212B
Muted text       #57606A
```

## Design mapping to the six inspirations

- Anime/personality → hero banner and scene artwork.
- Capsule render → rounded geometry and wave-like footer treatment, implemented locally.
- 3D contributions → night-green dark view and green light view.
- Pixel profile → pixel mascot and compact system cards.
- GitAscii → terminal-dot avatar plus contribution snake.
- Readme Aura → glow, gradients, animated cursor, and luminous borders.

The goal is one original system UI, not six separate widgets pasted together.
