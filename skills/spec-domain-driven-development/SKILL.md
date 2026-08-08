---
name: spec-domain-driven-development
description: Establish or realign a non-trivial project or feature with Specification-Driven Development (SDD), proportionate Domain-Driven Design (DDD), and domain-core-to-adapter implementation. Use only when the user explicitly invokes $spec-domain-driven-development.
---

# Spec and Domain Driven Development

## Purpose

Create a stable path from intent to implementation:

1. Define observable behavior and constraints with SDD.
2. Derive only the domain model the problem actually needs.
3. Fix ownership, invariants, boundaries, and dependency direction.
4. Implement coherent vertical slices from the domain core toward external adapters.

Optimize for alignment and traceability, not documentation volume or architectural ceremony.

## Operating rules

- Treat the specification as the source of truth for intended behavior and the domain model as the
  source of truth for business meaning and ownership.
- Scale artifacts to decision complexity. For a trivial or isolated change, stop after a compact
  behavior contract; do not create durable SDD or DDD documents when they add no coordination value.
- Do not begin broad implementation while unresolved decisions could still change core invariants,
  context boundaries, external contracts, or data ownership.
- Permit a narrow discovery spike when evidence is missing. Mark it as disposable; do not let spike
  code become production architecture without review.
- Treat a design baseline as accepted only when the user approves it or an authoritative repository
  artifact already establishes it. Once accepted, update it deliberately and assess downstream
  impact before or with the implementation change.
- Preserve existing project conventions and useful architecture. Do not rename concepts or rebuild
  boundaries merely to make the repository look more like a DDD example.

An analysis or design request permits inspection and proposed artifacts, not repository edits. Edit
only when the user asks to create, update, apply, implement, or fix.

## Workflow

### 1. Establish the current system

Read applicable instructions, specifications, architecture documents, code structure, schemas,
external contracts, and existing terminology. For an existing system, distinguish:

- **As-is:** behavior and boundaries that exist now.
- **To-be:** intentional changes required by the current request.

Do not design a replacement model before understanding current ownership, coupling, compatibility
constraints, and migration cost.

### 2. Build the specification first

Define only what is needed to make implementation decisions:

- Problem, goals, non-goals, actors, and scope.
- Use cases or scenarios with observable outcomes.
- Business rules, invariants, state transitions, and failure behavior.
- External contracts, data constraints, compatibility needs, and material quality attributes.
- Acceptance criteria, open questions, assumptions, and deferred decisions.

Write requirements as behavior, not as a preselected class, database, framework, or endpoint design.
Resolve questions that could change the domain model or public contract; leave lower-level choices to
implementation when several options remain valid.

### 3. Choose the proportionate DDD level

Classify the feature or project before introducing DDD constructs:

- **No tactical DDD:** Simple CRUD, thin adapters, presentation-only work, one-off automation, or
  behavior dominated by an external system. Define clear module ownership and contracts instead.
- **Light DDD:** A coherent domain with meaningful vocabulary, rules, lifecycles, or invariants but
  no strong need for multiple bounded contexts. Model the core concepts and consistency boundary.
- **Strategic and tactical DDD:** Multiple business capabilities, conflicting meanings, independent
  lifecycles, complex policies, or different ownership and integration boundaries. Define bounded
  contexts and their relationships before tactical models.

Base the choice on domain complexity, not repository size or a desire for more layers. Record the
decision and its evidence. Do not invent aggregates, repositories, services, or events without a rule
or boundary that needs them.

### 4. Derive the domain model

Build from the specification:

1. Establish a small ubiquitous-language glossary and resolve ambiguous terms.
2. Identify business capabilities, bounded contexts when justified, and context relationships.
3. Assign each invariant and state transition to one owning boundary.
4. Model entities, value objects, aggregates, domain services, policies, and domain events only where
   they express required behavior.
5. Define aggregate and transaction boundaries by consistency needs; do not mirror database tables.
6. Expose cross-boundary interaction through explicit contracts and translations. Do not share
   internal models merely for convenience.

Prefer behavior-rich domain concepts over data containers with business rules scattered across
controllers, UI, jobs, or infrastructure code.

### 5. Fix the architecture boundary

Use the following dependency direction unless the repository has an equivalent established model:

- **Domain:** business meaning, rules, invariants, and state transitions; no framework or
  infrastructure dependency.
- **Application:** use-case orchestration, authorization decisions, transactions, and domain ports.
- **Adapters and infrastructure:** persistence, messaging, remote services, files, clocks, and other
  technical implementations of boundary contracts.
- **Delivery:** API, CLI, UI, scheduled jobs, and transport-specific mapping.

Place contracts at the boundary that owns the need. Keep external schemas and persistence models out
of the domain through explicit mapping when their semantics differ.

### 6. Plan implementation from the core outward

Divide work into end-to-end vertical slices. For each slice:

1. Name the specification scenario or acceptance criterion it satisfies.
2. Implement or adjust the owning domain behavior and invariants.
3. Add application orchestration and boundary contracts.
4. Add the minimum adapters and delivery path required to exercise the behavior.
5. Verify the acceptance criterion with evidence proportional to uncertainty and risk.

Start with a representative slice that tests the riskiest boundary or assumption. Do not build every
layer, repository, event, or abstraction in advance of behavior that uses it.

### 7. Keep artifacts and AGENTS.md proportional

Follow existing documentation locations and formats. Update an authoritative artifact instead of
creating a competing specification. When the repository has no convention, keep specifications and
domain design in clearly named project documentation rather than embedding them in `AGENTS.md`.

Put only durable execution constraints and pointers in `AGENTS.md`, such as:

- Treat the accepted specification and domain model as authoritative.
- Keep business rules in their owning domain boundary and dependencies directed inward.
- Update design artifacts when behavior, invariants, ownership, or public contracts change.

Do not copy scenarios, glossaries, aggregate catalogs, diagrams, or implementation plans into
`AGENTS.md`.

## Completion check

Before presenting or applying the design, confirm that:

- Goals, non-goals, observable scenarios, invariants, and acceptance criteria agree.
- Material ambiguity is resolved or explicitly recorded with its impact.
- The chosen DDD level is justified and avoids both anemic modeling and unnecessary ceremony.
- Every important rule has one owner and every cross-boundary dependency has a direction.
- The first implementation slices trace back to the specification and reach a usable boundary.
- Proposed `AGENTS.md` text is compact, durable, and points to detailed artifacts instead of
  duplicating them.

## Output

- **Design only:** Lead with the recommended SDD/DDD level, then present the specification baseline,
  domain boundaries, unresolved decisions, and an ordered implementation slice plan.
- **Apply:** Create or update the authoritative project artifacts and only the minimum durable
  `AGENTS.md` rules requested. Do not implement product code unless the user also asks for it.
- **Review existing design:** Complete a system-wide coverage pass, group symptoms by root cause, and
  return material gaps together rather than incrementally.
