import sim.util, sim, os, sys

class CoreStatePredictor:
    def __init__(self, sampling_period, observation_window):
        self.sampling_period = sampling_period
        self.observation_window = observation_window
        self.core_state = {}

    def predict_state(self, core_id, current_state, pc, predicted, actual, indirect):
        # Ensure we have a history for this core
        if core_id not in self.core_state:
            self.core_state[core_id] = {'history': [], 'confidence': 0}

        # Record the state (idle or running)
        self.core_state[core_id]['history'].append(current_state)

        # Limit the history size to the observation window
        if len(self.core_state[core_id]['history']) > self.observation_window:
            self.core_state[core_id]['history'].pop(0)

        # Predict the state based on history
        predicted_state = self._predict_core_state(core_id)

        # Set frequency based on predicted state
        frequency = self._set_frequency(predicted_state)

        return frequency

    def _predict_core_state(self, core_id):
        # A more sophisticated prediction: track transitions instead of just counts
        history = self.core_state[core_id]['history']

        # Track transitions to identify state changes
        if len(history) < 2:
            return 'running'  # Default to 'running' if not enough history

        # Check the most recent two states to identify transitions
        recent_states = history[-2:]
        if recent_states == ['idle', 'running']:
            return 'running'
        elif recent_states == ['running', 'idle']:
            return 'idle'

        # Fallback to simple count method if no recent transition detected
        if history.count('idle') > history.count('running'):
            return 'idle'
        return 'running'

    def _set_frequency(self, predicted_state):
        if predicted_state == 'idle':
            return 1.0  # Low frequency for idle state
        else:
            return 3.0  # High frequency for running state


# Global variables
PREDICTOR = CoreStatePredictor(sampling_period=200, observation_window=10)

# Callback function for branch prediction
def hook_branch_predict(ip, predicted, actual, indirect, core_id):
    # Get the current state from branch predictor information
    current_state = "running" if actual == predicted else "idle"

    # Make the prediction and set the frequency
    frequency = PREDICTOR.predict_state(core_id, current_state, ip, predicted, actual, indirect)

    # Log or set the core frequency in the simulation
    print(f"Core {core_id}: Predicted State = {current_state}, Set Frequency = {frequency} GHz")

    return frequency


# Hook the callback into Sniper
sim.util.EveryBranch(hook_branch_predict)
