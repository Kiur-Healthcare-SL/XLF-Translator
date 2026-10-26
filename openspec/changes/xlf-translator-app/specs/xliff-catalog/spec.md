# Spec Delta

## Purpose

Reads, classifies and writes Angular XLIFF 1.2 message catalogs, keeping every
element and attribute the application does not deliberately change.

## ADDED Requirements

### Requirement: Parse an XLIFF 1.2 catalog
The system SHALL read an XLIFF 1.2 document into an ordered collection of
translation units, preserving each unit's identifier, document order, source
content including inline placeholder elements, any target content, and all
leading and trailing whitespace. The system SHALL read the source language
declared by the file element, and the target language when one is declared.

#### Scenario: Catalog with sources only
- **WHEN** a document containing 60 trans-units, each with a source and no target, is parsed
- **THEN** the result contains 60 units in document order
- **AND** each unit reports the identifier declared in the document

#### Scenario: Source language is read
- **WHEN** a document whose file element declares source-language `es` and no target-language is parsed
- **THEN** the catalog reports source language `es` and no target language

#### Scenario: Whitespace is preserved
- **WHEN** a unit whose source begins with two non-breaking spaces is parsed
- **THEN** the parsed source begins with those two characters exactly, neither trimmed nor normalised

#### Scenario: Escaped markup is text
- **WHEN** a unit whose source contains the characters `&lt;p&gt;` is parsed
- **THEN** the parsed source contains the literal text `<p>` and no element node

### Requirement: Reject documents that cannot be translated
The system SHALL refuse a document that is not encoded as UTF-8, is not
well-formed XML, is not XLIFF version 1.2, declares no file element, declares
no source language, contains no translation unit, or contains duplicate unit
identifiers. Each refusal SHALL state what was expected and what was found.

#### Scenario: Not XML
- **WHEN** a file whose content is not well-formed XML is submitted
- **THEN** the document is refused
- **AND** the refusal states that well-formed XML was expected

#### Scenario: Not UTF-8
- **WHEN** a document whose XML declaration names encoding `ISO-8859-1` is submitted
- **THEN** the document is refused
- **AND** the refusal names both the expected encoding UTF-8 and the encoding found

#### Scenario: Invalid UTF-8 bytes
- **WHEN** a document containing a byte sequence that is not valid UTF-8 is submitted
- **THEN** the document is refused
- **AND** the refusal states that UTF-8 was expected

#### Scenario: Wrong XLIFF version
- **WHEN** a document declaring version 2.0 is submitted
- **THEN** the document is refused
- **AND** the refusal names both the expected version 1.2 and the version found

#### Scenario: No source language
- **WHEN** a document whose file element declares no source-language attribute is submitted
- **THEN** the document is refused
- **AND** the refusal states that a source language was expected

#### Scenario: Duplicate identifiers
- **WHEN** a document contains two trans-units sharing one identifier
- **THEN** the document is refused
- **AND** the refusal names the duplicated identifier

### Requirement: Classify a catalog by its content
The system SHALL classify a parsed catalog as fresh when every unit whose source
holds non-whitespace content is untranslated, completed when every unit is
translated, and partial otherwise. Classification SHALL depend only on document
content, never on the file's name.

#### Scenario: Fresh catalog
- **WHEN** a catalog whose units all lack targets, one of which has a whitespace-only source, is classified
- **THEN** the classification is fresh

#### Scenario: Partial catalog
- **WHEN** a catalog of 60 units in which one unit is untranslated is classified
- **THEN** the classification is partial

#### Scenario: Imported damage keeps a catalog partial
- **WHEN** a catalog whose every unit carries a target, one of them invalid, is classified
- **THEN** the classification is partial

#### Scenario: A draft named as a draft is judged by content
- **WHEN** a catalog whose every unit is translated is classified
- **THEN** the classification is completed regardless of the file name it arrived under

### Requirement: Whitespace-only sources need no translation
A unit whose source contains only whitespace SHALL be treated as translated on
parse, with its target set to its source, and SHALL be marked as auto-filled.
This rule is provisional; see deferred note N1 in design.md.

#### Scenario: Blank source is already done
- **WHEN** a unit whose source is only whitespace is parsed
- **THEN** that unit reports itself translated and auto-filled
- **AND** its target equals its source

### Requirement: Keep every element the application does not edit
The system SHALL write a catalog by modifying the uploaded document, so that
every element, attribute and text node the application does not edit is
present in the output with the same name, attributes, attribute values, text,
order and nesting. This includes `<note>`, `<context-group>` and `<context>`
elements and XML comments. Byte-level formatting, such as attribute quoting or
the form of the XML declaration, is not required to match.

#### Scenario: Notes and context groups are replicated
- **WHEN** a unit carrying a description note, a meaning note and a context group with source file and line number is serialised
- **THEN** the serialised unit carries the same note and context-group elements with the same attributes and text

#### Scenario: Comments are replicated
- **WHEN** a document containing an XML comment is serialised
- **THEN** the output contains the same comment at the same position

#### Scenario: Untouched targets are replicated
- **WHEN** a unit imported with a target declaring state `translated` is serialised without its target having been edited
- **THEN** the serialised unit carries that target with state `translated` and the same content

#### Scenario: Default namespace is kept
- **WHEN** a document in the XLIFF 1.2 default namespace is serialised
- **THEN** the output declares the same default namespace and no element carries a generated namespace prefix

### Requirement: Write targets for edited units
For each unit whose target was edited in the session, the system SHALL write a
target element holding the unmasked target content, placed immediately after
the unit's source element and carrying no state attribute. A unit whose target
became untranslated SHALL carry no target element.

#### Scenario: New target is placed after its source
- **WHEN** a unit without a target in the uploaded document is translated and serialised
- **THEN** its target element immediately follows its source element
- **AND** the target element declares no state attribute

#### Scenario: Edited imported target is replaced
- **WHEN** a unit imported with a target is given a different target and serialised
- **THEN** the unit carries exactly one target element, holding the new content

#### Scenario: Cleared target is removed
- **WHEN** a unit imported with a target has its target cleared and is serialised
- **THEN** that unit's serialised form contains no target element

### Requirement: Declare source and target languages
The system SHALL keep the file element's source-language attribute unchanged
and SHALL declare the session's target language as its target-language
attribute, adding it when absent and replacing its value when present.

#### Scenario: Both languages declared
- **WHEN** a catalog parsed from a document declaring source language `es` and no target language is serialised for target language `en-GB`
- **THEN** the file element declares source-language `es` and target-language `en-GB`

### Requirement: Serialisation round-trips
Parsing a document the system produced SHALL yield a catalog equal to the one
that produced it, for unit identifiers, source content, target content and
declared languages.

#### Scenario: Output re-parses to an equal catalog
- **WHEN** a catalog is serialised and the resulting document is parsed again
- **THEN** the second catalog equals the first in identifiers, sources, targets and languages
