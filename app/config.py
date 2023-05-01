from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the app
    """

    app_name: str = "iRss"
    app_version: str = "0.0.1"
    app_description: str = "a rss reader"

    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    db_url: str = "mongodb://irss-test%40wr:%5EXEwJ85TG8E%40@8.219.156.181:27017/?authSource=irss-test&readPreference=primary&ssl=false&directConnection=true"

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
