import math
import typing
import pymunk
import pymunk.constraints
from PIL import Image, ImageDraw

configuration = {
    'pixel_scale': 200,
    'space_width': 3,
    'space_height': 1,
    'hip_x': 0.5,
    'hip_y': 0.4,
    'thigh_length': 0.2,
    'thigh_radius': 0.05,
    'thigh_angle': 315,
    'tibia_length': 0.2,
    'tibia_radius': 0.05,
    'tibia_angle': 225,
    'foot_length': 0.15,
    'foot_radius': 0.025,
    'foot_angle': 0,
    'ground_y': 0.05,
    'ground_radius': 0.05,
    'ball_radius': 0.1,
    'ball_x': 0.7,
    'ball_y': 0.2,
}

space = pymunk.Space()
space.gravity = 0, -9.81

ground = pymunk.Segment(
    space.static_body,
    (0, configuration['ground_y']),
    (configuration['space_width'], configuration['ground_y']),
    radius=configuration['ground_radius'],
)
ground.elasticity = 0.1  # enable ball bounce

ball_body = pymunk.Body()
ball_body.position = configuration['ball_x'], configuration['ball_y']
ball_body.moment = 1
ball = pymunk.Circle(ball_body, radius=configuration['ball_radius'])
ball.mass = 1
ball.elasticity = 0


def attach_segment(anchor_body: pymunk.Body, anchor_point: pymunk.Vec2d, angle: float, length: float, radius: float) -> typing.Tuple[pymunk.Body, pymunk.Shape, pymunk.constraints.PivotJoint, pymunk.constraints.SimpleMotor]:
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
    segment.elasticity = 0.5
    segment.filter = pymunk.ShapeFilter(group=1)

    joint = pymunk.constraints.PivotJoint(
        anchor_body,
        segment_body,
        anchor_body.world_to_local(anchor_point),
        (0, 0),
    )
    joint.collide_bodies = False

    motor = pymunk.constraints.SimpleMotor(
        anchor_body,
        segment_body,
        math.pi * 0.25,
    )

    return segment_body, segment, joint, motor


thigh_body, thigh, hip_joint, hip_motor = attach_segment(
    space.static_body,
    pymunk.Vec2d(configuration['hip_x'], configuration['hip_y']),
    configuration['thigh_angle'],
    configuration['thigh_length'],
    configuration['thigh_radius'],
)

tibia_body, tibia, knee_joint, knee_motor = attach_segment(
    thigh_body,
    thigh_body.local_to_world(thigh.b),
    configuration['tibia_angle'],
    configuration['tibia_length'],
    configuration['tibia_radius'],
)

foot_body, foot, ankle_joint, ankle_motor = attach_segment(
    tibia_body,
    tibia_body.local_to_world(tibia.b),
    configuration['foot_angle'],
    configuration['foot_length'],
    configuration['foot_radius'],
)

space.add(
    ground,
    # ball_body,
    # ball,
    thigh_body,
    thigh,
    hip_joint,
    hip_motor,
    tibia_body,
    tibia,
    knee_joint,
    knee_motor,
    foot_body,
    foot,
    ankle_joint,
    ankle_motor,
)

print_options = pymunk.SpaceDebugDrawOptions()


def draw_line(draw, body: pymunk.Body, segment: pymunk.Segment, color: str):
    draw.line([
        int(body.local_to_world(segment.a).x *
            configuration['pixel_scale']),
        (configuration['space_height'] * configuration['pixel_scale']) -
        int(body.local_to_world(segment.a).y *
            configuration['pixel_scale']),
        int(body.local_to_world(segment.b).x *
            configuration['pixel_scale']),
        (configuration['space_height'] * configuration['pixel_scale']) -
        int(body.local_to_world(segment.b).y *
            configuration['pixel_scale']),
    ], fill=color, width=int(2 * segment.radius * configuration['pixel_scale']))


# angles in radians
keyframes = [
    {'hip_angle': 0, 'knee_angle': 0, 'ankle_angle': 0, 'duration': 5},
    {'hip_angle': math.pi / 2, 'knee_angle': math.pi / 2, 'ankle_angle': math.pi / 2, 'duration': 5},
    {'hip_angle': 0, 'knee_angle': 0, 'ankle_angle': 0, 'duration': 5},
    {'hip_angle': -math.pi / 2, 'knee_angle': -math.pi / 2, 'ankle_angle': -math.pi / 2, 'duration': 5},
    {'hip_angle': 0, 'knee_angle': 0, 'ankle_angle': 0, 'duration': 5},
]


def normalize_angle(input_angle: float) -> float:
    output_angle = input_angle % (2 * math.pi)
    return output_angle - (2 * math.pi) if output_angle > math.pi else output_angle


def get_current_angles(thigh_body: pymunk.Body, thigh: pymunk.Segment, tibia_body: pymunk.Body, tibia: pymunk.Segment, foot_body: pymunk.Body, foot: pymunk.Segment):
    thigh_vector = thigh_body.local_to_world(thigh.b) - thigh_body.local_to_world(thigh.a)
    tibia_vector = tibia_body.local_to_world(tibia.b) - tibia_body.local_to_world(tibia.a)
    foot_vector = foot_body.local_to_world(foot.b) - foot_body.local_to_world(foot.a)
    return (
        normalize_angle(thigh_vector.angle),
        normalize_angle(tibia_vector.angle - thigh_vector.angle),
        normalize_angle((foot_vector.angle - tibia_vector.angle - (math.pi / 2)) % (2 * math.pi)),
    )


frames = []
for keyframe in keyframes:
    hip_angle, knee_angle, ankle_angle = get_current_angles(thigh_body, thigh, tibia_body, tibia, foot_body, foot)
    hip_angle_difference = keyframe['hip_angle'] - hip_angle
    knee_angle_difference = keyframe['knee_angle'] - knee_angle
    ankle_angle_difference = keyframe['ankle_angle'] - ankle_angle
    hip_angle_velocity = hip_angle_difference / keyframe['duration']
    knee_angle_velocity = knee_angle_difference / keyframe['duration']
    ankle_angle_velocity = ankle_angle_difference / keyframe['duration']
    # TODO: clamp velocity @PasGl
    # TODO: limit angles @PasGl
    hip_motor.rate = -hip_angle_velocity
    knee_motor.rate = -knee_angle_velocity
    ankle_motor.rate = -ankle_angle_velocity
    for _ in range(keyframe['duration'] * 10):
        for _ in range(100):
            space.step(0.01 * 0.1)
        # space.debug_draw(print_options)
        frame = Image.new('RGB', (configuration['space_width'] * configuration['pixel_scale'],
                                configuration['space_height'] * configuration['pixel_scale']), '#fff')
        draw = ImageDraw.Draw(frame)
        draw.text((70, 10), f'{len(frames)}', fill='#000')
        draw_line(draw, space.static_body, ground, '#000')
        draw_line(draw, thigh_body, thigh, '#f00')
        draw_line(draw, tibia_body, tibia, '#f0f')
        draw_line(draw, foot_body, foot, '#00f')
        frames.append(frame)

frames[0].save('joint.webp', save_all=True,
               append_images=frames[1:], duration=100, loop=0)
