from xlf_translator.application.export_artifact import ExportArtifact


def test_an_artifact_carries_name_and_content():
    artifact = ExportArtifact("messages.en-GB.xlf", b"<xliff/>")
    assert (artifact.name, artifact.content) == ("messages.en-GB.xlf", b"<xliff/>")
