# Spec Delta

## Purpose

Governs how a catalog enters the application and how it leaves it, including
upload limits, what the exported files are named and when an export is
permitted.

## ADDED Requirements

### Requirement: Accept a catalog for translation
The system SHALL accept an uploaded XLIFF 1.2 document and begin a translation
session from it. A document that is refused SHALL leave no session open, and the
refusal SHALL be reported to the user.

#### Scenario: Accepted upload
- **WHEN** a well-formed XLIFF 1.2 document declaring a source language and carrying 60 units is uploaded
- **THEN** a session opens over those 60 units

#### Scenario: Refused upload
- **WHEN** a document that is not XLIFF 1.2 is uploaded
- **THEN** no session opens
- **AND** the reported reason names what was expected

### Requirement: Limit the size of an upload
The system SHALL refuse, before parsing it, an uploaded document larger than
4 MiB (4,194,304 bytes), and the refusal SHALL state both the limit and the
size received.

#### Scenario: Upload at the limit
- **WHEN** a valid catalog of exactly 4,194,304 bytes is uploaded
- **THEN** a session opens

#### Scenario: Upload over the limit
- **WHEN** a document of 4,194,305 bytes is uploaded
- **THEN** no session opens
- **AND** the refusal states the 4 MiB limit and the size received

### Requirement: Establish the target language
The system SHALL require the translator to choose a target language through the
language form before translation begins when the uploaded document declares
none, and SHALL adopt the declared target language without asking when the
document declares one, as a re-uploaded draft does. The controls and validation
of the language form are deferred; see note N3 in design.md.

#### Scenario: Fresh catalog
- **WHEN** a catalog declaring no target language is accepted
- **THEN** a target language is required before any unit can be translated

#### Scenario: Language chosen in the form
- **WHEN** target language `en-GB` is submitted in the language form for a fresh catalog
- **THEN** the session's target language is `en-GB`

#### Scenario: Re-uploaded draft
- **WHEN** a catalog declaring target language `en-GB` is accepted
- **THEN** the session adopts `en-GB` without asking

### Requirement: Export work in progress at any time
The system SHALL export the current state of the catalog on request, whatever
the state of its units, including while units are untranslated or invalid. The
exported document SHALL declare both the source and the target language.

#### Scenario: Draft while a unit is invalid
- **WHEN** an export of work in progress is requested while the current unit is invalid
- **THEN** the export is produced

#### Scenario: Draft carries the work done so far
- **WHEN** an export of work in progress is requested for a fresh 60-unit catalog after 10 units are translated, one of the remaining units being auto-filled
- **THEN** the exported document carries 11 target elements

#### Scenario: Draft declares both languages
- **WHEN** an export of work in progress is requested for a catalog with source language `es` and target language `en-GB`
- **THEN** the exported document declares source language `es` and target language `en-GB`

### Requirement: Name the exported artifacts
The system SHALL name an export of work in progress
`<stem>.<target-language>.draft.xlf` and a final export
`<stem>.<target-language>.xlf`, where the stem is that of the uploaded document.

#### Scenario: Draft name
- **WHEN** work in progress on `messages.xlf` for target language `en-GB` is exported
- **THEN** the exported artifact is named `messages.en-GB.draft.xlf`

#### Scenario: Final name
- **WHEN** a completed catalog from `messages.xlf` for target language `en-GB` is exported
- **THEN** the exported artifact is named `messages.en-GB.xlf`

### Requirement: Refuse a final export of an incomplete catalog
The system SHALL refuse a final export while any unit is untranslated or
invalid, and SHALL report the ordinal of every such unit so each can be reached
directly. An export of work in progress is a separate operation and is not
subject to this refusal.

#### Scenario: Final export refused for damage
- **WHEN** a final export is requested for a catalog holding invalid units at ordinals 44 and 52
- **THEN** no final export is produced
- **AND** ordinals 44 and 52 are reported as needing repair

#### Scenario: Final export refused for gaps
- **WHEN** a final export is requested for a catalog whose units are all translated except an untranslated unit at ordinal 31
- **THEN** no final export is produced
- **AND** ordinal 31 is reported as needing translation

#### Scenario: Final export permitted
- **WHEN** a final export is requested for a catalog whose units are all translated
- **THEN** the final export is produced

### Requirement: Start over only after exporting
The system SHALL offer to begin a new session from a new upload only after a
final export of the current catalog has been requested.

#### Scenario: Offer withheld
- **WHEN** a catalog is complete and no final export has been requested
- **THEN** beginning a new session is not offered

#### Scenario: Offer available
- **WHEN** a final export has been requested
- **THEN** beginning a new session is offered
