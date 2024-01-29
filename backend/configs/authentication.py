from fastapi.security import APIKeyHeader

auth_key_header = APIKeyHeader(name="Authorization")