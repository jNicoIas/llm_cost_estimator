from helpers import LlmCostEstimator
from helpers.models import CostEstimatorConfig
import logging



if __name__ == '__main__':
    try:
        llm_cost_estimator = LlmCostEstimator(logging_level=logging.DEBUG) # You can change the log level
        
        config = CostEstimatorConfig(llm_input='You are an expert Writer', llm_output='How can I help you?', model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=True, current_cost=12)
        cost1 = llm_cost_estimator.update_current_cost(config)
        
        config = CostEstimatorConfig(llm_input='Write me an LLM poem', llm_output='I am therefore I think. -  Shooktspeare', model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=True)
        cost2 = llm_cost_estimator.update_current_cost(config)
        
        
        config = CostEstimatorConfig(input_tokens=8, output_tokens= 8, model= 'claude-3.5-sonnet', llm_provider='claude', service='sause', is_input_str=False)
        cost3 = llm_cost_estimator.update_current_cost(config)
    
    except ValueError as e:
        print(e)