# Spec Delta

## Purpose

Tracks where a translator is in a catalog, what state each unit is in, and when
moving on or finishing is permitted.

## ADDED Requirements

### Requirement: Derive the state of a unit
The system SHALL report a unit whose source holds only whitespace as
translated. For every other unit, the system SHALL report it untranslated when
its target is empty or holds only whitespace, invalid when its target holds
non-whitespace content and its placeholders do not match its source's, and
translated otherwise.

#### Scenario: Empty target
- **WHEN** a unit's target is empty
- **THEN** the unit is untranslated

#### Scenario: Whitespace-only target
- **WHEN** a unit whose source holds text has a target of three spaces
- **THEN** the unit is untranslated

#### Scenario: Target matching its source's placeholders
- **WHEN** a unit's target holds text and the same tokens as its source
- **THEN** the unit is translated

#### Scenario: Target missing a placeholder
- **WHEN** a unit's target holds text and omits a token its source holds
- **THEN** the unit is invalid

#### Scenario: A target identical to its source is valid
- **WHEN** a unit's target equals its source exactly
- **THEN** the unit is translated

### Requirement: Warn about auto-filled units
The system SHALL report, on opening a catalog, the ordinals of all units that
were auto-filled because their source holds only whitespace, and SHALL mark a
current unit as auto-filled while it is displayed. Clearing the target of an
auto-filled unit SHALL restore the auto-filled target.

#### Scenario: Auto-filled units are reported on open
- **WHEN** a catalog whose unit 30 has a whitespace-only source is opened
- **THEN** the opening report names ordinal 30 as auto-filled

#### Scenario: Current auto-filled unit is marked
- **WHEN** unit 30, auto-filled, becomes the current unit
- **THEN** the unit's description marks it as auto-filled

#### Scenario: Clearing an auto-filled target restores it
- **WHEN** the target of an auto-filled unit is emptied
- **THEN** its target equals its source again
- **AND** the unit is translated

### Requirement: Refuse to leave an invalid unit
The system SHALL refuse every movement away from the current unit while that
unit is invalid, and SHALL accompany the refusal with the placeholder difference
that caused it.

#### Scenario: Moving forward is refused
- **WHEN** movement to the next unit is requested while the current unit is invalid
- **THEN** the position does not change
- **AND** the refusal names the tokens that are missing, repeated or unknown

#### Scenario: Moving backward is refused
- **WHEN** movement to the previous unit is requested while the current unit is invalid
- **THEN** the position does not change

#### Scenario: Clearing the target releases the block
- **WHEN** the target of an invalid unit is emptied
- **THEN** the unit becomes untranslated
- **AND** movement to another unit is permitted

### Requirement: Move through every unit in document order
The system SHALL traverse all units of the catalog in document order, whatever
their state, and SHALL refuse movement beyond either end.

#### Scenario: Forward movement
- **WHEN** movement to the next unit is requested at position 7 of 60 with the current unit not invalid
- **THEN** the position becomes 8

#### Scenario: Already translated units are not skipped
- **WHEN** movement to the next unit is requested and the following unit is already translated
- **THEN** the position moves to that unit
- **AND** its existing target is offered for editing

#### Scenario: End of catalog
- **WHEN** movement to the next unit is requested at the last position
- **THEN** the position does not change

### Requirement: Report the absolute position
The system SHALL report the current position as its ordinal among all units of
the catalog, counting from 1, together with the total number of units.

#### Scenario: Position report
- **WHEN** the seventh unit of a 60-unit catalog is current
- **THEN** the reported position is 7 and the reported total is 60

### Requirement: Move directly to a chosen unit
The system SHALL move to any unit named by its ordinal, subject to the same
refusal that governs stepwise movement, and SHALL refuse an ordinal outside the
catalog.

#### Scenario: Jump to an ordinal
- **WHEN** movement to unit 52 of 60 is requested from unit 7 and unit 7 is not invalid
- **THEN** the position becomes 52

#### Scenario: Ordinal out of range
- **WHEN** movement to unit 500 of a 60-unit catalog is requested
- **THEN** the position does not change

### Requirement: Resume at the first unresolved unit
On opening a catalog, the system SHALL position at the first unit that is
untranslated or invalid, and at the first unit when every unit is translated.

#### Scenario: Partial catalog
- **WHEN** a catalog whose first 30 units are translated and whose 31st is untranslated is opened
- **THEN** the position is 31

#### Scenario: Auto-filled units do not stop the resume
- **WHEN** a catalog whose units 1 to 29 are translated, whose unit 30 is auto-filled and whose unit 31 is untranslated is opened
- **THEN** the position is 31

#### Scenario: Catalog carrying an imported invalid unit
- **WHEN** a catalog whose units are all translated except an invalid unit at position 44 is opened
- **THEN** the position is 44

### Requirement: Report completion
The system SHALL report a catalog complete only when every unit is translated,
and SHALL otherwise report the ordinals of all untranslated and invalid units.

#### Scenario: Complete
- **WHEN** every unit of a catalog is translated
- **THEN** the catalog is reported complete

#### Scenario: Incomplete with imported damage and gaps
- **WHEN** a catalog holds untranslated units at ordinals 31 and 38 and invalid units at ordinals 44 and 52
- **THEN** the catalog is not reported complete
- **AND** the report names ordinals 31, 38, 44 and 52

### Requirement: Copy a source into its target
The system SHALL offer to replace the current unit's target with its source,
copying every character including leading and trailing whitespace, escaped
markup and every placeholder token.

#### Scenario: Copying a source carrying placeholders
- **WHEN** the source of a unit masked as `{1}limited functionality{2}` is copied into its target
- **THEN** the target becomes `{1}limited functionality{2}`
- **AND** the unit is translated

#### Scenario: Copying preserves whitespace
- **WHEN** a source beginning with two non-breaking spaces is copied into its target
- **THEN** the target begins with those two characters
