from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance Web"],
)


templates = Jinja2Templates(
    directory="web/templates"
)


@router.get("/")
def maintenance_dashboard(
    request: Request,
):
    return templates.TemplateResponse(
        "pages/maintenance/dashboard.html",
        {
            "request": request,
        },
    )
