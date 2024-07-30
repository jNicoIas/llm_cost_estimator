# from datetime import time


import tiktoken


class TokenCounter:    
    def __init__(self, payload:dict, model:str = 'gpt-4-1106-preview'):
        """
        Counts the number of tokens in the payload message
        :param:     payload     -> dict
        :return:    num_tokens  -> int
        """
        self.payload    = payload
        self.model      = model
        self.num_tokens = 0
              
    def num_tokens_from_messages(self) -> int: 
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")

        try:
            # gpt vision counts tokens differently because its inputs contain texts and images
            # if self.model == "gpt-4-vision-preview":
            #     return self.__num_tokens_from_vision(encoding)
            # dall-e doesn't need tokens because it limits rate only based on number of images generated
            if self.model == "dall-e-2" or self.model == "dall-e-3":
                self.num_tokens = self.payload['n'] 
                return self.num_tokens
            
            elif self.model == "text-embedding-3-small":
               return self.__num_tokens_from_embeddings(encoding)
            
            else:
                return self.__num_tokens_from_chat(encoding)
        except Exception as e:
            print("Exception num tokens: ", e)
     
    def __num_tokens_from_chat(self, encoding) -> str:
        try:
            messages = self.payload['messages'] # zpao
            for message in messages:
                self.num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    self.num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        self.num_tokens += (
                            -1
                        )  # role is always required and always 1 token
            self.num_tokens += 2  # every reply is primed with <im_start>assistant
            return self.num_tokens
        except Exception as e:
            print("Exception @ __num_tokens_from_chat:", e)
        
    def __num_tokens_from_vision(self, encoding) -> int:
        messages = self.payload['messages'] # zpao
        for message in messages:
            for key, value in message.items():
                if isinstance(value, list):
                    for item in value:
                        self.num_tokens += len(encoding.encode(item["type"]))
                        if item["type"] == "text":
                            self.num_tokens += len(encoding.encode(item["text"]))
                        elif item["type"] == "image_url":
                            self.num_tokens += calculate_image_token_cost(
                                item["image_url"]["url"],
                                item["image_url"]["detail"],
                            )
                elif isinstance(value, str):
                    self.num_tokens += len(encoding.encode(value))
        self.num_tokens += 3  # every reply is primed with assistant
        return self.num_tokens
            
    def __num_tokens_from_embeddings(self, encoding) -> int:
       
        messages =  [{"role": "system", "content": self.payload['input']},] 
        for message in messages:
            self.num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                self.num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    self.num_tokens += (
                        -1
                    )  # role is always required and always 1 token
        self.num_tokens += 2  # every reply is primed with <im_start>assistant
        return self.num_tokens
     