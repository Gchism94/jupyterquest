import unittest
from jupyterquest.code_quality_check import assess_code_complexity, assess_code_structure, assess_code_quality

class TestCodeQualityCheck(unittest.TestCase):
    def test_assess_code_complexity_valid_input(self):
        code = "def example_function(x):\n    return x * 2\n"
        result = assess_code_complexity(code)
        self.assertIsInstance(result, str)  # The function now returns a string.
        self.assertIn("example_function", result)  # Checking for function name in the result.

    def test_assess_code_complexity_invalid_input(self):
        code = 123  # Non-string input
        result = assess_code_complexity(code)
        self.assertEqual(result, "Invalid input: Code must be a string")

    def test_assess_code_structure_valid_input(self):
        code = "def example_function(x):\n    return x * 2\n"
        result = assess_code_structure(code)
        self.assertTrue("Number of functions: 1" in result)

    def test_assess_code_structure_syntax_error(self):
        code = "def example_function(x):\nreturn x * 2"  # Indentation error
        result = assess_code_structure(code)
        self.assertTrue("Syntax error in code:" in result)

    def test_assess_code_quality(self):
        code_blocks = [
            "def example_function(x):\n    return x * x\n",
            "def another_function(y):\n    if y > 0:\n        return y\n    else:\n        return -y\n"
        ]
        result = assess_code_quality(code_blocks)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(code_blocks))

        for key, value in result.items():
            # Broad check for the presence of expected function names in the complexity report
            self.assertTrue("example_function" in value["Complexity"] or "another_function" in value["Complexity"])


    def test_assess_code_quality_invalid_input(self):
        code_blocks = ["def example_function(x):\n    return x * x\n", 123]  # Contains invalid input
        result = assess_code_quality(code_blocks)
        self.assertEqual(result, {"Error": "All code blocks must be strings"})

if __name__ == '__main__':
    unittest.main()