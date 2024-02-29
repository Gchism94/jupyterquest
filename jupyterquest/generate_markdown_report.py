def format_complexity_report(complexity_report):
    """
    Formats the complexity report into a markdown string.
    """
    report_md = "### Complexity Report\n"
    for item in complexity_report:
        report_md += f"- **Function/Method**: {item[0]}, **Complexity**: {item[1]}, **Rank**: {item[2]}\n"
    return report_md

def format_structure_report(structure_report):
    """
    Formats the structure report into a markdown string.
    """
    return f"### Structure Report\n- {structure_report}\n"

def generate_markdown_report(quality_reports, repo_structure_results, notebook_stats=None, other_reports=None):
    """Generates a comprehensive Markdown (.md) report from various checks."""
    report_md = "# Introduction\n\nThis report presents the results of the autograding process for a Jupyter notebook...\n\n"

    # Include notebook stats if provided
    if notebook_stats and 'total_code_cells' in notebook_stats:
        report_md += f"- **Total Code Cells**: {notebook_stats['total_code_cells']}\n"
    else:
        report_md += "- **Total Code Cells**: Data not available\n"

    # Add Repository Structure Check Results
    report_md += "## Repository Structure Check\n"
    report_md += "- **Missing Directories**: " + ", ".join(repo_structure_results['missing_directories']) + "\n"
    report_md += "- **Unexpected Files**: " + ", ".join(repo_structure_results['unexpected_files']) + "\n\n"

    # Add Code Quality Reports
    report_md += "## Code Quality Checks\n"
    for block_id, report in quality_reports.items():
        report_md += f"#### Cell {block_id}\n"
        report_md += format_complexity_report(report['Complexity']) + "\n"
        report_md += format_structure_report(report['Structure']) + "\n"

    # Add other reports if any
    if other_reports:
        for title, content in other_reports.items():
            report_md += f"## {title}\n{content}\n"

    return report_md

def save_markdown_report(report_content, file_path):
    """Saves the given Markdown report content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(report_content)

# Example usage
if __name__ == "__main__":
    sample_quality_reports = {
        "Code Cell 1": {
            "Complexity": [("example_function", 2, "B")],
            "Structure": "Good structure and organization."
        },
        # ... other code cells
    }
    sample_repo_structure_results = {
        "missing_directories": ["data"],
        "unexpected_files": ["temp.txt"]
    }
    # Example notebook statistics (adjust as necessary)
    sample_notebook_stats = {
        "total_code_cells": 10,
        "total_markdown_cells": 5,
    }
    # Assuming other_reports is a dictionary of other check results
    markdown_report = generate_markdown_report(sample_quality_reports, sample_repo_structure_results, sample_notebook_stats)

    report_file_path = "/autograder/autograder_report.md" 
    save_markdown_report(markdown_report, report_file_path)