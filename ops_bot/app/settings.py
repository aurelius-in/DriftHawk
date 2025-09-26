from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  jira_base: str | None = None
  jira_user: str | None = None
  jira_token: str | None = None
  snow_instance: str | None = None
  snow_user: str | None = None
  snow_token: str | None = None
  infracost_api_key: str | None = None
  slack_webhook_url: str | None = None

  class Config:
    env_file = ".env"


settings = Settings()  # load on import


