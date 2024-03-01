import unittest
from unittest.mock import patch, MagicMock
from git.exc import InvalidGitRepositoryError, NoSuchPathError
import os
from jupyterquest.commit_analysis import analyze_commit_messages

class TestCommitAnalysis(unittest.TestCase):

    @patch('jupyterquest.commit_analysis.Repo')
    def test_analyze_commit_messages_valid_repo_with_branches(self, mock_repo):
        # Simulate multiple branches with shared and unique commits
        mock_branch1_commit1 = MagicMock(message='feat: Add new feature\nDetails.\n')
        mock_branch1_commit2 = MagicMock(message='fix: Fix issue\nDetails.\n')
        mock_branch2_commit1 = mock_branch1_commit1  # Simulate a shared commit across branches
        mock_branch2_commit2 = MagicMock(message='Update readme\nMinor updates.\n')

        mock_repo.return_value.branches = ['branch1', 'branch2']
        mock_repo.return_value.iter_commits.side_effect = [
            [mock_branch1_commit1, mock_branch1_commit2],  # branch1 commits
            [mock_branch2_commit1, mock_branch2_commit2]   # branch2 commits
        ]
        
        # Expected result should consider unique commits across all branches
        expected_result = {
            "total_commits": 3,
            "short_message_issues": 0,
            "non_informative_issues": 2,
            "non_conforming_messages": 1
        }
        
        result = analyze_commit_messages('mock_repo_path')
        self.assertEqual(result, expected_result)

    @patch('jupyterquest.commit_analysis.Repo')
    def test_analyze_commit_messages_invalid_repo(self, mock_repo):
        # Mock to simulate an invalid repository path
        mock_repo.side_effect = InvalidGitRepositoryError
        result = analyze_commit_messages('/path/to/invalid/repo')
        self.assertIn("Error with the repository:", result)

    @patch('jupyterquest.commit_analysis.Repo')
    def test_analyze_commit_messages_no_commits(self, mock_repo):
        # Mock to simulate a repository with no commits
        mock_repo.return_value.iter_commits.return_value = []
        result = analyze_commit_messages('/path/to/repo/with/no/commits')
        self.assertEqual(result, "No commits found in the repository.")

    @patch('os.getenv')
    @patch('jupyterquest.commit_analysis.Repo')
    def test_analyze_commit_messages_env_variable(self, mock_repo, mock_getenv):
        # Mocking os.getenv to simulate GITHUB_WORKSPACE environment variable
        mock_getenv.return_value = '/mock/repo/path'
        
        # Setup mock commits as needed
        mock_repo.return_value.iter_commits.return_value = [
            MagicMock(message='feat: Enhance feature\nDetailed explanation.\n')
        ]
        
        # Expected results based on the mocked commits
        expected_result = {
            "total_commits": 1,
            "short_message_issues": 0,
            "non_informative_issues": 0,
            "non_conforming_messages": 0
        }
        
        result = analyze_commit_messages(os.getenv('GITHUB_WORKSPACE'))
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()