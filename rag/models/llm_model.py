from openai import OpenAI
from typing import List, Optional

from rag.db.elasticsearch.operations import ElasticsearchProvider
from rag.prompts.template import SYSTEM_PROMPT, TEMPLATE_PROMPT
from rag.config.setting import llm_config, Role
from rag.utils.utils import parse_response

class LlmModel:
    def __init__(
        self,
        llm: Optional[OpenAI] = None,
        prompt_template: Optional[str] = TEMPLATE_PROMPT
    ) -> None:
        self.prompt_template = prompt_template
        if llm is None:
            llm = OpenAI(api_key=llm_config.api_key, base_url=llm_config.base_url)
        self.llm = llm
        self.elasticsearch_provider = ElasticsearchProvider()

    def generate(self, prompt: str) -> str:
        response = self.llm.chat.completions.create(
            seed=llm_config.seed,
            temperature=llm_config.temperature,
            top_p=llm_config.top_p,
            model=llm_config.llm_model,
            messages=[
                {"role": Role.SYSTEM, "content": SYSTEM_PROMPT},
                {"role": Role.USER, "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        return parse_response(content)

    def inject_prompt(
        self,
        text: str,
        history: Optional[str] = "",
        retrieval_documents: Optional[str] = "",
    ) -> str:
        prompt_str = self.prompt_template.format(
            text=text,
            history=history,
            retrieval_documents=retrieval_documents,
        )
        return prompt_str

    def run(
        self,
        query: str,
        top_k: int,
        is_retrieval: bool,
        chat_history: str = "",
        bm25_boost: float = 1.0,
        vector_boost: float = 1.0,
    ) -> tuple[List[str], str]:
        documents = []
        if is_retrieval:
            retrieved_documents = self.elasticsearch_provider.hybrid_search(query, top_k, bm25_boost, vector_boost)
            documents.append(retrieved_documents)

        prompt = self.inject_prompt(
            text=query,
            history=chat_history,
            retrieval_documents=documents
        )
        response = self.generate(prompt)
        return documents, response
