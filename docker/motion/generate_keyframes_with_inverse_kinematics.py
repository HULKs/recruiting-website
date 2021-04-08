import math
import feasibility
import inverse_kinematics
import pymunk


def generate_keyframes():
    # These keyframes are just an example, you can turn them into comments
    # Please calculate the angles and duration yourself and then return the generated keyframes
    position_0 = pymunk.Vec2d(0.5, 0.55)
    length_1 = 0.2
    length_2 = 0.2
    length_3 = 0.15
    position_keyframes = [
        {
            'position_3': pymunk.Vec2d(0.3376735890632774, 0.25),
            'rotation_3': -1.5,
            'duration': 1.05,
        },
        {
            'position_3': pymunk.Vec2d(0.73, 0.1976091315972936),
            'rotation_3': -0.4,
            'duration': 0.3,
        },
        {
            'position_3': pymunk.Vec2d(1, 0.376091315972936),
            'rotation_3': -0.3,
            'duration': 0.3,
        },
    ]
    keyframes = []
    for i, position_keyframe in enumerate(position_keyframes):
        print(
            f'Calculating inverse kinematic of position keyframe #{i + 1}...')
        set_of_joint_angles = inverse_kinematics.inverse_kinematic(
            position_0,
            position_keyframe['position_3'],
            position_keyframe['rotation_3'],
            length_1,
            length_2,
            length_3,
        )
        print(
            f'  Found {len(set_of_joint_angles)} set{"s" if len(set_of_joint_angles) != 1 else ""} of joint angles: {", ".join([f"({math.degrees(joint_angles.theta_1):.1f}°, {math.degrees(joint_angles.theta_2):.1f}°, {math.degrees(joint_angles.theta_3):.1f}°)" for joint_angles in set_of_joint_angles])}')
        feasible_set_of_joint_angles = feasibility.filter_feasible_joint_angles(
            set_of_joint_angles,
        )
        print(
            f'  Got {len(feasible_set_of_joint_angles)} feasible set{"s" if len(feasible_set_of_joint_angles) != 1 else ""} of joint angles: {", ".join([f"({math.degrees(joint_angles.theta_1):.1f}°, {math.degrees(joint_angles.theta_2):.1f}°, {math.degrees(joint_angles.theta_3):.1f}°)" for joint_angles in feasible_set_of_joint_angles])}')
        if len(feasible_set_of_joint_angles) < 1:
            raise RuntimeError(
                f'No feasible joint angles for position keyframe #{i + 1}')
        keyframes.append({
            'hip_angle': feasible_set_of_joint_angles[0].theta_1,
            'knee_angle': feasible_set_of_joint_angles[0].theta_2,
            'ankle_angle': feasible_set_of_joint_angles[0].theta_3,
            'duration': position_keyframe['duration'],
        })
    return keyframes
