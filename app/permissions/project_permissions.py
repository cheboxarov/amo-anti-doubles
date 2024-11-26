from fastapi import Request
from schemas.project_schema import ProjectSchema
from fastapi.exceptions import HTTPException


class ProjectChecker:
    """Checks the specified conditions on the project associated with the request."""

    def __init__(self, is_admin: bool = False, is_active: bool = False):
        self.is_admin = is_admin
        self.is_active = is_active

    def __call__(self, request: Request) -> ProjectSchema:
        """Checks the specified conditions on the project associated with the request.

        Args:
            request (Request): The incoming FastAPI request, which should have a project
                            stored in its state.

        Returns:
            ProjectSchema: The project associated with the request if all conditions are met.

        Raises:
            HTTPException: If the project does not meet the specified `is_admin` or
                        `is_active` conditions, an HTTP 403 Forbidden error is raised.
        """
        project: ProjectSchema = request.state.project
        if self.is_admin and not project.is_admin:
            raise HTTPException(status_code=403, detail="Your project is not admin")
        if self.is_active and not project.is_active:
            raise HTTPException(status_code=403, detail="Your project is not active")
        return project
