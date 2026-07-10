class ResourceNotFoundException(Exception):

    def __init__(self,resource: str):
        self.resource = resource