# Prompt Safety

## Goal

Help users create original AI video prompts from references without copying protected expression.

## Default transformation

Do not output:

- exact movie title as style instruction in final prompt
- actor likeness
- copyrighted character names
- franchise identifiers
- exact famous scene recreation
- dialogue copied from a work
- unique worldbuilding terms

Convert references into neutral cinematic language.

## Example conversions

| Risky input | Safer output |
|---|---|
| Make it like Parasite | class contrast, vertical spatial design, social thriller tension |
| Use David Fincher style | precise camera movement, low-saturation palette, psychological pressure |
| Like Squid Game but in an office | closed-rule competition, moral pressure, institutional satire |
| A Ma Dong-seok character | physically imposing middle-aged man with calm, grounded presence |

## Risk levels

- Low: genre, mood, camera, lighting, general narrative mechanics
- Medium: highly specific setting or plot mechanism
- High: named characters, famous scenes, direct plot clone, actor likeness
- Block/redirect: user asks to recreate copyrighted scene, character, or actor performance directly

## Prompt pack requirements

Every generated prompt pack should include:

1. Creative prompt
2. Shot list
3. Negative prompt
4. Derivative-risk notes
