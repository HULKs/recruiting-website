import math
import pymunk
import scene


def forward_kinematics(position_0: pymunk.Vec2d,
                       theta_1: float,
                       length_1: float,
                       theta_2: float,
                       length_2: float,
                       theta_3: float,
                       length_3: float):
    theta_1_with_offset = theta_1 - math.radians(45)
    position_1 = pymunk.Vec2d(
        position_0.x + math.cos(theta_1_with_offset) * length_1,
        position_0.y + math.sin(theta_1_with_offset) * length_1,
    )
    theta_2_with_offset = theta_1_with_offset + theta_2 - math.radians(90)
    position_2 = pymunk.Vec2d(
        position_1.x + math.cos(theta_2_with_offset) * length_2,
        position_1.y + math.sin(theta_2_with_offset) * length_2,
    )
    theta_3_with_offset = theta_2_with_offset + theta_3 + math.radians(111.61)
    position_3 = pymunk.Vec2d(
        position_2.x + math.cos(theta_3_with_offset) * length_3,
        position_2.y + math.sin(theta_3_with_offset) * length_3,
    )
    return position_1, position_2, position_3, theta_3_with_offset


# calculate position_3 with forward kinematics
theta_0 = math.radians(0)
theta_1 = math.radians(0)
theta_2 = math.radians(0)
position_0 = pymunk.Vec2d(0.5, 0.55)
length_0 = 0.2
length_1 = 0.2
length_2 = 0.15
position_1, position_2, position_3, rotation_3 = forward_kinematics(
    position_0,
    theta_0,
    length_0,
    theta_1,
    length_1,
    theta_2,
    length_2,
)

# drawing
joint_draw_radius = 0.0175
joint_draw_thickness = 0.01
position_offset = pymunk.Vec2d(0.05, 0)
s = scene.Scene(1, 0.65, 720)
s.draw_line(pymunk.Vec2d(0.5, 0.65), position_0, joint_draw_thickness, '#888')
s.draw_circle(position_0, joint_draw_radius, '#000')
s.draw_line(position_0, position_1, joint_draw_thickness, '#000')
s.draw_circle(position_1, joint_draw_radius, '#000')
s.draw_line(position_1, position_2, joint_draw_thickness, '#000')
heel_position = position_2 + \
    pymunk.Vec2d(0.1, 0).rotated(rotation_3 + math.radians(23.39+180+39))
s.draw_line(position_2, heel_position, joint_draw_thickness, '#888')
s.draw_line(heel_position, position_3, joint_draw_thickness, '#888')
s.draw_circle(position_2, joint_draw_radius, '#000')
s.draw_line(position_2, position_3, joint_draw_thickness, '#000')
s.draw_circle(position_3, joint_draw_radius, '#000')
s.draw_text(
    f'position_0: ({position_0.x:.2f}, {position_0.y:.2f})\ntheta_0: {math.degrees(theta_0):.1f}°',
    position_0 - position_offset, '#000', 'rm')
s.draw_text(
    f'position_1: ({position_1.x:.2f}, {position_1.y:.2f})\ntheta_1: {math.degrees(theta_1):.1f}°',
    position_1 + position_offset, '#000', 'lm')
s.draw_text(
    f'position_2: ({position_2.x:.2f}, {position_2.y:.2f})\ntheta_2: {math.degrees(theta_2):.1f}°',
    position_2 - position_offset, '#000', 'rm')
s.draw_text(
    f'position_3: ({position_3.x:.2f}, {position_3.y:.2f})\nrotation_3: {math.degrees(rotation_3):.1f}°',
    position_3 + position_offset, '#000', 'lm')
s.save_png('forward_kinematics.png')
