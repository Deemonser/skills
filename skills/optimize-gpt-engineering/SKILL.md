---
name: optimize-gpt-engineering
description: "Directly apply a canonical, minimally adapted AGENTS.md policy that optimizes GPT coding-agent behavior across proactive token-efficient commander-led delegation, strict testing restraint, and one-pass architecture-first review with risk-proportionate security; also align Codex subagent defaults. Explicit invocation of $optimize-gpt-engineering authorizes the relevant local edits by default; remain read-only only when the user explicitly forbids changes."
---

# Optimize GPT Engineering Behavior

## Purpose

Install or audit one compact policy that corrects three recurring GPT engineering biases:

1. weak or indiscriminate subagent orchestration;
2. testing for its own sake instead of risk reduction;
3. fragmented local review and expansive security work that are detached from whole-system
   consistency and reachable risk.

Treat all three pillars as required coverage. Align Codex subagent defaults as supporting runtime
configuration for the orchestration pillar. Treat comprehensive architecture review and
risk-proportionate security as two mandatory parts of the review pillar.

Use the canonical policy in `references/agents-md-policy-template.md` as the source of truth. This is
a template-driven installation, not an invitation to generate a new policy from general guidance.

## Execution authority

- Treat explicit invocation as authorization to inspect and directly update the applicable
  `AGENTS.md` instruction chain and effective Codex subagent defaults. Do not stop at suggestions or
  ask for confirmation before safe, in-scope local edits.
- Remain read-only only when the user explicitly says not to edit, to provide advice only, or to show
  a proposed patch. The word "audit" alone does not make the request read-only.
- Respect explicit scope limits. Otherwise, align all three behavior pillars in the governing
  project `AGENTS.md` and align the user-level subagent defaults. If no suitable project
  `AGENTS.md` exists, create one at the repository root.

## Workflow

1. Read `references/agents-md-policy-template.md` completely before inspecting or editing project
   instructions.
2. Read the complete active `AGENTS.md` chain, nested overrides, repository conventions, and
   effective Codex subagent configuration.
3. Compare the effective instructions against the canonical template clause by clause. Generic
   phrases such as "use subagents", "test thoroughly", "review carefully", or "follow security best
   practices" do not count as equivalent coverage.
4. Install the template as one coherent policy. Merge genuine equivalents and make only the minimal
   project adaptations allowed by the template; do not regenerate or selectively summarize it.
5. Align worker defaults without changing the primary model. Apply all safe in-scope edits before
   responding.
6. Run the counterexample check and reread the entire effective instruction chain for missing
   clauses, weakened polarity, contradictions, repetition, and unintended scope.

## Template fidelity

- Use the canonical wording verbatim by default. Translate or adapt only when required by the
  project's language, terminology, scope, existing equivalent rules, or a concrete repository
  requirement.
- Preserve every normative decision, default, exception threshold, and ownership boundary. Never
  replace a hard rule with advice such as "consider", "when useful", or "where appropriate".
- Require a concrete observed project reason for each semantic deviation. Style preference,
  shortening, or the claim that the model already knows the behavior is not a reason.
- Merge duplicates and adjust headings or placement to fit the active instruction chain, but keep
  the canonical policy recognizable and complete. Add project-specific rules only when they do not
  weaken or obscure it.

## Canonical AGENTS.md policy

Read and apply [the canonical policy template](references/agents-md-policy-template.md). Its policy
block is the default content for `AGENTS.md`, not an example. A pillar is adequate only when every
corresponding template clause remains enforceable in the effective instruction chain.

## Codex subagent defaults

Locate the effective user Codex config: `$CODEX_HOME/config.toml` when `CODEX_HOME` is set, otherwise
`~/.codex/config.toml`. Preserve all unrelated settings and ensure its `[agents]` table contains:

```toml
[agents]
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "xhigh"
```

- Replace only conflicting values; do not create a second `[agents]` table or change the primary
  agent's `model` or `model_reasoning_effort`.
- Verify that the active primary model is suitable for the commander role and more capable than the
  default worker for the decisions it retains. Report a mismatch instead of silently changing the
  user's primary-model selection.
- Check project-scoped Codex configuration and custom agents for overrides. Align them only when the
  request includes that scope; otherwise report that they can supersede the user default.
- Do not silently substitute another model or effort if the current Codex runtime rejects either
  value. Report the incompatibility and the effective fallback.
- After changing Codex configuration, state that existing sessions may retain their prior settings
  and Codex should be restarted before relying on the new default.

## Counterexample check

Before finalizing a proposed rule set, verify that it produces the intended decision in each case:

- The commander directly completes trivial work cheaper than handoff, but delegates bounded
  discovery, analysis, implementation, or validation without requiring the work to be large or
  dependency-free. For architecture-critical work, it retains the decision while delegating
  separable evidence or execution.
- Obvious workstreams are dispatched before the commander duplicates their exploration. Sequencing,
  setup, and shared files lead to explicit prerequisites or ownership boundaries rather than a
  blanket refusal to delegate; redundant agents are used only for risk-justified confirmation.
- A worker returns concise artifacts and evidence. The commander reviews and integrates them in
  proportion to risk rather than either accepting a cross-cutting decision or redoing settled work.
- An unoverridden subagent resolves to `gpt-5.6-luna` with `xhigh` effort after configuration reload;
  an explicit or project override is detected rather than mistaken for the default.
- A simple function whose result is evident from inspection gets no test. Even a change at a named
  high-risk boundary gets a test only when a plausible material failure cannot be settled more
  cheaply; a narrow change does not trigger a broad suite without evidence of wider coupling.
- A repository-wide review remains commander-executed: the commander maps the relevant system,
  completes the primary breadth and cross-component pass before ordinary reporting or patching, and
  returns material findings together under architectural root causes. Workers may collect bounded
  evidence or independently verify a suspected issue, but their output neither replaces commander
  review nor counts as coverage before commander inspection and integration.
- A security review prioritizes reachable high-impact boundaries. New controls require a concrete
  asset, threat source, realistic attack path, and verifiable result; low-value theoretical checks
  do not expand implementation or obscure major risk.

If the proposed text cannot distinguish both sides of any case, it is too compressed or too vague.
If it restates the cases or the workflow verbatim in `AGENTS.md`, it is too verbose.

## Output

- By default, make the necessary edits before responding. Lead with what is now effective, then state
  the changed surfaces and coverage of all three pillars, including both review dimensions,
  followed by worker defaults, detected overrides, and whether a restart is needed.
- For an explicitly read-only request, show one coherent patch covering every material gap rather
  than several incremental alternatives.
- Do not ask the user to reconfirm safe edits already authorized by explicit invocation.
- Do not pad the result with compliant areas, minor observations, or a copied policy template.
