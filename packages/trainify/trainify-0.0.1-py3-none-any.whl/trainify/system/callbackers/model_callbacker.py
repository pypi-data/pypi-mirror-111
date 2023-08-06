from . import BaseCallbacker


class ModelCallbacker(BaseCallbacker):
    def update(self, outputs, **kwargs):
        if 'callbacks' in outputs.keys():
            self.update_values({f'model_{"validation" if self.val_mode else "training"}/{callback}': value
                                for callback, value in outputs['callbacks'].items()})
