# Package manifest

This archive is ready to extract directly into the root of the `naveenkarasu` profile repository.

## Render-critical files included before any workflow runs

- `README.md`
- `assets/header.svg` (built from `assets/art/header.jpg`)
- dark + light terminal/profile/status/skills/project/stats/activity/certification/footer panels
- dark + light pixel mascot
- dark + light contribution-snake placeholders

## Generated/updated by GitHub Actions

- terminal avatar in dark + light mode
- live GitHub stats in dark + light mode
- recent activity in dark + light mode
- dark + light 3D contribution terrain (`assets/contributions*.svg`)
- dark + light contribution snake

## Workflow permission model

- default: `contents: read`
- build job: `contents: read`
- publish job only: `contents: write`
