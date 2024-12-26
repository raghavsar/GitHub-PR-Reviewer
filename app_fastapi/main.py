from fastapi import FastAPI, BackgroundTasks, HTTPException, status
import httpx
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

DJANGO_API_URL = "http://127.0.0.1:8001/"


class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None


@app.post("/start_task/")
async def start_task_endpoint(task_request: AnalyzePRRequest):
    """
    Trigger the task in Django and return the task ID.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DJANGO_API_URL}/start_task/",
            data={
                "repo_url": task_request.repo_url,
                "pr_number": task_request.pr_number,
                "github_token": task_request.github_token,

            }
        )
        if response.status_code != 200:
            return {"error": "Failed to start task", "details": response.text}
        task_id = response.json().get("task_id")
        return {"task_id": task_id, "status": "Task started"}


@app.get("/task_status/{task_id}/")
async def task_status_endpoint(task_id: str):
    """
    Check the status of the task by making a request to Django.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DJANGO_API_URL}task_status/{task_id}/")
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Task with ID {task_id} not found"
                )
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to Django service: {str(e)}"
            )