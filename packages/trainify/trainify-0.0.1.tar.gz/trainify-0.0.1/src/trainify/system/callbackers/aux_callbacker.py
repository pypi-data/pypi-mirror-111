from . import BaseCallbacker


class AuxillaryCallbacker(BaseCallbacker):
    def update(self, lr, epoch, **kwargs):
        if self.val_mode:
            return
        self.update_values({'aux/lr': lr, 'aux/epoch': epoch})
