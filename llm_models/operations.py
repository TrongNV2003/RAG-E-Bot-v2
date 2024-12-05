import torch
from config.yaml_loader import load_config
from embedding_models.operations import EmbeddingModel
from db.elasticsearch.operations import ElasticsearchProvider
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

model = EmbeddingModel()
elasticsearch_provider = ElasticsearchProvider()
config = load_config()


class LlmModel():
    def __init__(self):
        model_name = config["model"]["llama_model"]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        
    def text_query(self, query, temperature):
        prompt = f"""<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n"""
        output = self.generate(prompt, temperature)
        return output
    
    
    def retrieve_query(self, query, temperature, threshold):
        documents = [] 
        retrieved_documents = elasticsearch_provider.embedding_search(query, threshold) # có thể thay đổi hàm embedding_search
        documents.append(retrieved_documents)
        prompt = f"""<|im_start|>user\nQuestion:{query}\nDựa vào những thông tin dưới đây để trả lời câu hỏi:\n{documents}.<|im_end|>\n<|im_start|>assistant\n"""
        output = self.generate(prompt, temperature)
        return documents, output
        
        
    def generate(self, input, temperature: float):
        inputs = self.tokenizer(input, return_tensors="pt").to(self.device)
        with torch.no_grad():
            generation_output = self.model.generate(
                inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                pad_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=512,
                temperature=temperature,
                repetition_penalty=1.1,
            ).to(self.device)
            
        output = self.tokenizer.decode(generation_output[0], skip_special_tokens=True)
        output_processed = self.process_output(output)
        return output_processed
    
    def process_output(self, output):
        response_start = output.find("<|im_start|>assistant") + len("<|im_start|>assistant")
        response = output[response_start:].strip()
        return response
        
        
    

        