# AGENTS.md

## Project
This repository contains local, project-scoped Pi skills.

## Session Start
- Activate the `git-commit` and `caveman` skills at session start.

## Conventions
- Keep skills in `.pi/skills/` only.
- Add each skill as its own directory with a `SKILL.md` file.
- Keep skill descriptions specific and concise.
- Store helper scripts and references inside the skill directory.

## Workflow
- Use `read` before editing files.
- Use `bash` for discovery and git checks.
- Make minimal, targeted edits.
- Avoid adding global or shared skills outside this repo.

## Git
- Use conventional commits.
- Do not commit secrets or local IDE state.
- `.idea/` should stay ignored.
