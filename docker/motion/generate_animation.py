import math
import typing
import pymunk
import pymunk.constraints
from PIL import Image, ImageDraw, ImageFont
import generate_keyframes
from configuration import *

font = ImageFont.truetype('JetBrainsMono-Regular.ttf', 14)
body_sprite = Image.open(body_sprite_path)
thigh_sprite = Image.open(thigh_sprite_path)
tibia_sprite = Image.open(tibia_sprite_path)
foot_sprite = Image.open(foot_sprite_path)
leg_sprite = Image.open(leg_sprite_path)
ball_sprite = Image.open(ball_sprite_path)
ball_shadow_sprite = Image.open(ball_shadow_sprite_path)
ghost_ball_sprite = Image.open(ghost_ball_sprite_path)
ghost_ball_shadow_sprite = Image.open(ghost_ball_shadow_sprite_path)
target_sprite = Image.open(target_sprite_path)

ground_sprite = Image.open(ground_sprite_path)
ground_sprite_height = int(
    space_width * pixel_scale / ground_sprite.size[0] * ground_sprite.size[1])
ground_sprite = ground_sprite.resize(
    (space_width * pixel_scale, ground_sprite_height))


space = pymunk.Space()
space.gravity = 0, -9.81
space.damping = 0.9

ground = pymunk.Segment(
    space.static_body,
    (0, ground_y),
    (space_width, ground_y),
    radius=ground_radius,
)
ground.elasticity = elasticity
ground.friction = friction

ball_body = pymunk.Body()
ball_body.position = ball_position
ball_body.moment = 1
ball = pymunk.Circle(ball_body, radius=ball_radius)
ball.mass = 0.1
ball.elasticity = elasticity
ball.friction = friction


def attach_segment(anchor_body: pymunk.Body, anchor_point: pymunk.Vec2d, angle: float, angle_min: float, angle_max: float, length: float, radius: float, mass: float) -> typing.Tuple[pymunk.Body, pymunk.Shape, pymunk.constraints.PivotJoint, pymunk.constraints.SimpleMotor]:
    segment_body = pymunk.Body()
    segment_body.position = anchor_point.x, anchor_point.y
    segment_body.moment = 1
    segment = pymunk.Segment(
        segment_body,
        (0, 0),
        (math.cos(math.radians(angle)) * length,
         math.sin(math.radians(angle)) * length),
        radius=radius,
    )
    segment.mass = mass
    segment.elasticity = elasticity
    segment.friction = friction
    segment.filter = pymunk.ShapeFilter(group=1)

    pivot_joint = pymunk.constraints.PivotJoint(
        anchor_body,
        segment_body,
        anchor_body.world_to_local(anchor_point),
        (0, 0),
    )
    pivot_joint.collide_bodies = False

    limit_joint = pymunk.constraints.RotaryLimitJoint(
        anchor_body,
        segment_body,
        math.radians(angle_min),
        math.radians(angle_max),
    )
    limit_joint.collide_bodies = False

    motor = pymunk.constraints.SimpleMotor(
        anchor_body,
        segment_body,
        math.pi * 0.25,
    )
    motor.max_force = 2.3

    return segment_body, segment, pivot_joint, limit_joint, motor


thigh_body, thigh, hip_joint, hip_limit_joint, hip_motor = attach_segment(
    space.static_body,
    body_joint_position,
    thigh_angle,
    thigh_angle_min,
    thigh_angle_max,
    thigh_length,
    thigh_radius,
    thigh_mass,
)

tibia_body, tibia, knee_joint, knee_limit_joint, knee_motor = attach_segment(
    thigh_body,
    thigh_body.local_to_world(thigh.b),
    tibia_angle,
    tibia_angle_min,
    tibia_angle_max,
    tibia_length,
    tibia_radius,
    tibia_mass,
)

foot_body, foot, ankle_joint, ankle_limit_joint, ankle_motor = attach_segment(
    tibia_body,
    tibia_body.local_to_world(tibia.b),
    foot_angle,
    foot_angle_min,
    foot_angle_max,
    foot_length,
    foot_radius,
    foot_mass/3,
)

