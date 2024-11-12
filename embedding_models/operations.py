import torch
from transformers import AutoTokenizer, AutoModel

class EmbeddingModel():
    def __init__(self):
        self.model_name = "Trongdz/roberta-embeddings-auto-labeling-tasks"
        self.model = AutoModel.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        self.pooling_type = "mean"

    def pool(self, hidden_states, attention_mask):  # [batch_size, seq_len, hidden_size]
        if self.pooling_type == "mean":
            hidden_states = hidden_states * attention_mask[:, :, None]
            pooled = hidden_states.mean(dim=1) / attention_mask.sum(dim=-1, keepdim=True)
        elif self.pooling_type == "max":
            pooled = hidden_states.max(dim=1)
        else:
            pooled = hidden_states[:, 0]
        return pooled
    
    def embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = self.pool(outputs.last_hidden_state, inputs.attention_mask)[0].tolist()
        return embedding
    
    def embedding_query(self, query):
        inputs = self.tokenizer(query, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0].tolist()
        return embedding
