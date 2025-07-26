from enum import Enum
from pydantic import Field
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class LLMConfig(BaseSettings):
    base_url: str = Field(
        description="Base URL for OpenAI API",
        alias="LLM_URL",
    )
    api_key: str = Field(
        description="API key for OpenAI",
        alias="LLM_KEY",
    )
    llm_model: str = Field(
        description="Model name to be used (e.g., GPT-4)",
        alias="LLM_MODEL",
    )
    embeddings_model: str = Field(
        default="hiieu/halong_embedding",
        alias="EMBEDDINGS_MODEL",
        description="Model name for embeddings",
    )
    temperature: float = Field(
        default=0.6,
        description="Sampling temperature; higher values make output more random",
        alias="TEMPERATURE",
    )
    max_tokens: int = Field(
        default=1024,
        alias="MAX_TOKENS",
        description="Maximum number of tokens for API responses",
    )
    top_p: float = Field(
        default=0.95,
        alias="TOP_P",
        description="Nucleus sampling parameter; higher values increase randomness",
    )
    seed: int = Field(
        default=42,
        alias="SEED",
        description="Random seed for sampling"
    )


class ElasticsearchConfig(BaseSettings):
    host: str = Field(
        default="localhost",
        alias="ELASTICSEARCH_HOST",
        description="Elasticsearch host address"
    )
    port: int = Field(
        default=9200,
        alias="ELASTICSEARCH_PORT",
        description="Elasticsearch port number"
    )
    index_name: str = Field(
        default="text_embeddings",
        alias="ELASTICSEARCH_INDEX",
        description="Elasticsearch index name"
    )
    username: str = Field(
        default="elastic",
        alias="ELASTICSEARCH_USERNAME",
        description="Elasticsearch username"
    )
    password: str = Field(
        alias="ELASTICSEARCH_PASSWORD",
        description="Elasticsearch password"
    )


class MongoDBConfig(BaseSettings):
    mongodb_uri: str = Field(
        description="MongoDB URI for connecting to the database",
        alias='MONGODB_URI'
    )
    db_name: str = Field(
        default='rag_db',
        description="Name of the MongoDB database"
    )
    collection_name: str = Field(
        default='vector_store',
        description="Name of the MongoDB collection for certificates"
    )
    user_collection_name: str = Field(
        default='users',
        description="Name of the MongoDB collection for user accounts"
    )
    admin_collection_name: str = Field(
        default='admins',
        description="Name of the MongoDB collection for admin accounts"
    )
    admin_log_collection_name: str = Field(
        default='admin_logs',
        description="Name of the MongoDB collection for admin logs"
    )

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

llm_config = LLMConfig()
mongo_config = MongoDBConfig()
elasticsearch_config = ElasticsearchConfig()
