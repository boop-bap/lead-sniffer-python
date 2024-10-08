from typing_extensions import Literal, TypedDict


class LeadTarget(TypedDict):
    model: Literal["Retail", "E-commerce", "Both e-commerce and physical stores", "Physical stores"]
    monthly_or_more_often_published_catalogs: Literal["Yes", "No", "Maybe", "Not sure"]
    type: Literal["B2B", "B2C", "Both B2B and B2C", "Agency"]
    website_url: Literal["Yes", "No"]
    online: Literal["Yes", "No"]
