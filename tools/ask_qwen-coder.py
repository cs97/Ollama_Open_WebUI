import requests
import json


class Tools:
    def __init__(self):
        self.ollama_url = "http://ollama:11434/api/generate"
        # self.ollama_url = "http://host.docker.internal:11434/api/generate"
        self.coder_model = "qwen2.5-coder:0.5b"

    def ask_coder_expert(self, task_description: str) -> str:
        """
        Delegates programming tasks to the Qwen-Coder expert.
        INSTRUCTION FOR THE MANAGER: Please translate the user's request into precise technical English before passing it to this tool.
        :param task_description: The technical task description:
        """

        system_instructions = (
            "You are an expert Senior Developer. Please solve the following task. "
            "Write the code and all technical explanations in English for maximum precision. "
            "Focus on memory safety and idiomatic Rust (if applicable).\n\n"
        )

        full_prompt = f"{system_instructions}Task to solve: {task_description}"

        payload = {
            "model": self.coder_model,
            "prompt": full_prompt,
            "stream": False,
            # "options": {
            #    "temperature": 0.1,
            # "num_ctx": 8192,
            # },
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()
            output = result.get("response", "No response received.")

            #return f"--- {self.coder_model} ---\n\n{output}"
            return output
      
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Qwen-Coder: {str(e)}"
