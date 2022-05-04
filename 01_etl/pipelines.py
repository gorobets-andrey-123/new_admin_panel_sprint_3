from dataclasses import dataclass

from . import enrichers, loaders, producers, transformers


@dataclass
class Pipeline:
    producer: producers.Base
    enricher: enrichers.Base
    transformer: transformers.Base
    loader: loaders.Base

    def run(self):
        chunks = self.producer.produce()
        for chunk in chunks:
            last_modified = max([modified for _, modified in chunk])
            items = self.enricher.enrich([item_id for item_id, _ in chunk])
            self.loader.load(self.transformer.transform(items))
            self.producer.last_modified = last_modified
