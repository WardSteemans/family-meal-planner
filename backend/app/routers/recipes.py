from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.database import get_db
from ..models.recipy import Recipe
from ..models.user import User
from ..schemas.recipe import RecipeCreate, RecipeOut
from ..dependencies.auth import get_current_user

router = APIRouter()
router.prefix = "/recipes"
router.tags = ["Recipes"]

@router.post("/", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_in: RecipeCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    if not current_user.family_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to a family to create recipes."
        )

    new_recipe = Recipe(
        **recipe_in.model_dump(),
        # auto fetched family id from current_user
        family_id=current_user.family_id
    )

    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe

@router.get("/", response_model=List[RecipeOut])
async def get_recipes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    if not current_user.family_id:
        return []

    # Isolation logic
    query = select(Recipe).where(Recipe.family_id == current_user.family_id)
    result = await db.execute(query)
    return result.scalars().all()