from utils import TokenCounter
from . models import OpenAiCostEstimator, AnthropicCostEstimator, CostEstimatorConfig
import logging 

class LlmCostEstimator:
    def __init__(self):
        self.current_cost = 0
        logging.basicConfig(
            level=logging.ERROR,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        
    def update_current_cost(self, estimator_config: CostEstimatorConfig):
        """
        payload keys: input, output
        """
        try:
            self.__validate_input(estimator_config)
            
            self.current_cost = estimator_config.current_cost if self.current_cost == 0 else self.current_cost
            
            input_tokens, output_tokens = self.__get_token_count(estimator_config)
                
            input_pricing, output_pricing =  self.__set_pricing(estimator_config)

            input_cost  = input_pricing * input_tokens
            output_cost = output_pricing * output_tokens
            
            total_cost = input_cost + output_cost
            
            self.current_cost += total_cost
            
            logging.info(estimator_config.llm_provider)
            logging.info(f"input/output tokens: {input_tokens}/{output_tokens}")
            logging.info(f"Cost of this post: $ {total_cost}")
            logging.info(f"Accumulated cost:  $ {self.current_cost}")
            
            return self.current_cost
        except Exception as e:
            print("Exception @ estimate_cost:", e)
            
    def __validate_input(self, estimator_config: CostEstimatorConfig):
        if not estimator_config.is_input_str and estimator_config.input_tokens is None:
                raise ValueError("input_tokens and output_tokens must be provided if is_input_str is True")
        if estimator_config.is_input_str and estimator_config.llm_input is None:
            raise ValueError("llm_input and llm_output must be provided if is_input_str is False")
    
    def __get_token_count(self, estimator_config: CostEstimatorConfig):
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
            
        return input_tokens, output_tokens
    
    def __set_pricing(self, estimator_config: CostEstimatorConfig):
        input_pricing = OpenAiCostEstimator.pricing[estimator_config.model].input_pricing
        output_pricing = OpenAiCostEstimator.pricing[estimator_config.model].output_pricing
        
        return input_pricing, output_pricing