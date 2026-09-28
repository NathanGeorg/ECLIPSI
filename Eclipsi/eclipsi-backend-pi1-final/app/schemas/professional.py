from decimal import Decimal
from pydantic import BaseModel


class ProfessionalResponse(BaseModel):
    id: int
    user_id: int
    name: str
    specialty: str
    approach: str
    description: str
    modality: str
    location: str | None = None
    price: Decimal | None = None
