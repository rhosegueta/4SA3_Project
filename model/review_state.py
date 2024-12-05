#state pattern, reviewstate can be draftstate or publishedstate
class ReviewState:
    def publish(self, review):
        raise NotImplementedError
        #method must be implemented by subclasses

    def draft(self, review):
        raise NotImplementedError
        #method must be implemented by subclasses

class DraftState(ReviewState):
    def draft(self, review):
        return True
    #if publishing DraftState, convert to PublishedState
    def publish(self, review):
        review.state = PublishedState()
        return True

class PublishedState(ReviewState):
    def publish(self, review):
        return True
    #if drafting PublishedState, convert to DraftState
    def draft(self, review):
        review.state = DraftState()
        return True


