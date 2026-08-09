# Minimal AGENTS.md Router

Use this only when the user explicitly requests persistent project routing. Merge the following hook
into the governing project `AGENTS.md`, preserving unrelated instructions and avoiding duplicates:

```markdown
## Engineering workflow

- For code implementation, debugging, refactoring, testing strategy, multi-agent engineering,
  architecture or code review, or security-sensitive changes, apply `$optimize-gpt-engineering` and
  load only its task-relevant references.
```

Do not install any other policy from this skill into `AGENTS.md`. Do not create nested overrides or
edit Codex model configuration unless the user separately requests it.
