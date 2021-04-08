import collections
import math
import typing

JointAngles = collections.namedtuple(
    'JointAngles',
    ['theta_1', 'theta_2', 'theta_3'],
)


def are_joint_angles_feasible(i: int, joint_angles: JointAngles):
    if joint_angles.theta_1 < math.radians(-90) or joint_angles.theta_1 > math.radians(45):
        print(
            f'    theta_1 ({math.degrees(joint_angles.theta_1):.1f}°) of joint angle #{i + 1} is out of limit [-90°, 45°]')
        return False
    if joint_angles.theta_2 < math.radians(-45) or joint_angles.theta_2 > math.radians(90):
        print(
            f'    theta_2 ({math.degrees(joint_angles.theta_2):.1f}°) of joint angle #{i + 1} is out of limit [-45°, 90°]')
        return False
    if joint_angles.theta_3 < math.radians(-135) or joint_angles.theta_3 > math.radians(0):
        print(
            f'    theta_3 ({math.degrees(joint_angles.theta_3):.1f}°) of joint angle #{i + 1} is out of limit [-135°, 0°]')
        return False
    return True


def filter_feasible_joint_angles(set_of_joint_angles: typing.List[JointAngles]) -> typing.List[JointAngles]:
    return [
        joint_angles
        for i, joint_angles in enumerate(set_of_joint_angles)
        if are_joint_angles_feasible(i, joint_angles)
    ]
