# AGENTS.md

Working agreement for any agent contributing to this repository.

## What this project is

A Streamlit application for translating Angular XLIFF 1.2 (`.xlf`) message
catalogs one translation unit per screen: upload, translate with Angular's
inline placeholders masked as `{1}`...`{n}`, save drafts at any time, and
download the finished catalog once every unit is valid.
See [design-notes.md](design-notes.md) for the work and decisions deferred to
later changes.

## Workflow

This repository uses OpenSpec. Plan before you code: propose a change, get the
proposal, specs and tasks in place, then implement. Project context and
per-artifact rules live in [openspec/config.yaml](openspec/config.yaml).

- Proposals: under 500 words.
- Tasks: chunks of at most 1 hour.
- Apply: keep summaries concise.
- Archive: summarize the archive outcome before finishing.

## Git: no write operations

**Agents MUST NOT perform any git write operation.** This is a hard requirement,
not a preference, and it holds no matter who asks or how the request is phrased.

## Architecture

Four layers, dependencies pointing inwards only:

| Layer             | Contains                                                         | Must not contain                            |
| ----------------- | ---------------------------------------------------------------- | ------------------------------------------- |
| `domain/`         | Business entities and value objects                              | Any I/O, XML, Streamlit or framework import |
| `application/`    | Use cases, and the ports they depend on                          | Concrete adapters                           |
| `infrastructure/` | XLIFF parsing and serialisation, encoding checks                 | Business rules                              |
| `presentation/`   | Streamlit pages, widgets, session-state adapters                 | Business logic of any kind                  |

`presentation -> application -> domain`. `infrastructure` implements
`application` ports and is wired in at the composition root. The business logic
must be fully testable without importing Streamlit.

## Code style — Object Calisthenics

Apply this all business logic related code.
Apply it to infrastracture related code only when possible.

1. One level of indentation per method.
2. No `else` keyword.
3. Wrap all primitives and strings in value objects.
4. First-class collections: a class holding a collection holds nothing else.
5. One dot per line. Law of Demeter.
6. No abbreviations in names.
7. Keep entities small.
8. No more than two instance variables per class.
9. No getters, setters or public properties — tell, don't ask.

## Hard limits

- Functions: under 20 lines.
- Classes: under 200 lines.
- One class per file, the file named after the class.
- Every class has its own dedicated unit test file, mirroring the package path.

## Testing

`pytest`. A change is not done until the layering rules and the limits above
hold, and the new class's test file exists and passes.
