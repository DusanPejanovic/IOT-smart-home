class ControllerRegistry:
    controllers = []

    @staticmethod
    def register(controller):
        ControllerRegistry.controllers.append(controller)

    @staticmethod
    def print_controllers():
        controllers_by_pi = {}
        for controller in ControllerRegistry.controllers:
            pi_id = controller.pi_id
            if pi_id not in controllers_by_pi:
                controllers_by_pi[pi_id] = []
            controllers_by_pi[pi_id].append(controller)

        print("**********Created Components**********")
        for pi_id, controllers in sorted(controllers_by_pi.items()):
            print(f"Pi: {pi_id}")
            for controller in sorted(controllers, key=lambda c: c.__class__.__name__):
                print(
                    f" - {controller.component_id} ({controller.settings['type']}, Simulated: {controller.settings['simulated']})")
