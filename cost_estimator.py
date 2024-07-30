from helpers import LlmCostEstimator
from helpers.models import CostEstimatorConfig

if __name__ == '__main__':
    try:
        llm_cost_estimator = LlmCostEstimator()
        
        config = CostEstimatorConfig(llm_input='Wow', llm_output='Wow', model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=True)
        cost = llm_cost_estimator.update_current_cost(config)
        # print(cost)
        print('==')
        config = CostEstimatorConfig(llm_input='Wow', llm_output='Wow', model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=True)
        cost = llm_cost_estimator.update_current_cost(config)
        
        
        print('==')
        config = CostEstimatorConfig(input_tokens=8, output_tokens= 8, model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=False)
        cost = llm_cost_estimator.update_current_cost(config)
    
    except ValueError as e:
        print(e)