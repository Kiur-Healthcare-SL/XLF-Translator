# Spec Delta

## Purpose

Governs how a catalog enters the application and how it leaves it, including
what the exported files are named and when an export is permitted.

## ADDED Requirements

### Requirement: Accept a catalog for translation
The system SHALL accept an uploaded XLIFF 1.2 document and begin a translation
session from it. A document that is refused SHALL leave no session open, and the
refusal SHALL be reported to the user.

#### Scenario: Accepted upload
- **WHEN** a well-formed XLIFF 1.2 document carrying 360 units is uploaded
- **THEN** a session opens over those 360 units

#### Scenario: Refused upload
- **WHEN** a document that is not XLIFF 1.2 is uploaded
- **THEN** no session opens
- **AND** the reported reason names what was expected

### Requirement: Establish the target language
The system SHALL require a target language before translation begins when the
uploaded document declares none, and SHALL adopt the declared target language
without asking when the document carries one.

#### Scenario: Fresh catalog
- **WHEN** a catalog declaring no target language is accepted
- **THEN** a target language is required before any unit can be translated

#### Scenario: Resumed catalog
- **WHEN** a catalog declaring target language `en-GB` is accepted
- **THEN** the session adopts `en-GB` without asking

### Requirement: Export work in progress at any time
The system SHALL export the current state of the catalog on request, whatever
the state of its units, including while a unit is invalid.

#### Scenario: Draft while a unit is invalid
- **WHEN** an export of work in progress is requested while the current unit is invalid
- **THEN** the export is produced

#### Scenario: Draft carries the work done so far
- **WHEN** an export of work in progress is requested after 40 of 360 units are translated
- **THEN** the exported document carries 40 target elements

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

### Requirement: Refuse a final export of a damaged catalog
The system SHALL refuse a final export while any unit is invalid, and SHALL
report the ordinal of every such unit so each can be reached directly.

#### Scenario: Final export refused
- **WHEN** a final export is requested for a catalog holding invalid units at ordinals 112 and 203
- **THEN** no final export is produced
- **AND** ordinals 112 and 203 are reported as needing repair

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
