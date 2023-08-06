from pydantic import BaseSettings


class Settings(BaseSettings):
    AWS_SNS_KEY: str = None
    AWS_SNS_SECRET: str = None
    AWS_SNS_PATH: str = 'arn:aws:sns:ap-southeast-1:580482583062:'

    class Config:
        case_sensitive = True

        fields = {
            'AWS_SNS_KEY': {'env': 'AWS_SNS_KEY'},
            'AWS_SNS__SECRET': {'env': 'AWS_SNS__SECRET'},
            'AWS_SNS_PATH': {'env': 'AWS_SNS_PATH'},
        }


settings = Settings()
