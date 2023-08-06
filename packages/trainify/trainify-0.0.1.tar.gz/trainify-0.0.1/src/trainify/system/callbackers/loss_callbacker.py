from .base_callbacker import BaseCallbacker


class LossCallbacker(BaseCallbacker):
    def update(self, outputs, **kwargs):
        if not self.val_mode:
            self.update_values({'loss/training': outputs['loss']})
        else:
            self.update_values({'loss/validation': outputs['loss']})

        if 'losses' in outputs.keys():
            losses = outputs['losses']
            self.update_values({
                f"{task}/{'validation' if self.val_mode else 'training'}/{head}/loss":
                    losses[task][head] for task in losses.keys() for head in losses[task]
            })
