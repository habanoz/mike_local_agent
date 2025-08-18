
class Kllm:
    def __init__(self, config):
        self.agent_llm = LLMFactory.build(config['agent'])

    def get_agent_llm(self):
        return self.agent_llm


class LLMFactory:
    @classmethod
    def build(cls, config):
        provider = config['provider']
        if provider == "ollama":
            return LLMFactory.ollama(config)
        if provider == "groq":
            return LLMFactory.groq(config)
        if provider == "together":
            return LLMFactory.together(config)
        if provider == "cohere":
            return LLMFactory.cohere(config)
        else:
            raise Exception("Unknown provider" + str(provider))
      
      
    @classmethod
    def ollama(cls, config):
        from langchain_ollama import ChatOllama
        return ChatOllama(model=config['model'],
                          base_url=config['base_url'] if "base_url" in config else "http://127.0.0.1:11434",
                          temperature=config['temperature'],
                          top_p=config.get("top_p", 0.9),
                          top_k=config.get("top_k", 40),
                          repeat_penalty=config.get("repeat_penalty", 1.0),
                          reasoning=config.get("think", False) )

    @classmethod
    def groq(cls, config):
        from langchain_groq import ChatGroq
        
        reasoning = config.get("think", False)
        if isinstance(reasoning, bool):
            reasoning = "default" if reasoning else "none"
            
        return ChatGroq(model=config['model'],
                        base_url=config.get('base_url', None),
                        temperature=config['temperature'],
                        model_kwargs={
                            "top_p":config.get("top_p", 0.9),
                            "presence_penalty":config.get("presence_penalty", 0.0), #-2,2
                        },
                        reasoning_effort=reasoning,
                        )
        
    @classmethod
    def together(cls, config):
        from langchain_together import ChatTogether
        return ChatTogether(model_name=config['model'],
                            temperature=config['temperature'],
                            top_p=config.get("top_p", 0.9),
                            presence_penalty=config.get("presence_penalty", 0.0), #-2,2
                            )

    @classmethod
    def cohere(cls, config):
        from langchain_cohere import ChatCohere
        return ChatCohere(model=config['model'],
                            temperature=config['temperature'],
                            )