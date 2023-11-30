from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    port: int
    password: str
    user: str
    database: str
    global_path: str


@dataclass
class Config:
    db: DbConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            password=env.str("DB_PASSWORD"),
            user=env.str("DB_USER"),
            database=env.str("DB_DATABASE"),
            global_path=f'postgresql+psycopg2://'
                        f'{env.str("DB_USER")}:'
                        f'{env.str("DB_PASSWORD")}@'
                        f'{env.str("DB_HOST")}:'
                        f'{env.int("DB_PORT")}/'
                        f'{env.str("DB_DATABASE")}'
        )
    )


if __name__ == "__main__":
    # PATH = '/.env'
    # services_config = load_config(PATH)
    services_config = load_config()

    print('')
