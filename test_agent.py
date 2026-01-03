from src.agent.graph import app_agent

inputs = {"question": "What are the symptoms of Citrus Canker?"}
result = app_agent.invoke(inputs)

print(f"Intent: {result['intent']}")
print(f"Answer: {result['answer']}")