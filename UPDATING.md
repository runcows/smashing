# Updating Steps
This document is mostly a reminder to me

## Aside from the normal minecraft updating things:
- Update `spyglass.json`
- Update `data/rc_smashing/dialog/about.json` with the new version number
- Consider updating `data/rc_smashing/function/init.mcfunction` score for `load.status`

## Packaging
### Datapack
Include:
- data
- pack.mcmeta
- pack.png
- LICENSE
- any overlays

File naming scheme is as follows:
`{mc_version_min}-{mc_version_max}_smashing_v{major}.{minor}.{patch}.zip`

Example:
`1.21.8-1.21.11_smashing_v1.1.0.zip`
