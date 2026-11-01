import sys
from types import ModuleType


def _install_deepeval_test_doubles():
    deepeval = ModuleType("deepeval")
    deepeval.evaluate = lambda *args, **kwargs: None

    test_case = ModuleType("deepeval.test_case")

    class LLMTestCase:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class LLMTestCaseParams:
        ACTUAL_OUTPUT = "actual_output"
        EXPECTED_OUTPUT = "expected_output"

    test_case.LLMTestCase = LLMTestCase
    test_case.LLMTestCaseParams = LLMTestCaseParams

    metrics = ModuleType("deepeval.metrics")

    class FakeMetric:
        def __init__(self, **kwargs):
            self.options = kwargs
            self.score = 0.876
            self.test_case = None

        def measure(self, test_case):
            self.test_case = test_case

    metrics.AnswerRelevancyMetric = FakeMetric
    metrics.GEval = FakeMetric

    sys.modules["deepeval"] = deepeval
    sys.modules["deepeval.test_case"] = test_case
    sys.modules["deepeval.metrics"] = metrics


_install_deepeval_test_doubles()
