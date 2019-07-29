from abc import ABC, abstractmethod

class ContextDrawable(ABC):
    @abstractmethod
    def draw(self, ctx):
        pass

    def post_loop_hook(self, ctx):
        pass
