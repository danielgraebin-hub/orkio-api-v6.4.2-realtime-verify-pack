from fastapi import APIRouter

router = APIRouter(prefix="/api/internal/git", tags=["git-internal"])

@router.get("/health")
def git_health():
    return {"ok": True, "service": "git_internal"}
