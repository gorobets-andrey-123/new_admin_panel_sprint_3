import signal
import time

from . import enrichers, loaders, producers, states, transformers
from .pipelines import Pipeline


class Runner:
    stopped = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.stopped = True

    def run(self, pipelines: list[Pipeline]):
        while not self.stopped:
            time.sleep(1)
            print("doing something in a loop ...")


if __name__ == '__main__':
    state = states.State(states.RedisStorage())
    enricher = enrichers.Movie()
    transformer = transformers.ElasticSearchMovie()
    loader = loaders.ElasticSearchMovie(transformer)

    pipelines = [
        Pipeline(producers.PersonModified(state, conn, chunk_size), enricher, transformer, loader),
        Pipeline(producers.GenreModified(state, conn, chunk_size), enricher, transformer, loader),
        Pipeline(producers.FilmworkModified(state, conn, chunk_size), enricher, transformer, loader),
    ]

    Runner().run(pipelines)
