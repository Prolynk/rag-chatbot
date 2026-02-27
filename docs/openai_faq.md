\# OpenAI API FAQ



\## What is the OpenAI API?

The OpenAI API gives developers access to powerful AI models like GPT-4o and GPT-4o-mini. You can use it to build chatbots, summarizers, code assistants, and more.



\## How do I get an API key?

Go to https://platform.openai.com/api-keys, log in to your OpenAI account and click "Create new secret key".



\## How does OpenAI pricing work?

OpenAI charges per token. A token is roughly 4 characters of text. GPT-4o-mini costs $0.15 per million input tokens and $0.60 per million output tokens.



\## What is GPT-4o-mini?

GPT-4o-mini is OpenAI's most affordable and efficient model. It is ideal for applications that need fast, cheap responses without sacrificing too much quality.



\## What is the context window?

The context window is the maximum amount of text a model can process in one request. GPT-4o-mini has a 128,000 token context window.



\## What are rate limits?

Rate limits control how many API requests you can make per minute. They exist to prevent abuse and ensure fair usage across all users.



\## Is my data used to train OpenAI models?

By default, OpenAI does not use API data to train its models. You can review their data usage policy at https://openai.com/policies/api-data-usage-policies.



\## What is temperature in the API?

Temperature controls the randomness of responses. A value of 0 makes responses deterministic and focused. A value of 1 makes responses more creative and varied.



\## What is the difference between GPT-4o and GPT-4o-mini?

GPT-4o is OpenAI's most capable model, better at complex reasoning and nuanced tasks. GPT-4o-mini is faster and cheaper, ideal for simpler tasks and high-volume applications.



\## How do I count tokens before sending a request?

Use the tiktoken Python library to count tokens before sending. This helps you stay within context limits and estimate costs accurately.

