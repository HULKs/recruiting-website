import math
import typing
import pymunk
import pymunk.constraints
from PIL import Image, ImageDraw, ImageFont

pixel_scale = 200
space_width = 3
space_height = 1.6875  # 16:9 aspect ratio
body_sprite_path = 'body.png'
body_joint_position = pymunk.Vec2d(0.5, 0.55)
body_joint_pixel = pymunk.Vec2d(212, 876)
body_top_pixel = pymunk.Vec2d(212, 24)
body_length = 0.5
body_shadow_radius = pymunk.Vec2d(-0.35, 0.025)
thigh_sprite_path = 'thigh.png'
thigh_joint_a_pixel = pymunk.Vec2d(191, 69)
thigh_joint_b_pixel = pymunk.Vec2d(183, 509)
thigh_angle = 315
thigh_angle_min = -90
thigh_angle_max = 45
thigh_length = 0.2
thigh_radius = 0.05
tibia_sprite_path = 'tibia.png'
tibia_joint_a_pixel = pymunk.Vec2d(184, -44)
tibia_joint_b_pixel = pymunk.Vec2d(183, 382)
tibia_angle = 225
tibia_angle_min = -45
tibia_angle_max = 90
tibia_length = 0.2
tibia_radius = 0.05
foot_sprite_path = 'foot.png'
foot_joint_a_pixel = pymunk.Vec2d(513, 125)
foot_joint_b_pixel = pymunk.Vec2d(1224, 416)
foot_angle = -21
foot_angle_min = -135
foot_angle_max = 0
foot_length = 0.15
foot_radius = 0.025
foot_heel_angle = 219
foot_heel_length = 0.1
ground_sprite_path = 'ground.png'
ground_y = 0.05
ground_radius = 0.05
ball_sprite_path = 'ball.png'
ball_radius = 0.1
ball_position = pymunk.Vec2d(1.0, 1.0)
ball_shadow_radius = pymunk.Vec2d(-0.1, 0.0175)
maximum_velocity = math.pi
target_position = pymunk.Vec2d(2.5, 0.75)
elasticity = 0.97
friction = 0.5
minimal_frame_amount = 50

font = ImageFont.truetype('JetBrainsMono-Regular.ttf', 14)
body_sprite = Image.open(body_sprite_path)
thigh_sprite = Image.open(thigh_sprite_path)
tibia_sprite = Image.open(tibia_sprite_path)
foot_sprite = Image.open(foot_sprite_path)
ball_sprite = Image.open(ball_sprite_path)

ground_sprite = Image.open(ground_sprite_path)
ground_sprite_height = int(space_width * pixel_scale / ground_sprite.size[0] * ground_sprite.size[1])
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
ball.mass = 1
ball.elasticity = elasticity
ball.friction = friction


def attach_segment(anchor_body: pymunk.Body, anchor_point: pymunk.Vec2d, angle: float, angle_min: float, angle_max: float, length: float, radius: float) -> typing.Tuple[pymunk.Body, pymunk.Shape, pymunk.constraints.PivotJoint, pymunk.constraints.SimpleMotor]:
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
    segment.mass = 1
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
    motor.max_force = 10

    return segment_body, segment, pivot_joint, limit_joint, motor


thigh_body, thigh, hip_joint, hip_limit_joint, hip_motor = attach_segment(
    space.static_body,
    body_joint_position,
    thigh_angle,
    thigh_angle_min,
    thigh_angle_max,
    thigh_length,
    thigh_radius,
)

tibia_body, tibia, knee_joint, knee_limit_joint, knee_motor = attach_segment(
    thigh_body,
    thigh_body.local_to_world(thigh.b),
    tibia_angle,
    tibia_angle_min,
    tibia_angle_max,
    tibia_length,
    tibia_radius,
)

foot_body, foot, ankle_joint, ankle_limit_joint, ankle_motor = attach_segment(
    tibia_body,
    tibia_body.local_to_world(tibia.b),
    foot_angle,
    foot_angle_min,
    foot_angle_max,
    foot_length,
    foot_radius,
)

heel_vector = pymunk.Vec2d(foot_heel_length, 0).rotated_degrees(
    foot_heel_angle)
heel_segment = pymunk.Segment(
    foot_body,
    (0, 0),
    heel_vector,
    radius=foot_radius,
)
heel_segment.mass = 1
heel_segment.elasticity = elasticity
heel_segment.friction = friction
heel_segment.filter = pymunk.ShapeFilter(group=1)

