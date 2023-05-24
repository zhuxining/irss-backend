from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the app
    """

    # Fastapi
    app_name: str = "iRss"
    app_version: str = "0.0.1"
    app_description: str = "iRss is a RSS reader"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    # Uvicorn
    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_PORT: int = 8000

    # DB
    db_url: str = "mongodb://irss-test%40wr:%5EXEwJ85TG8E%40@8.219.156.181:27017/?authSource=irss-test&readPreference=primary&ssl=false&directConnection=true"

    # Token
    token_algorithm: str = "HS256"  # 算法
    token_secret_key: str = (
        "1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk"  # 密钥 secrets.token_urlsafe(32))
    )
    token_lifetime_seconds: int = 60 * 24 * 1  # token 时效 60 * 24 * 1 = 1 天

    reset_password_token_secret: str = "1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk"
    reset_password_token_lifetime_seconds: int = 60 * 10  # 10分钟
    verification_token_secret: str = "1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk"
    verification_token_lifetime_seconds: int = 60 * 10  # 10分钟

    # Middleware
    middleware_https_redirect: bool = False
    middleware_trusted_host: bool = False
    middleware_gzip: bool = True
    middleware_cors: bool = True
    cors_origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # json_encoders = {datetime.datetime: lambda dt: dt.isoformat()}
        extra = "ignore"
        allow_population_by_field_name = True
        validate_assignment = True
        validate_all = True
        extra = "ignore"
        env_prefix = "API_"


settings = Settings()
