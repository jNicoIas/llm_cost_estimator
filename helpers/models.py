from typing import Dict
from pydantic import BaseModel, Field, root_validator, ValidationError, field_validator
from typing import NamedTuple, Callable
from typing import Optional


class CostEstimatorConfig(BaseModel):
    model: str
    service: str
    llm_input: Optional[str] = None
    llm_output: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    is_input_str: bool = False
    llm_provider: str = "openai"
    current_cost: float = 0.0
    
   

class LlmPricing(BaseModel):
    input_pricing:  float
    output_pricing: float
    
class CostEstimatorBlueprint(BaseModel):
    pricing: Dict[str, LlmPricing]

M_tokens = 1_000_000

OpenAiCostEstimator = CostEstimatorBlueprint(
    pricing = {
        "gpt-4-turbo":              LlmPricing(input_pricing=10/M_tokens, output_pricing=30/M_tokens),
        "gpt-4-turbo-2024-04-09":   LlmPricing(input_pricing=10/M_tokens, output_pricing=30/M_tokens),
        "gpt-4":                    LlmPricing(input_pricing=30/M_tokens, output_pricing=60/M_tokens),
        "gpt-4-32k":                LlmPricing(input_pricing=60/M_tokens, output_pricing=120/M_tokens),
        "gpt-4-0125-preview":       LlmPricing(input_pricing=10/M_tokens, output_pricing=30/M_tokens),
        "gpt-4-1106-preview":       LlmPricing(input_pricing=10/M_tokens, output_pricing=30/M_tokens),
        "gpt-4-vision-preview":     LlmPricing(input_pricing=10/M_tokens, output_pricing=30/M_tokens),
        "gpt-3.5-turbo-0125":       LlmPricing(input_pricing=0.50/M_tokens, output_pricing=1.50/M_tokens),
        "text-embedding-3-small":   LlmPricing(input_pricing=0.020/M_tokens, output_pricing=0.010/M_tokens),
        "text-embedding-3-large":   LlmPricing(input_pricing=0.130/M_tokens, output_pricing=0.065/M_tokens),
        "gpt-4o-mini":              LlmPricing(input_pricing=0.150/M_tokens, output_pricing=0.600/M_tokens),
        "gpt-4o":                   LlmPricing(input_pricing=5/M_tokens, output_pricing=15/M_tokens),
    }
)

AnthropicCostEstimator = CostEstimatorBlueprint(
    pricing = {
        "claude-3.5-sonnet":        LlmPricing(input_pricing=3.0/M_tokens, output_pricing=15.0/M_tokens),
        "claude-3-opus":            LlmPricing(input_pricing=15.0/M_tokens, output_pricing=75.0/M_tokens),
        "claude-3-haiku":           LlmPricing(input_pricing=0.25/M_tokens, output_pricing=1.25/M_tokens),
    }
)
