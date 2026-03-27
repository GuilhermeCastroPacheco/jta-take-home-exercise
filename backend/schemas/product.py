from pydantic import BaseModel
from typing import Optional, List

class ReviewSchema(BaseModel):
    rating: int
    comment: str
    reviewerName: str
    reviewerEmail: str

class ProductSchema(BaseModel):
    id: int
    title: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    brand: Optional[str] = None
    availabilityStatus: str
    minimumOrderQuantity: int
    thumbnail: str
    tags: List[str]
    reviews: List[ReviewSchema]
    returnPolicy: str