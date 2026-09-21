# Spec Delta

## Purpose

Reads, classifies and writes Angular XLIFF 1.2 message catalogs, preserving
every byte of source content that the application does not deliberately change.

## ADDED Requirements

### Requirement: Parse an XLIFF 1.2 catalog
The system SHALL read an XLIFF 1.2 document into an ordered collection of
translation units, preserving each unit's identifier, document order, source
content including inline placeholder elements, and all leading and trailing
whitespace.

#### Scenario: Catalog with sources only
- **WHEN** a document containing 360 trans-units, each with a source and no target, is parsed
- **THEN** the result contains 360 units in document order
- **AND** each unit reports the identifier declared in the document

#### Scenario: Whitespace is preserved
- **WHEN** a unit whose source is two non-breaking spaces is parsed
- **THEN** the parsed source equals those two characters exactly, neither trimmed nor normalised

#### Scenario: Escaped markup is text
- **WHEN** a unit whose source contains the characters `&lt;p&gt;` is parsed
- **THEN** the parsed source contains the literal text `<p>` and no element node

### Requirement: Reject documents that cannot be translated
The system SHALL refuse a document that is not well-formed XML, is not XLIFF
version 1.2, declares no file element, contains no translation unit, or
contains duplicate unit identifiers. Each refusal SHALL state what was expected
and what was found.

#### Scenario: Not XML
- **WHEN** a file whose content is not well-formed XML is submitted
- **THEN** the document is refused
- **AND** the refusal states that well-formed XML was expected

#### Scenario: Wrong XLIFF version
- **WHEN** a document declaring version 2.0 is submitted
- **THEN** the document is refused
- **AND** the refusal names both the expected version 1.2 and the version found

#### Scenario: Duplicate identifiers
- **WHEN** a document contains two trans-units sharing one identifier
- **THEN** the document is refused
- **AND** the refusal names the duplicated identifier

### Requirement: Classify a catalog by its content
The system SHALL classify a parsed catalog as fresh when no unit carries a
target, completed when every unit carries a target and no unit is invalid, and
partial otherwise. Classification SHALL depend only on document content, never
on the file's name.

#### Scenario: Fresh catalog
- **WHEN** a catalog whose units all lack targets is classified
- **THEN** the classification is fresh

#### Scenario: Partial catalog
- **WHEN** a catalog of 360 units in which 359 carry targets is classified
- **THEN** the classification is partial

#### Scenario: A draft named as a draft is judged by content
- **WHEN** a catalog whose every unit carries a valid target is classified
- **THEN** the classification is completed regardless of the file name it arrived under

### Requirement: Serialise a catalog to XLIFF 1.2
The system SHALL write a catalog as an XLIFF 1.2 document in which each
translated unit carries a target element holding the unmasked target content,
each untranslated unit carries no target element, and no target element carries
a state attribute.

#### Scenario: Untranslated units emit no target
- **WHEN** a catalog containing one untranslated unit is serialised
- **THEN** that unit's serialised form contains no target element

#### Scenario: No state attribute
- **WHEN** a catalog containing a translated unit is serialised
- **THEN** that unit's target element declares no state attribute

### Requirement: Declare source and target languages
The system SHALL write the source language read from the uploaded document and
the target language chosen for the session as the file element's
source-language and target-language attributes.

#### Scenario: Both languages declared
- **WHEN** a catalog parsed from a document declaring source language `es` is serialised for target language `en-GB`
- **THEN** the file element declares source-language `es` and target-language `en-GB`

### Requirement: Serialisation round-trips
Parsing a document the system produced SHALL yield a catalog equal to the one
that produced it, for unit identifiers, source content, target content and
declared languages.

#### Scenario: Output re-parses to an equal catalog
- **WHEN** a catalog is serialised and the resulting document is parsed again
- **THEN** the second catalog equals the first in identifiers, sources, targets and languages

### Requirement: Whitespace-only sources need no translation
A unit whose source contains only whitespace SHALL be treated as translated on
parse, with its target set to its source.

#### Scenario: Blank source is already done
- **WHEN** a unit whose source is only whitespace is parsed
- **THEN** that unit reports itself translated
- **AND** its target equals its source
