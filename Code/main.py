import pandas as pd
import os
from util import query_gpt4, get_system_prompt
import argparse
import datetime
from prompts import SystemPrompt


# Main function
def main(dataset_path, output_path, perspective, limit):
    # grab api key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        return

    # create output file
    print("creating output file...")
    dataset_name = os.path.splitext(os.path.basename(dataset_path))[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"{dataset_name}_{perspective}_responses_{timestamp}.csv"
    output_path = os.path.join(output_path, output_file_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_df = pd.DataFrame(columns=["input","response", "raw_response"])

    dataset = pd.read_csv(dataset_path)
    
    if dataset.empty:
        print("No valid dataset found. Exiting.")
        return
    count = 0
    for _, entry in dataset.iterrows():
        if count > limit:
            break
        prompt = entry.to_dict()
        system_prompt = get_system_prompt(perspective)
        query = system_prompt + " " + prompt['input']
        llm_response = query_gpt4(query, api_key)
        if not llm_response:
            print("No response received. Skipping.")
            continue
        print("Response received: ", llm_response)
        output_df = pd.concat([output_df, pd.DataFrame([{
            "input": query,
            "response": llm_response.content,
            "raw_response": llm_response
        }])], ignore_index=True)
        count += 1
    
    output_df.to_csv(output_path, index=False, encoding='utf-8')
    print("Processing complete. Responses saved.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process dataset and interact with LLM.")
    # Add arguments for dataset and output paths
    parser.add_argument("--dataset_path", required=True, help="Path to the dataset file.")
    parser.add_argument("--output_dir", default="./output/responses.json", help="Directory to save the output responses.")
    parser.add_argument("--perspective", default="deontological", help="Ethical perspective to evaluate the scenarios.")
    parser.add_argument("--limit", type=int, default=100, help="Limit the number of queries to the LLM.")
    args = parser.parse_args()
    main(args.dataset_path, args.output_dir, args.perspective, args.limit)