sole_segment = pymunk.Segment(
    foot_body,
    foot.b,
    heel_vector,
    radius=foot_radius,
)
sole_segment.mass = 1
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
keyframes = [
    {'hip_angle': 0, 'knee_angle': 0, 'ankle_angle': 0, 'duration': 0.1},
    {'hip_angle': math.pi / 2, 'knee_angle': math.pi /
        2, 'ankle_angle': math.pi / 2, 'duration': 0.1},
    {'hip_angle': 0, 'knee_angle': 0, 'ankle_angle': 0, 'duration': 1},
    {'hip_angle': -math.pi / 2, 'knee_angle': -math.pi /
        2, 'ankle_angle': -math.pi / 2, 'duration': 1},
    {'hip_angle': 0, 'knee_angle': 0, 'ankle_angle': 0, 'duration': 1},
]


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
        normalize_angle(thigh_vector.angle),
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


def draw_sprite_with_bounding_box(frame: Image, circle_body: pymunk.Body, circle: pymunk.Circle, sprite: Image):
    upper_left = pymunk.Vec2d(circle.bb.left, circle.bb.top)
    bounding_box_size = pymunk.Vec2d(
        circle.bb.right - circle.bb.left, circle.bb.bottom - circle.bb.top)
    center = upper_left + (bounding_box_size / 2)
    radius = circle.bb.right - center.x
    angle_degrees = math.degrees(circle_body.angle)
    center_pixel = draw_transform(center)
    radius_pixel = radius * pixel_scale
    resized_sprite = sprite.resize(
        (int(radius_pixel * 2), int(radius_pixel * 2)))
    rotated_sprite = resized_sprite.rotate(angle_degrees)
    frame.paste(rotated_sprite, (center_pixel - (radius_pixel,
                                                 radius_pixel)).int_tuple, mask=rotated_sprite)


def append_frame(score: float):
    frame = Image.new('RGB', (int(space_width * pixel_scale),
                              int(space_height * pixel_scale)), '#eee')
    frame.paste(ground_sprite, (0, int((space_height * pixel_scale) - ground_sprite_height)), mask=ground_sprite)
    draw = ImageDraw.Draw(frame)
    draw.ellipse([
        draw_transform(pymunk.Vec2d(body_joint_position.x, ground_y + ground_radius) + body_shadow_radius),
        draw_transform(pymunk.Vec2d(body_joint_position.x, ground_y + ground_radius) - body_shadow_radius),
    ], fill='#000')
    ball_x = ball.bb.left + ((ball.bb.right - ball.bb.left) / 2)
    ball_y = ball.bb.bottom + ((ball.bb.top - ball.bb.bottom) / 2)
    ball_distance_from_ground = ball_y - ball_radius - ground_y - ground_radius
    ball_shadow_scale = max(0, 1 - ball_distance_from_ground)
    draw.ellipse([
        draw_transform(pymunk.Vec2d(ball_x, ground_y + ground_radius) + (ball_shadow_radius * ball_shadow_scale)),
        draw_transform(pymunk.Vec2d(ball_x, ground_y + ground_radius) - (ball_shadow_radius * ball_shadow_scale)),
    ], fill='#000')
    draw_circle(draw, target_position, target_position,
                ball_radius * pixel_scale, '#AAA')
    draw.multiline_text((10, 10), f'Time: {len(frames) / 10:.1f} s\nSmallest Distance: {"N/A" if math.isinf(score) else int(score * 100)} cm', font=font, fill='#000')
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
        tibia_body.local_to_world(tibia.a),
        tibia_body.local_to_world(tibia.b),
        tibia_sprite,
        tibia_joint_a_pixel,
        tibia_joint_b_pixel,
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
        body_joint_position,
        body_joint_position + pymunk.Vec2d(0, body_length),
        body_sprite,
        body_joint_pixel,
        body_top_pixel,
    )
    draw_sprite_with_bounding_box(frame, ball_body, ball, ball_sprite)
    return frame, abs(target_position - ball_body.position)


frames = []
score = float('inf')
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
        frame, current_score = append_frame(score)
        score = min(score, current_score)
        frames.append(frame)
if len(frames) < minimal_frame_amount:
    hip_motor.rate = 0
    knee_motor.rate = 0
    ankle_motor.rate = 0
    for _ in range(minimal_frame_amount - len(frames)):
        for _ in range(100):
            space.step(0.01 * 0.1)
        frame, current_score = append_frame(score)
        score = min(score, current_score)
        frames.append(frame)

print('Best Score:', score)

frames[0].save('animation.webp', save_all=True,
               append_images=frames[1:], duration=100, loop=0)
