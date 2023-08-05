from approvaltests.core.reporter import Reporter


class FirstWorkingReporter(Reporter):
    """
    A composite reporter that goes through a list
    of reporters, running the first one that is
    working on the current machine.

    This is mostly an implementation detail of other
    classes in the library, but it may be useful in scenarios
    where a team wants to supply a list of custom reporter,
    and have the first working one of these be used.

    See also MultiReporter.
    """

    def __init__(self, *reporters) -> None:
        self.reporters = reporters

    def report(self, received_path: str, approved_path: str) -> bool:
        for r in self.reporters:
            try:
                success = r.report(received_path, approved_path)
                if success:
                    return True
            except:
                pass

        return False

    def __str__(self):
        reporters = ", ".join(str(s) for s in self.reporters)
        return f"FirstWorkingReporter({reporters})"

    __repr__ = __str__

    def __eq__(self, other) -> bool:
        return repr(self) == repr(other)
