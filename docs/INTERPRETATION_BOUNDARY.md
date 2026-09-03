# Interpretation Boundary

## Purpose

VariantPriorX demonstrates transparent germline variant prioritization using multiple evidence sources.

It is designed for bioinformatics research, education, workflow engineering, portfolio demonstration, and variant evidence exploration.

## What VariantPriorX Does

VariantPriorX combines:

- Functional consequence evidence from Ensembl VEP.
- Curated clinical evidence from ClinVar.
- Population-frequency evidence from gnomAD.

These evidence layers contribute to a transparent prioritization score used to rank variants for further investigation.

## What VariantPriorX Does Not Do

VariantPriorX does not:

- Diagnose disease.
- Determine treatment.
- Replace professional clinical interpretation.
- Independently classify variants as pathogenic or benign.
- Implement the complete ACMG/AMP classification framework.
- Establish disease causality.

## HG002

HG002 is used as a benchmark/reference genome.

VariantPriorX does not treat HG002 as a clinical patient.

## Prioritization Score

A higher VariantPriorX score indicates that a variant satisfies more of the implemented prioritization criteria.

It does not mean that the variant has been clinically classified as pathogenic.

## Intended Use

Outputs are intended for research and educational use and require appropriate expert review before any potential clinical interpretation.
