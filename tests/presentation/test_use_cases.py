from support.fakes import InMemoryCatalogReader, InMemorySessionRepository, RecordingCatalogWriter

from xlf_translator.presentation.use_cases import UseCases


def test_every_use_case_shares_one_repository():
    repository = InMemorySessionRepository()
    use_cases = UseCases.wired(repository, InMemoryCatalogReader(None), RecordingCatalogWriter())
    assert use_cases.repository is repository
    assert not use_cases.show.is_open()
