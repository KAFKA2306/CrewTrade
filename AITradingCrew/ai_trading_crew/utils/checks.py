import tiktoken



class ValidationChecks:
    def __init__(self):
        pass


    def get_llm_for_task(self,
                           crew_instance,
                           context_data, 
                           llm_to_validate,
                           default_llm_for_task,
                           task_type : str,
                           max_tokens: int = 8196,
                           rejected_llms = ["together_ai/deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"]) -> str:


        if rejected_llms and llm_to_validate.model in rejected_llms:
            return default_llm_for_task

        task_config = crew_instance.tasks_config[task_type].copy()
        description = task_config.get("description", "")
        prompt = task_config.get("prompt", "")
        expected_output = task_config.get("expected_output", "")
        
        if context_data:
            description += f" {context_data}"
        
        combined_text = f"{description} {prompt} {expected_output}"
        
        print(combined_text)

        try:
            encoding = tiktoken.encoding_for_model(llm_to_validate.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        token_count = len(encoding.encode(combined_text))
        
        # Return the appropriate LLM based on token count
        return default_llm_for_task if token_count > (max_tokens/2) else llm_to_validate