import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger("elasticsearch_log")

def connect_db() -> Elasticsearch:
    try:
        # Kết nối đến Elasticsearch
        client = Elasticsearch("https://192.168.56.1:9200/",
                               http_auth=('elastic', 'a2XFW5LCbIrqPTA5n9a6'), 
                               timeout=10, 
                               max_retries=5, 
                               retry_on_timeout=True,
                               verify_certs=False,
                               ssl_show_warn=False)
        # # Kiểm tra xem Elasticsearch đã sẵn sàng chưa
        # if client.ping():
        #     logger.info(f"Connected to Elasticsearch ({host}:{port})")
        # else:
        #     logger.error(f"Failed to connect to Elasticsearch ({host}:{port}): Cluster is not reachable.")
        
        return client
        
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch {e}")
        