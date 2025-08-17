# Deprecated: Pydantic schemas should live under app/schemas/
# Keeping this file to preserve imports; re-export Property from new location.
from app.schemas.property import Property  # noqa: F401