heel_vector = pymunk.Vec2d(foot_heel_length, 0).rotated_degrees(
    foot_heel_angle)
heel_segment = pymunk.Segment(
    foot_body,
    (0, 0),
    heel_vector,
    radius=foot_radius,
)
heel_segment.mass = foot_mass/3
heel_segment.elasticity = elasticity
heel_segment.friction = friction
heel_segment.filter = pymunk.ShapeFilter(group=1)

sole_segment = pymunk.Segment(
    foot_body,
    foot.b,
    heel_vector,
    radius=foot_radius,
)
sole_segment.mass = foot_mass/3
sole_segment.elasticity = elasticity
sole_segment.friction = friction
sole_segment.filter = pymunk.ShapeFilter(group=1)

space.add(
    ground,
    ball_body,
    ball,
    thigh_body,
    thigh,
    hip_joint,
    hip_limit_joint,
    hip_motor,
    tibia_body,
    tibia,
    knee_joint,
    knee_limit_joint,
    knee_motor,
    foot_body,
    foot,
    heel_segment,
    sole_segment,
    ankle_joint,
    ankle_limit_joint,
    ankle_motor,
)


def draw_transform(point: pymunk.Vec2d):
    return pymunk.Vec2d(
        int(point[0] * pixel_scale),
        (space_height * pixel_scale
         ) - int(point[1] * pixel_scale),
    )


def draw_circle(draw: ImageDraw, a: pymunk.Vec2d, b: pymunk.Vec2d, radius: float, color: str):
    draw.ellipse([
        draw_transform(a) - pymunk.Vec2d(radius, radius),
        draw_transform(b) + pymunk.Vec2d(radius, radius)
    ], fill=color)


def draw_line(draw: ImageDraw, body: pymunk.Body, segment: pymunk.Segment, color: str):
    a = body.local_to_world(segment.a)
    b = body.local_to_world(segment.b)
    radius = segment.radius
    draw.line((draw_transform(a), draw_transform(b)), fill=color,
              width=int(radius * 2 * pixel_scale))
    draw_circle(draw, a, a, radius * pixel_scale, color)
    draw_circle(draw, b, b, radius * pixel_scale, color)


# angles in radians
keyframes = generate_keyframes.generate_keyframes()


def normalize_angle(input_angle: float) -> float:
    output_angle = input_angle % (2 * math.pi)
    return output_angle - (2 * math.pi) if output_angle > math.pi else output_angle


def get_current_angles(thigh_body: pymunk.Body, thigh: pymunk.Segment, tibia_body: pymunk.Body, tibia: pymunk.Segment, foot_body: pymunk.Body, foot: pymunk.Segment):
    thigh_vector = thigh_body.local_to_world(
        thigh.b) - thigh_body.local_to_world(thigh.a)
    tibia_vector = tibia_body.local_to_world(
        tibia.b) - tibia_body.local_to_world(tibia.a)
    foot_vector = foot_body.local_to_world(
        foot.b) - foot_body.local_to_world(foot.a)
    return (
        normalize_angle(thigh_vector.angle - math.radians(thigh_angle)),
        normalize_angle(tibia_vector.angle - thigh_vector.angle),
        normalize_angle(
            (foot_vector.angle - tibia_vector.angle - (math.pi / 2)) % (2 * math.pi)),
    )


def clamp(v, low, high):
    return max(low, min(high, v))


