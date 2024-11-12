import torch
from embedding_models.operations import EmbeddingModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from db.elasticsearch.operations import ElasticsearchProvider

model = EmbeddingModel()
elasticsearch_provider = ElasticsearchProvider()

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)
class LlmModel():
    def __init__(self):
        model_name = "unsloth/Llama-3.2-1B-Instruct"
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForCausalLM.from_pretrained(model_name, 
                                                          device_map={"": 0},
                                                          use_cache = False,
                                                          cache_dir='tmp',
                                                          trust_remote_code = True,
                                                          quantization_config = bnb_config,
                                                          )
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.eval()

        
    def text_query(self, query, temperature):
        prompt = f"""<|im_start|>user\n\n{query}<|im_end|>\n<|im_start|>assistant\n\n"""
        output = self.generate(prompt, temperature)
        return output
    
    
    def retrieve_query(self, query, temperature, threshold):     
        retrieved_documents = elasticsearch_provider.embedding_search(query, threshold) # có thể thay đổi hàm embedding_search
        documents = "\n".join(retrieved_documents)
        prompt = f"""<|im_start|>user\n\n{documents}\n\nDựa vào những thông tin trên đây để trả lời câu hỏi, hãy chọn lọc thông tin để trả lời đúng trọng tâm câu hỏi.\n\n{query}<|im_end|>\n<|im_start|>assistant\n\n"""
        output = self.generate(prompt, temperature)
        return documents, output
        
        
    def generate(self, input, temperature: float):
        inputs = self.tokenizer(input, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(self.device)
        with torch.no_grad():
            generation_output = self.model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                pad_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=256,
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
        
        
    

        