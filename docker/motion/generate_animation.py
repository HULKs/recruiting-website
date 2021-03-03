import math
import typing
import pymunk
import pymunk.constraints
from PIL import Image, ImageDraw

configuration = {
    'pixel_scale': 200,
    'space_width': 3,
    'space_height': 1,
    'body_sprite_path': 'body.png',
    'body_joint_position': pymunk.Vec2d(0.5, 0.45),
    'body_joint_pixel': pymunk.Vec2d(212, 876),
    'body_top_pixel': pymunk.Vec2d(212, 24),
    'body_length': 0.5,
    'thigh_sprite_path': 'thigh.png',
    'thigh_joint_a_pixel': pymunk.Vec2d(191, 69),
    'thigh_joint_b_pixel': pymunk.Vec2d(183, 509),
    'thigh_angle': 315,
    'thigh_angle_min': -90,
    'thigh_angle_max': 45,
    'thigh_length': 0.2,
    'thigh_radius': 0.05,
    'tibia_sprite_path': 'tibia.png',
    'tibia_joint_a_pixel': pymunk.Vec2d(184, -44),
    'tibia_joint_b_pixel': pymunk.Vec2d(183, 382),
    'tibia_angle': 225,
    'tibia_angle_min': -45,
    'tibia_angle_max': 90,
    'tibia_length': 0.2,
    'tibia_radius': 0.05,
    'foot_sprite_path': 'foot.png',
    'foot_joint_a_pixel': pymunk.Vec2d(513, 125),
    'foot_joint_b_pixel': pymunk.Vec2d(1224, 416),
    'foot_angle': -21,
    'foot_angle_min': -135,
    'foot_angle_max': 0,
    'foot_length': 0.15,
    'foot_radius': 0.025,
    'foot_heel_angle': 219,
    'foot_heel_length': 0.1,
    'ground_y': 0.05,
    'ground_radius': 0.05,
    'ball_sprite_path': 'ball.png',
    'ball_radius': 0.1,
    'ball_position': pymunk.Vec2d(0.9, 0.4),
    'maximum_velocity': math.pi,
    'target_position': pymunk.Vec2d(2.5, 0.25),
    'elasticity': 0.95,
    'friction': 0.5,
}

body_sprite = Image.open(configuration['body_sprite_path'])
thigh_sprite = Image.open(configuration['thigh_sprite_path'])
tibia_sprite = Image.open(configuration['tibia_sprite_path'])
foot_sprite = Image.open(configuration['foot_sprite_path'])
ball_sprite = Image.open(configuration['ball_sprite_path'])

space = pymunk.Space()
space.gravity = 0, -9.81
space.damping = 0.9

ground = pymunk.Segment(
    space.static_body,
    (0, configuration['ground_y']),
    (configuration['space_width'], configuration['ground_y']),
    radius=configuration['ground_radius'],
)
ground.elasticity = configuration['elasticity']
ground.friction = configuration['friction']

ball_body = pymunk.Body()
ball_body.position = configuration['ball_position']
ball_body.moment = 1
ball = pymunk.Circle(ball_body, radius=configuration['ball_radius'])
ball.mass = 1
ball.elasticity = configuration['elasticity']
ball.friction = configuration['friction']


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
    segment.elasticity = configuration['elasticity']
    segment.friction = configuration['friction']
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
    configuration['body_joint_position'],
    configuration['thigh_angle'],
    configuration['thigh_angle_min'],
    configuration['thigh_angle_max'],
    configuration['thigh_length'],
    configuration['thigh_radius'],
)

tibia_body, tibia, knee_joint, knee_limit_joint, knee_motor = attach_segment(
    thigh_body,
    thigh_body.local_to_world(thigh.b),
    configuration['tibia_angle'],
    configuration['tibia_angle_min'],
    configuration['tibia_angle_max'],
    configuration['tibia_length'],
    configuration['tibia_radius'],
)

foot_body, foot, ankle_joint, ankle_limit_joint, ankle_motor = attach_segment(
    tibia_body,
    tibia_body.local_to_world(tibia.b),
    configuration['foot_angle'],
    configuration['foot_angle_min'],
    configuration['foot_angle_max'],
    configuration['foot_length'],
    configuration['foot_radius'],
)

heel_vector = pymunk.Vec2d(configuration['foot_heel_length'], 0).rotated_degrees(
    configuration['foot_heel_angle'])
heel_segment = pymunk.Segment(
    foot_body,
    (0, 0),
    heel_vector,
    radius=configuration['foot_radius'],
)
heel_segment.mass = 1
heel_segment.elasticity = configuration['elasticity']
heel_segment.friction = configuration['friction']
heel_segment.filter = pymunk.ShapeFilter(group=1)

