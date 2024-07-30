from utils import TokenCounter
from . models import OpenAiCostEstimator, AnthropicCostEstimator, CostEstimatorConfig

class LlmCostEstimator:
    def __init__(self):
        self.current_cost = 0
        
    def update_current_cost(self, estimator_config: CostEstimatorConfig):
        """
        payload keys: input, output
        """
        try:
            
            
            if not estimator_config.is_input_str and estimator_config.input_tokens is None:
                raise ValueError("input_tokens and output_tokens must be provided if is_input_str is True")
            if estimator_config.is_input_str and estimator_config.llm_input is None:
                raise ValueError("llm_input and llm_output must be provided if is_input_str is False")

            
            self.current_cost = estimator_config.current_cost if self.current_cost == 0 else self.current_cost
            
            if estimator_config.is_input_str:
                input_dict = {"messages":[
                            {"role": "user", "content": estimator_config.llm_input},
                        ]}
                output_dict = {"messages":[
                            {"role": "user", "content": estimator_config.llm_output},
                        ]}
                input_tokens    = TokenCounter(payload = input_dict,  model=estimator_config.model).num_tokens_from_messages()
                output_tokens   = TokenCounter(payload = output_dict, model=estimator_config.model).num_tokens_from_messages()
            else:
                input_tokens = estimator_config.input_tokens
                output_tokens = estimator_config.output_tokens
                
            input_pricing = OpenAiCostEstimator.pricing[estimator_config.model].input_pricing
            output_pricing = OpenAiCostEstimator.pricing[estimator_config.model].output_pricing

            input_cost  = input_pricing * input_tokens
            output_cost = output_pricing * output_tokens
            
            total_cost = input_cost + output_cost
            
            self.current_cost += total_cost
            
            print(estimator_config.llm_provider)
            print("input/output tokens:", input_tokens, '/', output_tokens)
            print("Cost of this post: $", total_cost)
            print("Accumulated cost:  $", self.current_cost, "\n")
            
            return self.current_cost
        except Exception as e:
            print("Exception @ estimate_cost:", e)