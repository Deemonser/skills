# Reachable-Risk Security

- Maximize reachable risk reduced per unit of complexity, not security code, scenario count, or
  theoretical coverage. Add logic only for a concrete asset, threat source, realistic attack path,
  and verifiable result; otherwise record an assumption or coverage note.
- Prioritize authentication and authorization, data isolation, untrusted input, sensitive data,
  irreversible operations, and unbounded resource entry points.
- Concentrate controls at trust boundaries. Establish internal invariants once at the unique entry
  boundary and add a focused test only when the validation gate is met; do not repeat defenses.
- Prefer standard language, framework, and platform mechanisms. Do not create custom cryptography or
  duplicate security infrastructure.
- When complexity may exceed expected risk reduction, report the tradeoff before implementation. Do
  not let low-risk checks crowd out major findings or protections.
