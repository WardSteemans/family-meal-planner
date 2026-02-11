from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated
from starlette import status

from backend.app.dependencies.auth import get_current_user
from backend.app.models import User, Family
from backend.app.models.database import get_db
from backend.app.schemas.family import FamilyOut, FamilyCreate
from ..models.family import Family
from ..schemas.family import FamilyUpdate, FamilyCreate, FamilyOut

router = APIRouter()
router.prefix = "/families"
router.tags = ["Families"]


@router.post("/", response_model=FamilyOut, status_code=status.HTTP_201_CREATED)
async def create_family(
        family_in: FamilyCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Create new family
    new_family = Family(name=family_in.name)
    db.add(new_family)
    await db.flush()  # Flush to get new_family.id

    # Assign current user to this family
    current_user.family_id = new_family.id
    await db.commit()
    await db.refresh(new_family)

    return new_family

@router.get("/me", response_model=FamilyOut)
async def get_my_family(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not part of a family"
        )
    return current_user.family