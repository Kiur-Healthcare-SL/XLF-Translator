"""A builder that records whatever a domain object describes into it."""


class DescriptionRecorder:
    def __init__(self):
        self.described = {}

    def __getattr__(self, name):
        def record(*values):
            self.described[name] = values if len(values) != 1 else values[0]

        return record


def described(subject, method="describe_into"):
    recorder = DescriptionRecorder()
    getattr(subject, method)(recorder)
    return recorder.described
