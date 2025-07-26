import torch
from typing import List
from sentence_transformers import SentenceTransformer

from rag.config.setting import llm_config

class EmbeddingModel:
    def __init__(self):
        self.model_name = llm_config.embeddings_model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(self.model_name, device=self.device)

    def _embedding_batch(self, documents: List[str]) -> List[List[float]]:
        try:
            embeddings = self.model.encode(
                documents,
                show_progress_bar=False,
                batch_size=32,
                normalize_embeddings=True
            )
            return embeddings.tolist()
        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings for batch: {str(e)}")

    def embedding(self, query: str) -> List[float]:
        embeddings = self._embedding_batch([query])
        return embeddings[0]


    # def _pool(self, hidden_states: torch.Tensor, attention_mask: torch.Tensor, pooling_type: str = "cls") -> torch.Tensor:
    #     # [batch_size, seq_len, hidden_size]
    #     if pooling_type == "mean":
    #         input_mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size()).float()
    #         sum_embeddings = torch.sum(hidden_states * input_mask_expanded, 1)
    #         sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    #         pooled = sum_embeddings / sum_mask
    #     elif pooling_type == "max":
    #         input_mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size()).float()
    #         hidden_states[input_mask_expanded == 0] = -1e9
    #         pooled = torch.max(hidden_states, 1)[0]
    #     elif pooling_type == "cls":
    #         if hidden_states.shape[1] > 0:
    #             pooled = hidden_states[:, 0, :]
    #     else:
    #         pooled = hidden_states[:, 0]
    #     return pooled