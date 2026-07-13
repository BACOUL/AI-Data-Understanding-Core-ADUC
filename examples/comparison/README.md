# Semantic comparison example

This example contains two differently shaped sources:

```text
French source: temp_moteur
US source:     motor_temp
```

Their profiles map both fields to:

```text
https://example.org/quantity/MotorTemperature
```

with `skos:exactMatch`. The French mapping is reviewed and the US mapping is publisher-canonical, so Gate 5 classifies the pair as `comparable`.

Run:

```bash
python tools/aduc_compare.py \
  examples/comparison/fr/profile.aduc.json \
  examples/comparison/us/profile.aduc.json \
  --trusted-authority-b https://example.org/id/us-data-authority
```

The source records also contain different units, timestamps and equipment identifiers. Gate 5 intentionally reports these dimensions as `notEvaluated`; it does not guess unit conversion, temporal equivalence or entity identity from names or values.
