---
name: pick-a-service
description: "Screen and rank service-business opportunities before validating one. Use when an individual, freelancer, consultant, or small team has decided to sell services and asks what service to offer, which service niche to pursue, whether candidate services reflect real buyer demand, or which candidates deserve testing. Apply a demand gate, anti-sycophancy rules, and a comparison of demand, competitive opening, and personal fit. Do not use for choosing jobs or industries, planning capital accumulation, selecting software vendors, experimentally validating one selected idea, or writing a business plan."
---

# Pick a Service

Choose at most two service opportunities worth validating. Screening narrows candidates; it does not
validate demand.

## Rules

- Separate **evidence**, **inference**, and **unknowns**. Do not complete missing evidence with a plausible
  story.
- Challenge the user's favorite as hard as the alternatives. Look for evidence that could disprove it.
- Treat popularity, market size, likes, survey interest, and AI relevance as weak signals unless they connect
  to a specific buyer, loss, budget, and buying behavior.
- Prefer observed behavior and current spending over stated intention.
- Avoid precise weighted scores unless the user provides calibrated weights. Do not use arithmetic to hide
  weak evidence.
- Do not invent fixed interview counts, conversion thresholds, or sample sizes. Leave experimental design to
  the validation stage unless the decision context supports a threshold.

## Workflow

### 1. Define comparable services

Capture the user's relevant skills and proof, buyer access, available time and capital, required income
continuity, and acceptable downside. Express each candidate as:

> Help [specific buyer] in [specific situation] achieve or avoid [measurable outcome] through [bounded service].

Split candidates with different buyers, problems, or offers. If no candidates exist, derive a small set from
the user's capabilities, access, constraints, and problems they have directly observed. Do not produce a long
list of fashionable industries.

### 2. Apply the demand gate

Check every candidate against the six criteria from the service-demand model:

1. **Specific customer:** Who experiences the problem, and in what situation?
2. **Explicit loss:** What money, time, opportunity, status, or risk is lost if it remains unsolved?
3. **Frequency or intensity:** Does it happen often enough, or carry enough cost when it happens?
4. **Existing budget:** What money, labor, tools, workaround, or management attention is already spent?
5. **Buying authority:** Who uses, decides, approves, and pays?
6. **Measurable result:** How will the buyer observe added revenue, lower cost, saved time, or reduced risk?

Classify each candidate:

- **Eliminate:** Contrary evidence or a known constraint breaks a load-bearing criterion.
- **Unknown:** Missing evidence prevents a responsible judgment. Name the cheapest fact-finding action.
- **Pass:** The demand case is coherent enough to compare, not validated.

Do not eliminate merely because evidence is missing, and do not pass merely because the story sounds
credible.

### 3. Check service viability

For candidates that pass or remain plausible, check:

- **Reachability:** Can likely buyers be identified and contacted without assuming an existing audience?
- **Deliverability:** Can the user credibly and legally produce the promised result?
- **Economics:** Could price exceed delivery and customer-acquisition costs with useful margin?
- **Repeatability:** Is there a route to repeat purchase, referrals, standardization, or follow-on work?
- **Downside:** Can it be tested without dangerous leverage, large inventory, high fixed overhead, or an
  irreversible loss of income?

Mark a viability failure as **eliminate** only when the constraint is known. Otherwise preserve it as an
explicit unknown for validation.

### 4. Compare survivors

Compare only candidates that survive the gates.

#### Demand

- Strength, frequency, urgency, and budget behind the buyer's loss
- Evidence of active search, current spending, workaround, or hiring
- Ease of demonstrating a valuable result

#### Competitive opening

- Direct competitors and indirect alternatives, including doing nothing
- A reachable gap in buyer segment, outcome, channel, speed, trust, or delivery model
- Switching cost and a concrete reason to choose this service
- Risk of easy copying or commoditization

Do not prefer low competition automatically; it can indicate low demand.

#### Personal fit

- Existing skill, experience, credibility, and proof
- Buyer access and speed to a credible first sales conversation
- Time to reach chargeable delivery quality
- Ability to start with low capital while preserving income continuity
- Willingness and capacity to repeat the work
- Scope to raise rates, retain clients, standardize delivery, or earn referrals

Rank only when evidence distinguishes the candidates. When evidence is too weak, recommend the next
fact-finding comparison instead of forcing a winner.

### 5. Select and hand off

Select at most two candidates. For each, report:

- Why it survived the demand and viability gates
- Why demand, competitive opening, and personal fit favor it
- The load-bearing assumption most likely to kill it
- Current evidence level:
  - **E0:** Speculation only
  - **E1:** Public signals, alternatives, or competitors
  - **E2:** Target-customer behavior, interviews, workflow, or current-spend evidence
  - **E3:** Trial order, deposit, preorder, or paid pilot
  - **E4:** Repeat purchases, referrals, or repeatable non-acquaintance sales
- The minimum next evidence needed

Describe E0-E2 candidates as **worth validating**, never validated. A high rank cannot compensate for weak
evidence.

When `testing-business-ideas` is available, hand off the buyer-problem-outcome-service statement, evidence,
unknowns, gate results, alternatives, load-bearing assumption, personal constraints, and minimum required
evidence. Ask it to design real-world experiments. If unavailable, produce the handoff artifact and state that
experimental validation remains outstanding.

## Output

Lead with the decision, then show:

1. A compact demand and viability gate table
2. Demand, competitive opening, and personal fit for survivors
3. Evidence, inference, unknowns, and E0-E4 level
4. The validation handoff

Stop at selection and handoff. Do not expand into career planning, branding, packaging, implementation, or a
business plan unless separately requested.
