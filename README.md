# LLM Cost Estimator

Welcome to the LLM Cost Estimator repository! This package is designed to help you keep track of the costs associated with using large language models (LLMs) for your projects. By applying this package, you can calculate the running cost of LLM usage per project or feature and store the output in a database for further analysis and budgeting.

## Features

- **Cost Estimation**: Calculate the cost of using LLMs based on the number of tokens used or the actual messages processed.
- **Configuration Object**: Easily configure the estimator with a simple object that specifies the model, provider, and other relevant details.
- **Output in Dollars**: Get a clear understanding of your spending with costs presented in dollars.
- **Extensible Model Support**: Add new models to the cost estimation by updating the `models.py` file with the pricing details of the new model.

## Usage

To use the LLM Cost Estimator, you need to create a `CostEstimatorConfig` object with the necessary details about your LLM usage. You can specify whether you're providing the number of tokens directly or the actual messages that the LLM will process.

Here's a quick example:
```py
from helpers import LlmCostEstimator
from helpers.models import CostEstimatorConfig

llm_cost_estimator = LlmCostEstimator()

config = CostEstimatorConfig(llm_input='Wow', llm_output='Wow', model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=True, current_cost=12)
cost1 = llm_cost_estimator.update_current_cost(config)

print('==')
config = CostEstimatorConfig(llm_input='Wow', llm_output='Wow', model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=True)
cost2 = llm_cost_estimator.update_current_cost(config)


print('==')
config = CostEstimatorConfig(input_tokens=8, output_tokens= 8, model= 'gpt-4o', llm_provider='openai', service='sause', is_input_str=False)
cost3 = llm_cost_estimator.update_current_cost(config)
```


## Python Concepts Applied:
- Modularization
- OOP
- Basemodel
- Logging