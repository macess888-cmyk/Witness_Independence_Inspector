# Witness Independence Inspector

Status: DELTA-005 bounded experiment.

## Question

Can multiple receipts, reports, or nominal witnesses be distinguished
from genuinely independent corroborating sources?

Core relation:

receipt_count > 1

does not establish

independent_witness_count > 1

## Purpose

Inspect source-origin relationships without determining claim truth,
authority, admissibility, or execution permission.

## Candidate distinctions

multiple receipts != independent corroboration

multiple witnesses != independent origins

shared derived dataset != independent source

correlated evidence != invalid evidence

independence established != claim truth

independence established != authority

## Bounded candidate states

- INDEPENDENCE_ESTABLISHED
- CORRELATED_SOURCE
- INDEPENDENCE_NOT_ESTABLISHED
- HOLD

## Governance boundaries

This inspector is observer-only.

It does not discard evidence merely because evidence is correlated.

It does not determine whether a claim is true.

It does not determine whether evidence is legally or institutionally admissible.

It does not grant execution, promotion, deployment, or decision authority.

UNKNOWN -> HOLD.