sole_segment = pymunk.Segment(
    foot_body,
    foot.b,
    heel_vector,
    radius=configuration['foot_radius'],
)
sole_segment.mass = 1
sole_segment.elasticity = configuration['elasticity']
sole_segment.friction = configuration['friction']
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

print_options = pymunk.SpaceDebugDrawOptions()


def draw_transform(point):
    return pymunk.Vec2d(
        int(point[0] * configuration['pixel_scale']),
        (configuration['space_height'] * configuration['pixel_scale']
         ) - int(point[1] * configuration['pixel_scale']),
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
              width=int(radius * 2 * configuration['pixel_scale']))
    draw_circle(draw, a, a, radius * configuration['pixel_scale'], color)
    draw_circle(draw, b, b, radius * configuration['pixel_scale'], color)


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
    radius_pixel = radius * configuration['pixel_scale']
    resized_sprite = sprite.resize(
        (int(radius_pixel * 2), int(radius_pixel * 2)))
    rotated_sprite = resized_sprite.rotate(angle_degrees)
    frame.paste(rotated_sprite, (center_pixel - (radius_pixel,
                                                 radius_pixel)).int_tuple, mask=rotated_sprite)


frames = []
score = float('inf')
for keyframe in keyframes:
    hip_angle, knee_angle, ankle_angle = get_current_angles(
        thigh_body, thigh, tibia_body, tibia, foot_body, foot)
    hip_angle_difference = keyframe['hip_angle'] - hip_angle
    knee_angle_difference = keyframe['knee_angle'] - knee_angle
    ankle_angle_difference = keyframe['ankle_angle'] - ankle_angle
    hip_angle_velocity = clamp(
        hip_angle_difference / keyframe['duration'], -configuration['maximum_velocity'], configuration['maximum_velocity'])
    knee_angle_velocity = clamp(
        knee_angle_difference / keyframe['duration'], -configuration['maximum_velocity'], configuration['maximum_velocity'])
    ankle_angle_velocity = clamp(
        ankle_angle_difference / keyframe['duration'], -configuration['maximum_velocity'], configuration['maximum_velocity'])
    hip_motor.rate = -hip_angle_velocity
    knee_motor.rate = -knee_angle_velocity
    ankle_motor.rate = -ankle_angle_velocity
    for _ in range(int(keyframe['duration'] * 10)):
        for _ in range(100):
            space.step(0.01 * 0.1)
        score = min(score, abs(
            configuration['target_position'] - ball_body.position))
        frame = Image.new('RGB', (configuration['space_width'] * configuration['pixel_scale'],
                                  configuration['space_height'] * configuration['pixel_scale']), '#fff')
        draw = ImageDraw.Draw(frame)
        draw_circle(draw, configuration['target_position'], configuration['target_position'],
                    configuration['ball_radius'] * configuration['pixel_scale'], '#AAA')
        draw.text((70, 10), f'{len(frames)}', fill='#000')
        draw.text((450, 10), f'Score: {score:.5f}', fill='#000')
        draw_line(draw, space.static_body, ground, '#000')
        draw_sprite_with_two_points(
            frame,
            thigh_body.local_to_world(thigh.a),
            thigh_body.local_to_world(thigh.b),
            thigh_sprite,
            configuration['thigh_joint_a_pixel'],
            configuration['thigh_joint_b_pixel'],
        )
        draw_sprite_with_two_points(
            frame,
            tibia_body.local_to_world(tibia.a),
            tibia_body.local_to_world(tibia.b),
            tibia_sprite,
            configuration['tibia_joint_a_pixel'],
            configuration['tibia_joint_b_pixel'],
        )
        draw_sprite_with_two_points(
            frame,
            foot_body.local_to_world(foot.a),
            foot_body.local_to_world(foot.b),
            foot_sprite,
            configuration['foot_joint_a_pixel'],
            configuration['foot_joint_b_pixel'],
        )
        draw_sprite_with_two_points(
            frame,
            thigh_body.local_to_world(thigh.a),
            thigh_body.local_to_world(
                thigh.a) + pymunk.Vec2d(0, configuration['body_length']),
            body_sprite,
            configuration['body_joint_pixel'],
            configuration['body_top_pixel'],
        )
        draw_sprite_with_bounding_box(frame, ball_body, ball, ball_sprite)
        frames.append(frame)

frames[0].save('animation.gif', save_all=True,
               append_images=frames[1:], duration=100, loop=0)
