# analysis_service.py
import uuid
import os
import sys
import json
from .github import fetch_pr_files, fetch_file_content
from .ai_agent import analyze_code_with_llm

def analyze_pr(repo_url, pr_number, github_token=None):
    """Analyzes the pull request for code issues."""
    task_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token)

        results = {
            "files": [],
            "summary": {
                "total_files": 0,
                "total_issues": 0,
                "critical_issues": 0
            }
        }

        for file in pr_files:
            file_name = file["filename"]
            raw_content = fetch_file_content(repo_url, file_name, github_token)

            # Analyze with LLM
            analysis_result = analyze_code_with_llm(raw_content, file_name)

            try:
                analysis_data = json.loads(analysis_result)
            except json.JSONDecodeError as e:
                return {
                    "task_id": task_id,
                    "status": "error",
                    "message": f"JSON decode error: {str(e)}"
                }

            total_issues = len(analysis_data["issues"])
            critical_issues = sum(
                1 for issue in analysis_data["issues"] if issue["type"] == "bug"
            )

            results["files"].append({
                "name": file_name,
                "issues": analysis_data["issues"]
            })

            results["summary"]["total_files"] += 1
            results["summary"]["total_issues"] += total_issues
            results["summary"]["critical_issues"] += critical_issues

        return {
            "task_id": task_id,
            "status": "completed",
            "results": results
        }
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {
            "task_id": task_id,
            "status": "error",
            "message": f"{exc_type, fname, exc_tb.tb_lineno,e}"
        }