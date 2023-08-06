import torch

from . import BaseCallbacker


class AccuracyCallbacker(BaseCallbacker):
    @staticmethod
    def accuracy(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        preds = torch.argmax(logits.view((-1, logits.shape[-1])), dim=-1)
        labels = labels.flatten()
        acc = (preds == labels).sum().float() / len(labels)
        return acc

    def update(self, outputs, **kwargs):
        logits = outputs.get('logits')
        labels = outputs.get('labels')
        assert logits is not None, 'to use AccuracyCallbacker, model should have "logits" key in outputs'
        assert labels is not None, 'to use AccuracyCallbacker, model should have "labels" key in outputs'
        self.update_values({f"{'validation' if self.val_mode else 'training'}/accuracy": self.accuracy(logits, labels)})
