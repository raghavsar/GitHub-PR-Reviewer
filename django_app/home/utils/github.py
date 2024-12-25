import requests
import base64
from urllib.parse import urlparse
import uuid
import os, sys
from .ai_agent import analyze_code_with_llm

def get_owner_and_repo(url):
    passed_url = urlparse(url)
    path_parts = passed_url.path.strip("/").spilt("/")
    if len(path_parts) >=2 :
        owner, repo = path_parts[0], path_parts[1]
        return owner, repo
    return None, None


def fetch_pr_files(repo_url, pr_number, github_token=None):
    owner, repo = get_owner_and_repo(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization" : f"token{github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_file_content(repo_url, file_path, github_token=None):
    owner, repo = get_owner_and_repo(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/api/{file_path}"
    headers = {"Authorization" : f"token{github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content = response.json()
    return base64.b64decode(content['content']).decode()


    #Analyzes the pull request for code issues
def analyze_pr(repo_url, pr_number, github_token=None):
    task_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url, pr_number, github_token)
        analysis_results = []
        for file in pr_files:
            file_name = file['filename']
            raw_content = fetch_file_content(repo_url, file_name, github_token)
            # Analyze with LLM
            analysis_result = analyze_code_with_llm(raw_content, file_name)
            analysis_results.append({"results" : analysis_result, "file_name" : file_name})
        return {"task_id" : task_id, "results" : analysis_results}

    except Exception as e:
        print(e)

    return {"task_id" : task_id, "results" : []}
    #         try:
    #             analysis_data = json.loads(analysis_result)  # Parse the result as JSON
    #         except json.JSONDecodeError as e:
    #             return {"task_id": task_id, "status": "error", "message": f"JSON decode error: {str(e)}"}
    #
    #
    #         total_issues = len(analysis_data["issues"])
    #         critical_issues =  sum(
    #                 1 for issue in analysis_data["issues"] if issue["type"] == "bug"
    #             )
    #
    #         results["files"].append({"name": file_name, "issues": analysis_data["issues"]})
    #
    #         results["summary"]["total_files"] += 1
    #         results["summary"]["total_issues"] += total_issues
    #         results["summary"]["critical_issues"] += critical_issues
    #
    #     return {"task_id": task_id, "status": "completed", "results": results}
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)
    #     return {"task_id": task_id, "status": "error", "message": f"{exc_type, fname, exc_tb.tb_lineno,e}"}