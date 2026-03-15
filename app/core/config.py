import configparser
import os
from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[str] = None
    db_name: Optional[str] = None
    database_url_env: Optional[str] = None
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def database_url(self) -> str:
        # Prioritize single URL environment variable (common in Vercel/Neon/Supabase)
        if self.database_url_env:
            # Vercel's Postgres URL might start with postgres://, SQLAlchemy async needs postgresql+asyncpg://
            url = self.database_url_env
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        
        # Fallback to individual components
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

def load_settings() -> Settings:
    # 1. Try environment variables first (for Vercel/Production/External DB)
    db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or os.getenv("NILEDB_URL")
    secret = os.getenv("SECRET_KEY")
    
    if db_url and secret:
        return Settings(
            database_url_env=db_url,
            secret_key=secret,
            algorithm=os.getenv("ALGORITHM", "HS256"),
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        )

    # 2. Fallback to config.properties (for Local Dev)
    config = configparser.ConfigParser()
    # Check current directory first, then look one level up if needed
    config_paths = [
        "config.properties",
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.properties")
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            config.read(path)
            return Settings(
                db_user=config.get("database", "db_user"),
                db_password=config.get("database", "db_password"),
                db_host=config.get("database", "db_host"),
                db_port=config.get("database", "db_port"),
                db_name=config.get("database", "db_name"),
                secret_key=config.get("security", "secret_key"),
                algorithm=config.get("security", "algorithm"),
                access_token_expire_minutes=config.getint("security", "access_token_expire_minutes")
            )
    
    # If no config.properties, but we have the DB info from environment (even without SECRET_KEY for testing)
    if db_url:
        return Settings(
            database_url_env=db_url,
            secret_key="dev_secret_key_change_me", # Fallback for local testing if env var missing
            algorithm="HS256",
            access_token_expire_minutes=30
        )
    
    raise ValueError("No configuration found. Set DATABASE_URL/POSTGRES_URL/NILEDB_URL and SECRET_KEY env vars or provide config.properties")

settings = load_settings()
