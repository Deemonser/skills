---
name: review-reachable-security
description: "Review or change code at security-sensitive boundaries using reachable-risk analysis. Use for authentication, authorization, tenant or data isolation, untrusted input, sensitive data, irreversible operations, exposed resource consumption, or explicit security review. Do not use for ordinary code with no credible security boundary or threat decision."
---

# Review Reachable Security

- Optimize for reachable risk reduced per unit of complexity, not security code, scenario count, or
  theoretical coverage. Identify the asset, threat source, realistic attack path, impact, and
  verifiable result before adding a control.
- Prioritize authentication and authorization, tenant and data isolation, untrusted input,
  sensitive data, irreversible operations, and externally reachable resource consumption.
- Put controls at the trust boundary that owns the invariant. Establish an internal invariant once
  at the unique entry boundary instead of repeating defenses throughout trusted code.
- Prefer standard language, framework, and platform mechanisms. Do not invent cryptography or
  duplicate existing identity, policy, validation, rate-limit, or audit infrastructure.
- Validate the highest-risk credible paths first. Add focused regression coverage when it proves a
  durable security property; avoid low-value scenario multiplication.
- Reject speculative hardening that has no concrete asset or reachable path. Record assumptions and
  coverage limits instead of encoding theoretical threats as permanent complexity.
- When control complexity may exceed expected risk reduction, surface the tradeoff before
  implementation. Do not let minor checks crowd out major findings or protections.
