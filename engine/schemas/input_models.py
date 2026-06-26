from pydantic import BaseModel, Field
from typing import Literal

class BeamDesignInput(BaseModel):
    # Support type (Support Layout)
    beam_type: Literal["Simply Supported", "Cantilever", "Continuous"] = Field(..., description="Support layout")

    # Structural Dimensions
    span: float = Field(..., gt=0, description="Effective Span length in meters")
    width_bw: float = Field(..., gt=0, description="Width of beam web in mm")
    depth_D: float = Field(..., gt=0, description="Overall depth of beam in mm")
    clear_cover: float = Field(..., ge=0, description="concrete clear cover in mm")

    # Material Specifications
    fck: float = Field(..., description="grade of concrete in N/mm²")
    fy: float = Field(..., description="grade of steel in N/mm²")

    #Loading Conditions
    dead_load: float = Field(..., ge=0, description="Superimposed dead load")
    live_load: float = Field(..., ge=0, description="Live lode")
