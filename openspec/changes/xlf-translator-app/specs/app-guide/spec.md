# Spec Delta

## Purpose

Explains to a translator how the application expects to be used, so the rules it
enforces are understood before they are met.

## ADDED Requirements

### Requirement: Provide guidance on the workflow
The system SHALL provide documentation covering how a catalog is uploaded, what
the numbered tokens in a source stand for, why a unit cannot be left while its
tokens do not match, how work in progress is saved and resumed, and how a
finished catalog is exported.

#### Scenario: Guidance covers the enforced rules
- **WHEN** the documentation is requested
- **THEN** it explains the meaning of numbered tokens
- **AND** it explains why movement away from a mismatched unit is refused
- **AND** it explains how work in progress is saved and resumed

### Requirement: Reaching the guidance costs no work
The system SHALL make the documentation reachable at any point in a translation
session without discarding the session or any target entered in it.

#### Scenario: Session survives a visit to the guidance
- **WHEN** the documentation is requested at unit 40 of 60 with 39 targets entered
- **AND** the translation session is returned to
- **THEN** the position is unit 40
- **AND** all 39 targets are still present
