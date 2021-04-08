import collections
import math
import pymunk
import scene
import typing


JointAngles = collections.namedtuple(
    'JointAngles',
    ['theta_1', 'theta_2', 'theta_3'],
)


def inverse_kinematic(position_0: pymunk.Vec2d, position_3: pymunk.Vec2d, rotation_3: float,
                      length_1: float, length_2: float, length_3: float) -> typing.List[JointAngles]:
    # calculate position_2 and distance between position_0 and position_2
    position_2 = pymunk.Vec2d(
        position_3.x - math.cos(rotation_3) * length_3,
        position_3.y - math.sin(rotation_3) * length_3,
    )
    distance_0_to_2 = math.dist(position_2, position_0)
    # select corresponding case 1, 2, or 3
    if distance_0_to_2 > length_1 + length_2:
        # no solution exists: distance between position_0 and position_2 cannot be reached
        return []
    elif distance_0_to_2 == length_1 + length_2:
        # one solution exists: position_1 must be on line between position_0 and position_2
        theta_2 = 0
        theta_2_with_offset = theta_2 + math.radians(90)
        theta_1 = math.atan2(
            position_2.y - position_0.y,
            position_2.x - position_0.x,
        )
        theta_1_with_offset = theta_1 + math.radians(45)
        theta_3 = rotation_3 - theta_1 - theta_2
        theta_3_with_offset = theta_3 - math.radians(111.61)

        return [
            JointAngles(
                theta_1_with_offset,
                theta_2_with_offset,
                theta_3_with_offset,
            ),
        ]
    else:  # distance_0_to_2 < length_1 + length_2
        # two solutions exists: length_1 and length_2 are too long, need to bend at position_1
        theta_1_1 = math.atan2(
            position_2.y - position_0.y,
            position_2.x - position_0.x,
        )
        theta_1_2 = math.acos(
            (distance_0_to_2 ** 2 + length_1 ** 2 - length_2 ** 2) /
            (2 * distance_0_to_2 * length_1),
        )
        first_theta_1 = theta_1_1 - theta_1_2
        second_theta_1 = theta_1_1 + theta_1_2
        first_theta_1_with_offset = first_theta_1 + math.radians(45)
        second_theta_1_with_offset = second_theta_1 + math.radians(45)

        theta_2_1 = math.acos(
            (length_1 ** 2 + length_2 ** 2 - distance_0_to_2 ** 2) /
            (2 * length_1 * length_2),
        )
        first_theta_2 = math.pi - theta_2_1
        second_theta_2 = theta_2_1 - math.pi
        first_theta_2_with_offset = first_theta_2 + math.radians(90)
        second_theta_2_with_offset = second_theta_2 + math.radians(90)

        first_theta_3 = rotation_3 - first_theta_1 - first_theta_2
        second_theta_3 = rotation_3 - second_theta_1 - second_theta_2
        first_theta_3_with_offset = first_theta_3 - math.radians(111.61)
        second_theta_3_with_offset = second_theta_3 - math.radians(111.61)

        return [
            JointAngles(
                first_theta_1_with_offset,
                first_theta_2_with_offset,
                first_theta_3_with_offset,
            ),
            JointAngles(
                second_theta_1_with_offset,
                second_theta_2_with_offset,
                second_theta_3_with_offset,
            ),
        ]


if __name__ == '__main__':
    # calculate joint angles with inverse kinematics
    position_0 = pymunk.Vec2d(0.5, 0.55)
    position_3 = pymunk.Vec2d(0.7376735890632774, 0.1976091315972936)
    rotation_3 = -0.4082325120414736
    length_1 = 0.2
    length_2 = 0.2
    length_3 = 0.15
    set_of_joint_angles = inverse_kinematic(
        position_0, position_3, rotation_3, length_1, length_2, length_3)

    # console output
    output = f'{len(set_of_joint_angles)} solutions for position_3: ({position_3.x:.2f}, {position_3.y:.2f}), rotation_3: {math.degrees(rotation_3):.1f}°'
    if len(set_of_joint_angles) > 0:
        output += ':'
        for index, joint_angles in enumerate(set_of_joint_angles):
            output += f'\n  #{index + 1}: theta_1: {math.degrees(joint_angles.theta_1):.1f}°, theta_2: {math.degrees(joint_angles.theta_2):.1f}°, theta_3: {math.degrees(joint_angles.theta_3):.1f}°'
    print(output)

    # drawing
    joint_draw_radius = 0.0175
    joint_draw_thickness = 0.01
    s = scene.Scene(1.1333, 0.6, 720)
    s.draw_line(pymunk.Vec2d(0.5, 0.6), position_0,
                joint_draw_thickness, '#888')
    s.draw_circle(position_0, joint_draw_radius, '#000')
    position_2 = pymunk.Vec2d(
        position_3.x - math.cos(rotation_3) * length_3,
        position_3.y - math.sin(rotation_3) * length_3,
    )
    for index, joint_angles in enumerate(set_of_joint_angles):
        theta_1_with_offset = joint_angles.theta_1 - math.radians(45)
        position_1 = pymunk.Vec2d(
            position_0.x + math.cos(theta_1_with_offset) * length_1,
            position_0.y + math.sin(theta_1_with_offset) * length_1,
        )
        s.draw_line(position_0, position_1, joint_draw_thickness, '#000')
        s.draw_circle(position_1, joint_draw_radius, '#000')
        s.draw_line(position_1, position_2, joint_draw_thickness, '#000')
        s.draw_text(f'#{index + 1}', position_1, '#fff', 'mm')
    if len(set_of_joint_angles) == 0:
        s.draw_text('no solutions', pymunk.Vec2d(
            0.5, s.height/2), '#000', 'mm')
    else:
        heel_position = position_2 + \
            pymunk.Vec2d(0.1, 0).rotated(
                rotation_3 + math.radians(23.39+180+39))
        s.draw_line(position_2, heel_position, joint_draw_thickness, '#888')
        s.draw_line(heel_position, position_3, joint_draw_thickness, '#888')
        s.draw_circle(position_2, joint_draw_radius, '#000')
        s.draw_line(position_2, position_3, joint_draw_thickness, '#000')
        s.draw_circle(position_3, joint_draw_radius, '#000')
    s.draw_text(output, pymunk.Vec2d(0.01, 0.0825), '#000', 'la')
    s.save_png('inverse_kinematics.png')
