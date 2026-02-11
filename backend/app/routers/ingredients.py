from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.database import get_db
from ..models.ingredient import Ingredient
from ..models.user import User
from ..schemas.ingredient import IngredientCreate, IngredientOut
from ..dependencies.auth import get_current_user

router = APIRouter()
router.prefix = "/ingredients"
router.tags = ["Ingredients"]


@router.post("/", response_model=IngredientOut, status_code=status.HTTP_201_CREATED)
async def create_ingredient(
        ingredient_in: IngredientCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)
):
    if not current_user.family_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to a family to create ingredients."
        )

    new_ingredient = Ingredient(
        **ingredient_in.model_dump(),
        #auto fetched family id from current_user
        family_id=current_user.family_id
    )

    db.add(new_ingredient)
    await db.commit()
    await db.refresh(new_ingredient)
    return new_ingredient


@router.get("/", response_model=List[IngredientOut])
async def get_ingredients(
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)
):
    if not current_user.family_id:
        return []

    # Only fetch ingredients belonging to the user's family
    query = select(Ingredient).where(Ingredient.family_id == current_user.family_id)
    result = await db.execute(query)
    return result.scalars().all()