def draw_sprite_with_two_points(frame: Image, joint_a: pymunk.Vec2d, joint_b: pymunk.Vec2d, sprite: Image, sprite_joint_a_pixel: pymunk.Vec2d, sprite_joint_b_pixel: pymunk.Vec2d):
    joint_a_pixel = draw_transform(joint_a)
    joint_b_pixel = draw_transform(joint_b)
    # rotate
    angle_degrees = (sprite_joint_b_pixel - sprite_joint_a_pixel).angle_degrees - \
        (joint_b_pixel - joint_a_pixel).angle_degrees
    rotated_sprite = sprite.rotate(angle_degrees, expand=True)
    sprite_center = pymunk.Vec2d(sprite.size[0], sprite.size[1]) / 2
    rotated_sprite_center = pymunk.Vec2d(
        rotated_sprite.size[0], rotated_sprite.size[1]) / 2
    sprite_center_to_sprite_joint_a_pixel = sprite_joint_a_pixel - sprite_center
    rotated_sprite_center_to_rotated_sprite_joint_a_pixel = sprite_center_to_sprite_joint_a_pixel.rotated_degrees(
        -angle_degrees)  # invert angle because of flipped y-axis
    rotated_sprite_joint_a_pixel = rotated_sprite_center + \
        rotated_sprite_center_to_rotated_sprite_joint_a_pixel
    # scale
    scale = (joint_b_pixel - joint_a_pixel).length / \
        (sprite_joint_b_pixel - sprite_joint_a_pixel).length
    scaled_sprite = rotated_sprite.resize(
        (pymunk.Vec2d(rotated_sprite.size[0], rotated_sprite.size[1]) * scale).int_tuple)
    scaled_sprite_joint_a_pixel = rotated_sprite_joint_a_pixel * scale
    # translate via paste
    frame.paste(scaled_sprite, (joint_a_pixel -
                                scaled_sprite_joint_a_pixel).int_tuple, mask=scaled_sprite)


def draw_sprite_with_center_comma_radius_oxford_comma_and_rotation(frame: Image, center_point: pymunk.Vec2d, radius: float, angle_degrees: float, sprite: Image):
    center_pixel = draw_transform(center_point)
    radius_pixel = radius * pixel_scale
    resized_sprite = sprite.resize(
        (int(radius_pixel * 2), int(radius_pixel * 2)))
    rotated_sprite = resized_sprite.rotate(angle_degrees)
    frame.paste(rotated_sprite, (center_pixel - (radius_pixel,
                                                 radius_pixel)).int_tuple, mask=rotated_sprite)

def get_current_ball_position():
    ball_x = ball.bb.left + ((ball.bb.right - ball.bb.left) / 2)
    ball_y = ball.bb.bottom + ((ball.bb.top - ball.bb.bottom) / 2)
    return pymunk.Vec2d(ball_x, ball_y)


def current_frame(score: float, ghost_ball_position: pymunk.Vec2d, ghost_ball_rotation: float):
    frame = Image.new('RGB', (int(space_width * pixel_scale),
                              int(space_height * pixel_scale)), '#eee')
    frame.paste(ground_sprite, (0, int(
        (space_height * pixel_scale) - ground_sprite_height)), mask=ground_sprite)
    draw = ImageDraw.Draw(frame, mode='RGBA')
    draw.ellipse([
        draw_transform(pymunk.Vec2d(body_joint_position.x,
                                    ground_y + ground_radius) + body_shadow_radius),
        draw_transform(pymunk.Vec2d(body_joint_position.x,
                                    ground_y + ground_radius) - body_shadow_radius),
    ], fill=(0, 0, 0, 127))
    ball_x, ball_y = get_current_ball_position()
    if ball_y >= 0:
        ball_distance_from_ground = ball_y - ball_radius - ground_y - ground_radius
        ball_shadow_scale = max(0, 1 - ball_distance_from_ground)
        draw.ellipse([
            draw_transform(pymunk.Vec2d(ball_x, ground_y + ground_radius) +
                           (ball_shadow_radius * ball_shadow_scale)),
            draw_transform(pymunk.Vec2d(ball_x, ground_y + ground_radius) -
                           (ball_shadow_radius * ball_shadow_scale)),
        ], fill=(0, 0, 0, 127))
    draw_sprite_with_center_comma_radius_oxford_comma_and_rotation(frame, target_position, target_radius, 0, target_sprite)
    draw.multiline_text(
        (10, 10), f'Time: {len(frames) / 10:.1f} s\nSmallest Distance: {int(score * 100)} cm', font=font, fill='#000')
    draw_sprite_with_two_points(
        frame,
        body_joint_position - pymunk.Vec2d(0, leg_length),
        body_joint_position,
        leg_sprite,
        leg_bottom_pixel,
        leg_joint_pixel,
    )
    draw_sprite_with_two_points(
        frame,
        thigh_body.local_to_world(thigh.a),
        thigh_body.local_to_world(thigh.b),
        thigh_sprite,
        thigh_joint_a_pixel,
        thigh_joint_b_pixel,
    )
    draw_sprite_with_two_points(
        frame,
        foot_body.local_to_world(foot.a),
        foot_body.local_to_world(foot.b),
        foot_sprite,
        foot_joint_a_pixel,
        foot_joint_b_pixel,
    )
    draw_sprite_with_two_points(
        frame,
        tibia_body.local_to_world(tibia.a),
        tibia_body.local_to_world(tibia.b),
        tibia_sprite,
        tibia_joint_a_pixel,
        tibia_joint_b_pixel,
    )
    draw_sprite_with_two_points(
        frame,
        body_joint_position,
        body_joint_position + pymunk.Vec2d(0, body_length),
        body_sprite,
        body_joint_pixel,
        body_top_pixel,
    )
    center = get_current_ball_position()
    radius = ball_radius
    angle_degrees = math.degrees(ball_body.angle)
    draw_sprite_with_center_comma_radius_oxford_comma_and_rotation(frame, ghost_ball_position, radius, ghost_ball_rotation, ghost_ball_sprite)
    draw_sprite_with_center_comma_radius_oxford_comma_and_rotation(frame, ghost_ball_position, radius, 0, ghost_ball_shadow_sprite)
    draw_sprite_with_center_comma_radius_oxford_comma_and_rotation(frame, center, radius, angle_degrees, ball_sprite)
    draw_sprite_with_center_comma_radius_oxford_comma_and_rotation(frame, center, radius, 0, ball_shadow_sprite)
    return frame


