import signal
import time
from dataclasses import dataclass

import psycopg2
import redis

import enrichers
import loaders
import producers
import settings
import states
import transformers
from pipelines import Pipeline


@dataclass
class Runner:
    pipelines: list[Pipeline]
    check_interval_sec: int
    _stopped: bool = False

    def __post_init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self):
        self._stopped = True

    def run(self):
        while not self._stopped:
            for pipeline in self.pipelines:
                pipeline.execute()
            time.sleep(self.check_interval_sec)


def init_etl():
    with psycopg2.connect(**settings.PG_DSL) as conn:
        storage = states.RedisStorage(redis=redis.Redis(**settings.REDIS_DSL), key=settings.STORAGE_STATE_KEY)
        state = states.State(storage)
        enricher = enrichers.Movie(conn)
        transformer = transformers.ElasticSearchMovie()
        loader = loaders.ElasticSearchMovie(transformer)

        pipelines = [
            Pipeline(producers.PersonModified(state, conn, settings.CHUNK_SIZE), enricher, transformer, loader),
            Pipeline(producers.GenreModified(state, conn, settings.CHUNK_SIZE), enricher, transformer, loader),
            Pipeline(producers.FilmworkModified(state, conn, settings.CHUNK_SIZE), enricher, transformer, loader),
        ]

        Runner(pipelines=pipelines, check_interval_sec=settings.CHECK_INTERVAL_SEC).run()


if __name__ == '__main__':
    init_etl()
