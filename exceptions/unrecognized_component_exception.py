class UnrecognizedComponentException(Exception):
    def __init__(self, component_type):
        self.component_type = component_type
        message = f"Unrecognized component type: {component_type}"
        super().__init__(message)