frames = []
score = float('inf')
ghost_ball_position = get_current_ball_position()
ghost_ball_rotation = math.degrees(ball_body.angle)
for keyframe in keyframes:
    hip_angle, knee_angle, ankle_angle = get_current_angles(
        thigh_body, thigh, tibia_body, tibia, foot_body, foot)
    hip_angle_difference = keyframe['hip_angle'] - hip_angle
    knee_angle_difference = keyframe['knee_angle'] - knee_angle
    ankle_angle_difference = keyframe['ankle_angle'] - ankle_angle
    hip_angle_velocity = clamp(
        hip_angle_difference / keyframe['duration'], -maximum_velocity, maximum_velocity)
    knee_angle_velocity = clamp(
        knee_angle_difference / keyframe['duration'], -maximum_velocity, maximum_velocity)
    ankle_angle_velocity = clamp(
        ankle_angle_difference / keyframe['duration'], -maximum_velocity, maximum_velocity)
    hip_motor.rate = -hip_angle_velocity
    knee_motor.rate = -knee_angle_velocity
    ankle_motor.rate = -ankle_angle_velocity
    for _ in range(int(keyframe['duration'] * 10)):
        for _ in range(100):
            space.step(0.01 * 0.1)
            current_score = abs(target_position - ball_body.position)
            if current_score < score:
                ghost_ball_position = get_current_ball_position()
                ghost_ball_rotation = math.degrees(ball_body.angle)
                score = current_score
        frame = current_frame(score, ghost_ball_position, ghost_ball_rotation)
        frames.append(frame)
if len(frames) < minimal_frame_amount:
    hip_motor.rate = 0
    knee_motor.rate = 0
    ankle_motor.rate = 0
    for _ in range(minimal_frame_amount - len(frames)):
        for _ in range(100):
            space.step(0.01 * 0.1)
            current_score = abs(target_position - ball_body.position)
            if current_score < score:
                ghost_ball_position = get_current_ball_position()
                ghost_ball_rotation = math.degrees(ball_body.angle)
                score = current_score
        frame = current_frame(score, ghost_ball_position, ghost_ball_rotation)
        frames.append(frame)

print(f'Smallest Distance: {int(score * 100)} cm')

frames[0].save('animation.webp', save_all=True,
               append_images=frames[1:], duration=100, loop=0)
