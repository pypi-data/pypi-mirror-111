from pydantic import BaseModel, Field


class SimplifierParams(BaseModel):
    hetero_atoms: bool = Field(
        True,
        description="Include hetero atoms close to transformation site",
    )
    aromatic: bool = Field(
        True,
        description="Include aromatic cycles close to transformation site",
    )
    conjugated: bool = Field(
        False,
        description="Include conjugated bonds close to transformation site",
    )
    cycles: bool = Field(
        False,
        description="Include cycles close to transformation site",
    )
