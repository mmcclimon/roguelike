from abc import ABC, abstractmethod

class ContextDrawable(ABC):
    @abstractmethod
    def draw(self, ctx):
        pass

    @abstractmethod
    def handle_collisions(self, ctx):
        pass

    def on_collision(self, ctx):
        pass
