import logging
from elasticsearch import Elasticsearch

from rag.config.setting import elasticsearch_config

logger = logging.getLogger("elasticsearch_log")

def connect_db() -> Elasticsearch:
    try:
        client = Elasticsearch([{"host": elasticsearch_config.host, 
                                 "port": elasticsearch_config.port, 
                                 "scheme": "https"}],
                               http_auth=(
                                   elasticsearch_config.http_auth.username,
                                   elasticsearch_config.http_auth.password,
                                ), 
                               timeout=10, 
                               max_retries=5, 
                               retry_on_timeout=True,
                               verify_certs=False,
                               ssl_show_warn=False)

        return client
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch {e}")
        