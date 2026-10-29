# Spec Delta

## Purpose

Hides Angular's inline placeholder elements behind short numbered tokens while a
human edits a translation, and restores them exactly afterwards, so markup
cannot be corrupted by typing.

## ADDED Requirements

### Requirement: Mask inline placeholders as numbered tokens
The system SHALL replace each inline placeholder element in a unit's content
with a token of the form `{n}`, numbered from 1 in document order, and SHALL
leave all other characters unchanged.

#### Scenario: A paired placeholder becomes two tokens
- **WHEN** content holding an opening and a closing bold placeholder around the words `limited functionality` is masked
- **THEN** the masked form is `{1}limited functionality{2}`

#### Scenario: Text without placeholders is unchanged
- **WHEN** content holding no placeholder element is masked
- **THEN** the masked form equals the original content character for character

#### Scenario: Escaped markup is not a placeholder
- **WHEN** content holding the literal text `<p><b>Tip</b></p>` and no placeholder element is masked
- **THEN** the masked form contains no token

### Requirement: Unmasking inverts masking
For every unit in a catalog, unmasking the masked form of its content SHALL
reproduce that content exactly, including placeholder attributes and their
order.

#### Scenario: Round trip over the fixture catalogs
- **WHEN** every source and target of every fixture catalog is masked and then unmasked
- **THEN** each result equals the original content exactly

#### Scenario: Placeholder attributes survive
- **WHEN** a placeholder declaring an identifier, a content type and equivalent text is masked and unmasked
- **THEN** the restored placeholder declares the same identifier, content type and equivalent text

### Requirement: Tokens may be reordered
The system SHALL accept a target whose tokens appear in an order different from
the source's, and SHALL restore each token to the placeholder it names.

#### Scenario: Reversed tokens
- **WHEN** a target masked as `{2}word{1}` is unmasked against a source whose tokens are `{1}` and `{2}`
- **THEN** the restored target holds the second placeholder before the first

### Requirement: Compare the placeholders of a source and a target
The system SHALL report a target as matching its source when the two contain the
same tokens with the same multiplicities, and SHALL otherwise report the
difference, naming each token that is missing, repeated or unknown together with
the markup it stands for.

#### Scenario: A deleted token is reported
- **WHEN** a target holding only `{1}` is compared against a source holding `{1}` and `{2}`
- **THEN** the comparison fails
- **AND** the report names `{2}` and the markup it stands for

#### Scenario: A repeated token is reported
- **WHEN** a target holding `{1}` twice is compared against a source holding `{1}` once
- **THEN** the comparison fails
- **AND** the report names `{1}` as repeated

#### Scenario: An unknown token is reported
- **WHEN** a target holding `{9}` is compared against a source holding two tokens
- **THEN** the comparison fails
- **AND** the report names `{9}` as unknown

#### Scenario: Matching placeholders pass
- **WHEN** a target holding `{2}` then `{1}` is compared against a source holding `{1}` and `{2}`
- **THEN** the comparison succeeds

### Requirement: Literal braces survive masking
The system SHALL distinguish a brace that is part of a unit's text from a brace
that delimits a token, so that content containing literal braces round-trips
unchanged.

#### Scenario: Literal braces in a source
- **WHEN** content containing the literal text `{1}` and no placeholder element is masked and then unmasked
- **THEN** the result equals the original content
- **AND** the comparison against that source reports no token
