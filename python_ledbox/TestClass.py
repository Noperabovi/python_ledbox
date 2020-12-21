class TestClass:
    """This Class is used to setup/test the CI-pipeline"""

    def add_integers(self, a: int, b: int) -> int:
        """Add one integer to another one."""

        return a + b

    def abs(self, a: int) -> int:
        """Returns the absolute value of the given integer."""

        if a >= 0:
            return a
        else:
            return -a
