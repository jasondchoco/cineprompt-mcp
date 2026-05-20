# Product Spec

## Working name

CinePrompt MCP

## User

Primary user: AI video creator, filmmaker, creative director, prompt designer, film student.

## Problem

Many AI video creators can operate tools but lack story development and cinematic reference translation skills. Searching for a synopsis is not enough. They need help turning references into original concepts, shot prompts, mood, rhythm, and visual language.

## Core value

Turn movie/TV references into usable AI video development material without copying the original work.

## Input examples

- `Parasite`
- `Bong Joon-ho`
- `David Fincher psychological thriller`
- `Korean revenge thriller, short-form vertical video`
- `A story engine similar to closed-space social pressure, but original`

## Output modules

1. Reference metadata
2. Neutral synopsis summary
3. Story engine
4. Character desire/conflict
5. Genre mechanics
6. Visual language
7. Camera/lighting/color/mise-en-scene keywords
8. AI video prompt: short
9. AI video prompt: long
10. Shot-by-shot prompt
11. Negative prompt
12. Derivative-risk warning

## v0.1 acceptance criteria

- User can search a movie title.
- User can search a person.
- User can get normalized title detail.
- User can ask for a cinematic reference pack.
- User can ask for an AI video prompt from a reference pack.
- Prompt output avoids direct imitation language by default.
- Tests pass without network access.
