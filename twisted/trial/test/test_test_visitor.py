from twisted.trial.unittest import TestCase, TestResult

class TestTestVisitor(TestCase):

    def setUp(self):
        try:
            from twisted.trial.unittest import TestVisitor
            class MockVisitor(TestVisitor):
                def __init__(self):
                    self.calls = []
                def visitCase(self, testCase):
                    self.calls.append(("case", testCase))
                def visitClass(self, testClass):
                    self.calls.append(("class", testClass))
                def visitClassAfter(self, testClass):
                    self.calls.append(("class_after", testClass))
                def visitModule(self, testModule):
                    self.calls.append(("module", testModule))
                def visitModuleAfter(self, testModule):
                    self.calls.append(("module_after", testModule))
                def visitSuite(self, testSuite):
                    self.calls.append(("suite", testSuite))
                def visitSuiteAfter(self, testSuite):
                    self.calls.append(("suite_after", testSuite))
            self.mock_visitor = MockVisitor
        except ImportError:
            pass

    def test_imports(self):
        from twisted.trial.unittest import TestVisitor

    def test_visit_case_default(self):
        from twisted.trial.unittest import TestVisitor
        from twisted.trial.runner import TestMethod
        testCase = TestMethod(self.test_visit_case)
        test_visitor = TestVisitor()
        testCase.visit(test_visitor)

    def test_visit_case(self):
        from twisted.trial.runner import TestMethod
        testCase = TestMethod(self.test_visit_case)
        test_visitor = self.mock_visitor()
        testCase.visit(test_visitor)
        self.assertEqual(test_visitor.calls, [("case", testCase)])

    def test_visit_suite_default(self):
        from twisted.trial.unittest import TestVisitor
        from twisted.trial.runner import TrialRoot
        from twisted.trial.reporter import Reporter
        from twisted.trial.util import _Janitor
        testCase = TrialRoot(Reporter(), _Janitor())
        test_visitor = TestVisitor()
        testCase.visit(test_visitor)

    def test_visit_suite(self):
        from twisted.trial.runner import TrialRoot
        from twisted.trial.reporter import Reporter
        from twisted.trial.util import _Janitor
        import sys
        test_visitor = self.mock_visitor()
        testCase = TrialRoot(Reporter(), _Janitor())
        testCase.addModule(sys.modules[__name__])
        testCase.visit(test_visitor)
        self.failIf(len(test_visitor.calls) < 4)
        self.assertEqual(test_visitor.calls[0], ("suite", testCase))
        self.assertEqual(test_visitor.calls[1][0], "module")
        self.assertEqual(test_visitor.calls[2][0], "class")
        self.assertEqual(test_visitor.calls[-1], ("suite_after", testCase))

    def test_visit_module_default(self):
        from twisted.trial.unittest import TestVisitor
        from twisted.trial.runner import TestModuleRunner
        import sys
        testCase = TestModuleRunner(sys.modules[__name__])
        test_visitor = TestVisitor()
        testCase.visit(test_visitor)

    def test_visit_module(self):
        from twisted.trial.runner import TestModuleRunner
        import sys
        test_visitor = self.mock_visitor()
        testCase = TestModuleRunner(sys.modules[__name__])
        testCase.visit(test_visitor)
        self.failIf(len(test_visitor.calls) < 5)
        self.assertEqual(test_visitor.calls[0], ("module", testCase))
        self.assertEqual(test_visitor.calls[1][0], "class")
        self.assertEqual(test_visitor.calls[-1], ("module_after", testCase))

    def test_visit_class_default(self):
        from twisted.trial.unittest import TestVisitor
        from twisted.trial.runner import TestCaseRunner
        testCase = TestCaseRunner(self.__class__)
        testCase.methodNames = ["test_visit_class_default"]
        test_visitor = TestVisitor()
        testCase.visit(test_visitor)

    def test_visit_class(self):
        from twisted.trial.runner import TestCaseRunner
        test_visitor = self.mock_visitor()
        testCase = TestCaseRunner(self.__class__)
        testCase.methodNames = ["test_visit_class"]
        testCase.visit(test_visitor)
        self.assertEqual(len(test_visitor.calls), 3)
        self.assertEqual(test_visitor.calls[0], ("class", testCase))
        self.assertEqual(test_visitor.calls[1][0], "case")
        self.assertEqual(test_visitor.calls[2], ("class_after", testCase))