import unittest
from jupyterquest import code_quality_check

class TestCodeQualityCheck(unittest.TestCase):
    def test_assess_code_complexity_valid_input(self):
        code = "def example_function(x):\n    return x * 2\n"
        result = code_quality_check.assess_code_complexity(code)
        self.assertIsInstance(result, list)  # Ensure it returns a list
        self.assertGreater(len(result), 0)  # Ensure the list is not empty
        # Further assertions can check for specific complexity metrics

    def test_assess_code_complexity_invalid_input(self):
        code = 123  # Non-string input
        result = code_quality_check.assess_code_complexity(code)
        self.assertEqual(result, "Invalid input: Code must be a string")

    def test_assess_code_structure_valid_input(self):
        code = "def example_function(x):\n    return x * 2\n"
        result = code_quality_check.assess_code_structure(code)
        self.assertTrue("Number of functions: 1" in result)

    def test_assess_code_structure_syntax_error(self):
        code = "def example_function(x):\nreturn x * 2"  # Indentation error
        result = code_quality_check.assess_code_structure(code)
        self.assertTrue("Syntax error in code:" in result)

    def test_assess_code_quality(self):
        code_blocks = [
            "def example_function(x):\n    return x * x\n",
            "def another_function():\n    pass\n"
        ]
        result = code_quality_check.assess_code_quality(code_blocks)
        self.assertIsInstance(result, dict)  # Ensure it returns a dictionary
        self.assertEqual(len(result), len(code_blocks))  # Ensure all blocks are assessed

        # Check for presence of expected keys in the results
        for key in result:
            self.assertIn("Complexity", result[key])
            self.assertIn("Structure", result[key])

    def test_assess_code_quality_invalid_input(self):
        code_blocks = ["def example_function(x):\n    return x * x\n", 123]  # Contains invalid input
        result = code_quality_check.assess_code_quality(code_blocks)
        self.assertEqual(result, {"Error": "All code blocks must be strings"})

if __name__ == '__main__':
    unittest.main()