from pydantic import BaseModel
from typing import List

class ReviewSchema(BaseModel):
    rating: int
    comment: str
    reviewerName: str
    reviewerEmail: str

class DimensionsSchema(BaseModel):
    width: float
    height: float
    depth: float

class ProductSchema(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    brand: str | None = None
    sku: str
    availabilityStatus: str
    minimumOrderQuantity: int
    thumbnail: str
    tags: List[str]
    reviews: List[ReviewSchema]
    returnPolicy: str
    warrantyInformation: str
    shippingInformation: str
    weight: float
    dimensions: DimensionsSchema