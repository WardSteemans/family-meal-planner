from enum import Enum

class IngredientCategory(str, Enum):
    FRUIT = "fruit"
    VEGETABLE = "vegetable"
    DAIRY = "dairy"
    MEAT = "meat"
    PANTRY = "pantry"
    OTHER = "other"

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class Role(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    CHILD = "child"