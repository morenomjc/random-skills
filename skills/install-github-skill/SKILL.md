---
name: install-github-skill
description: Installs a pi skill from a public GitHub repository or GitHub tree URL into this project's local .pi/skills directory. Use when the user provides a GitHub URL for a skill.
---

# Install GitHub Skill

## Usage

Run the installer with a GitHub URL:

```bash
./scripts/install-skill.py https://github.com/owner/repo
./scripts/install-skill.py https://github.com/owner/repo/tree/main/skills/my-skill
./scripts/install-skill.py https://github.com/owner/repo/blob/main/skills/my-skill/SKILL.md
```

## Behavior

- Clones the GitHub repository
- Finds the skill directory containing `SKILL.md`
- Reads the skill name from `SKILL.md`
- Installs it to this repo's `.pi/skills/<name>`
- Replaces any existing skill with the same name

## Notes

- If the repository contains multiple skills, provide a GitHub tree URL to the exact skill directory.
- This command is for public GitHub skills.
