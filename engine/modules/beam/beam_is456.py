import math
from schemas.input_models import BeamDesignInput

def design_beam_is456(inputs: BeamDesignInput) -> dict:
    # All calculation of RCC beam Section according to the LSM of IS 456:2000.

    #1.Calculate Effective Depth (d)
    assumed_bar_dia = 20
    effective_depth_d = inputs.depth_D - inputs.clear_cover - (assumed_bar_dia/2.0)

    #2.Factored Design Load (wu) & Bending Moment (Mu)
    total_load = inputs.dead_load + inputs.live_load
    factored_load_wu = 1.5*total_load
    # Maximum Bending Moment as per Support Layout [IS 456 cl. 22]
    if inputs.beam_type == "Simply Supported":
        max_bm_mu = (factored_load_wu * (inputs.span ** 2)) /  8.0
    elif inputs.beam_type == "Cantilever":
        max_bm_mu = (factored_load_wu * (inputs.span ** 2)) /  2.0
    else:
        max_bm_mu = (factored_load_wu * (inputs.span ** 2)) /  10.0

    #3.Determining Mu_limit
    if inputs.fy == 415:
        xu_max_by_d = 0.48
        lim_moment_coeff = 0.138
    elif inputs.fy == 500:
        xu_max_by_d = 0.46
        lim_moment_coeff = 0.133
    elif inputs.fy == 550:
        xu_max_by_d = 0.44
        lim_moment_coeff = 0.130
    else:
        xu_max_by_d = 700 / (1100 + 0.87 * inputs.fy)
        lim_moment_coeff = 0.36 * xu_max_by_d * (1.0 - 0.42 * xu_max_by_d)

    mu_limiting = (lim_moment_coeff * inputs.fck * inputs.width_bw * (effective_depth_d ** 2)) / 1e6

    #4.Check section status 
    section_status = "PASS"
    remark = "Section is singly reinforced."
    if max_bm_mu > mu_limiting:
        section_status = "WARNING"
        remark = "Doubly Reinforced Section (Concrete Depth sizing insufficient for tensile steel alone)"

    #5. Ast Calculation (Tension Reinforcement Area)
    term1 = 0.87 * inputs.fy * effective_depth_d
    term2 = inputs.fy / (inputs.width_bw * effective_depth_d * inputs.fck)
    mu_n_mm = max_bm_mu * 1e6

    discriminant = (term1 ** 2) - (4.0 * (term1 * term2 * 0.5) * mu_n_mm)

    if discriminant >= 0:
        ast_required = (term1 - math.sqrt(discriminant)) / (2.0 * (term1 * term2 * 0.5))
    else:
        ast_required = (0.5 * 0.138 * inputs.fck * inputs.width_bw * effective_depth_d) / inputs.fy

    # enforcing minimum Ast [IS 456 cl. 26.5.1.1]
    ast_minimum = (0.85 * inputs.width_bw * effective_depth_d) / inputs.fy 
    if ast_required < ast_minimum:
        ast_required = ast_minimum
        remark += " Ast Minimum enforced."

    #6.Basic Vertical Deflection Check [IS 456 cl. 23.2.1]
    if inputs.beam_type == "Simply Supported":
        allowable_ratio = 20.0
    elif inputs.beam_type == "Cantilever":
        allowable_ratio = 7.0
    else:
        allowable_ratio = 26.0

    actual_ratio = (inputs.span * 1000.0) / effective_depth_d
    deflection_status = "PASS" if actual_ratio <= allowable_ratio else "FAIL"

    # Output Dict for Backend pipeline
    return {
        "factored_bm":{"value": round(max_bm_mu,3),"unit":"kN-m","clause":"cl. 22.4"},
        "mu_limiting":{"value": round(mu_limiting,3),"unit":"kN-m","clause":"Annex G cl. 38.1"},
        "ast_required":{"value": round(ast_required,3),"unit":"mm²","clause":"cl. 26.5.1.1"},
        "deflection_check":{
            "actual_ratio": round(actual_ratio,3),
            "allowable_ration": round(allowable_ratio,3),
            "status": deflection_status,
            "clause": "cl. 23.2"
        },
        "section_status": section_status,
        "remark": remark
        
    }