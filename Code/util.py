import json
from openai import OpenAI
from prompts import SystemPrompt

# Query LLM
def query_gpt4(prompt, api_key):
    client = OpenAI(api_key=api_key)
    print("Querying LLM with prompt: ", prompt)
    try:
        response =  client.chat.completions.create(
            model="gpt-4", 
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message
    except Exception as e:
        print(f"Error querying LLM: {e}")
        return ""

def get_system_prompt(perspective):
    system_prompt = ""
    match perspective:
        case "deontological":
            system_prompt = SystemPrompt.DEONTOLOGY.value
        case "consequentialist":
            system_prompt = SystemPrompt.CONSEQUENTIALISM.value
        case "virtue ethics":
            system_prompt = SystemPrompt.VIRTUE_ETHICS.value
        case _:
            print(f"Unknown ethical perspective: {perspective}. Using default.")
            system_prompt = SystemPrompt.DEONTOLOGY.value
    return system_prompt

# Query LLM in batch

def query_llm_batch(client, prompts_df, system_task_prompt):
    # Creating tasks for batch processing
    tasks = []
    for index, row in prompts_df.iterrows():
        description = row['input']
        task = {
            "custom_id": f"task-{index}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "temperature": 0,
                "response_format": { 
                    "type": "json_object"
                },
                "messages": [
                    {
                        "role": "system",
                        "content": system_task_prompt
                    },
                    {
                        "role": "user",
                        "content": description
                    }
                ],
            }
        }
        tasks.append(task)

    # writing tasks to a file
    file_name = "data/batch.jsonl"
    with open(file_name, 'w') as file:
        for obj in tasks:
            file.write(json.dumps(obj) + '\n')
    
    # Creating a batch job
    batch_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
    )
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    print("Batch created with batch id: ", batch_job.id)