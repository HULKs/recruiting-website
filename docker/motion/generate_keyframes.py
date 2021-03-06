import math

def generate_keyframes():
    # These keyframes are just an example, you can turn them into comments
    # Please calculate the angles and duration yourself and then return the generated keyframes
    keyframes = [
        {'hip_angle': -math.pi / 2, 'knee_angle': -math.pi /
            2, 'ankle_angle': -math.pi / 2, 'duration': 1},
        {'hip_angle': -math.pi / 2, 'knee_angle': -math.pi /
            2, 'ankle_angle': 0, 'duration': 1},
        {'hip_angle': 0, 'knee_angle': -math.pi /
            2, 'ankle_angle': 0, 'duration': 0.5},
        {'hip_angle': math.pi / 4, 'knee_angle': math.pi / 8, 'ankle_angle': -math.pi, 'duration': 0.1},
        {'hip_angle': math.pi / 4, 'knee_angle': math.pi / 8, 'ankle_angle': -math.pi, 'duration': 0.5},
    ]
    return keyframes
