---
name: install-github-skill
description: Installs an Agent Skill from a public GitHub repository or GitHub tree URL for Pi, Claude Code, Codex, and other compatible agents. Prompts user to pick install target before install.
---

# Install GitHub Skill

## Usage

Run the installer with a GitHub URL (it will show a target picker):

```bash
./scripts/install-skill.py https://github.com/owner/repo
./scripts/install-skill.py https://github.com/owner/repo/tree/main/skills/my-skill
./scripts/install-skill.py https://github.com/owner/repo/blob/main/skills/my-skill/SKILL.md
```

Optional non-interactive mode:

```bash
./scripts/install-skill.py <github-url> --target pi-project
./scripts/install-skill.py <github-url> --path ~/.agents/skills
./scripts/install-skill.py <github-url> --yes
```

## Behavior

- Clones the GitHub repository
- Finds the skill directory containing `SKILL.md`
- Reads the skill name from `SKILL.md`
- Prompts user to choose target directory (Pi/Claude/Codex/.agents/custom path)
- Installs to `<target>/<name>`
- Replaces any existing skill with the same name

## Notes

- If the repository contains multiple skills, provide a GitHub tree URL to the exact skill directory.
- This command can install to project or global targets.
- This command is for public GitHub skills.
