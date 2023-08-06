from . import BasePreparator


class Renamer(BasePreparator):
    def __init__(self, rename_dict: dict):
        self.rename_dict = rename_dict

    def prepare(self, dataset, meta):
        dataset = dataset.rename(columns=self.rename_dict)
        if 'pad_map' in meta.keys():
            for key, new_key in self.rename_dict.items():
                if key in meta['pad_map'].keys():
                    meta['pad_map'][new_key] = meta['pad_map'][key]
                    del meta['pad_map'][key]
        return dataset, meta
