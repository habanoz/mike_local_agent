
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
        return ChatGroq(model=config['model'],
                        base_url=config.get('base_url', None),
                        temperature=config['temperature'],
                        top_p=config.get("top_p", 0.9),
                        presence_penalty=config.get("presence_penalty", 0.0), #-2,2
                        reasoning_effort="default" if config.get("think", False) else "none",
                        )