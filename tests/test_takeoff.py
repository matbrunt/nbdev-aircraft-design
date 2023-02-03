import pytest
from math import asin, cos, tan
from numpy import rad2deg, deg2rad
from typing import TypedDict

def transition_speed(V_s1: float) -> float:
    """
    V_s1: stall speed, ft/s
    """
    return 1.15 * V_s1

def test_transition_speed():
    # 108 ft/s => 64 KCAS
    output = transition_speed(108)
    assert round(output, 1) == 124.2

def lift_coefficient(w: int, v: float, s: float) -> float:
    """
    Lift coefficient ($C_L$) at velocity v
    w = weight lb_f
    v = speed ft/s
    s = wing surface area ft^2
    $$
    C_L = \frac{2W}{\rho V^2 S}
    $$
    """
    return (2 * w) / (0.002378 * (v ** 2) * s)

def test_lift_coefficient():
    w = 3400 # lb_f
    v = 124.2 # ft/s
    s = 144.9 # ft^2
    output = lift_coefficient(w, v, s)
    assert round(output, 3) == 1.279

def drag_coefficient_simplified(c_dmin: float, k: float, c_l: float) -> float:
    """
    Drag coefficient at velocity v using simplified drag model
    $$
    C_D = C_Dmin + k C^2_L
    $$
    """
    return c_dmin + k * (c_l ** 2)

def test_drag_coefficient():
    output = drag_coefficient_simplified(0.0350, 0.04207, 1.279)
    assert round(output, 4) == 0.1038

def climb_angle(t: int, w: int, l: float, d: float) -> float:
    """
    Climb angle (degrees) at velocity v
    T = thrust lb_f
    W = weight lb_f
    L = lift coefficient
    D = drag coefficient

    $$
    \theta_{climb} = \sin^{-1} \left( \frac{T}{W} - \frac{1}{L/D} \right)
    $$
    """
    thrust_weight_ratio = t / w
    lift_drag_ratio = l / d
    return rad2deg(asin(thrust_weight_ratio - (1 / lift_drag_ratio)))

def test_climb_angle():
    output = climb_angle(908, 3400, 1.279, 0.1038)
    assert round(output, 1) == 10.7

def transition_radius(v: float) -> float:
    """
    Transition radius, R ft
    v = stall speed, ft/s

    $$
    R \approx 0.2156 V^2_{S1}
    $$
    """
    return 0.2156 * (v ** 2)

def test_transition_radius():
    output = transition_radius(108.0)
    assert round(output, 0) == 2515

def transition_distance(v: float, t: int, w: int, l: float, d: float) -> float:
    """
    Transition distance ft
    v: stall speed, ft/s
    t: thrust, lb_f
    w: weight, lb_f
    l: lift coefficient
    d: drag coefficient

    $$
    S_{TR} \approx 0.2156 \times V^2{S1} \times \left( \frac{T}{W} - \frac{1}{L/D} \right)
    $$
    """
    thrust_weight_ratio = t / w
    lift_drag_ratio = l / d
    
    return 0.2156 * (v ** 2) * (thrust_weight_ratio - (1/lift_drag_ratio))

def test_transition_distance():
    output = transition_distance(108.0, 908, 3400, 1.279, 0.1038)
    assert round(output, 0) == 467

def transition_height(r: float, a: float) -> float:
    """
    Transition height, ft
    r: transition radius, ft
    a: climb angle: degrees
    
    $$
    h_{TR} = R \left( 1 - \cos \theta_{climb} \right)
    $$
    """
    return r * (1 - cos(deg2rad(a)))

def test_transition_height():
    output = transition_height(2515.0, 10.7)
    assert round(output, 1) == 43.7

def climb_distance(h_obst: float, h_tr: float, a: float) -> float:
    """
    Distance covered in the climb segment, ft
    h_obst: Height of obstacle, ft
    h_tr: transition height, ft
    a: climb angle: degrees

    $$
    S_C = \frac{h{obst} - h{TR}}{\tan \theta_{climb}}
    $$
    """
    return (h_obst - h_tr) / tan(deg2rad(a))

def test_climb_distance():
    output = climb_distance(50.0, 43.7, 10.7)
    assert round(output, 0) == 33

class TakeOffConfiguration(TypedDict):
    v_s1: float  # stall speed $V_{s1}$
    thrust_vr: int  # thrust at rotation speed lb_f
    weight: int  # weight lb_f
    c_dmin: float # coefficient of drag minimum
    c_lmax: float # coefficient of lift maximum in take-off configuration
    s: float  # wing surface area, ft^2
    k: float # TODO: what is this constant?
    s_gr: float # ground roll distance, ft

def take_off_distance(h_obst: float, cfg: TakeOffConfiguration) -> float:
    """
    Total take-off distance required, ft
    s_gr: ground roll distance, ft
    h_obst: obstacle height, ft
    """
    v_tr = transition_speed(cfg["v_s1"])
    c_l = lift_coefficient(cfg["weight"], v_tr, cfg["s"])
    c_d = drag_coefficient_simplified(cfg["c_dmin"], cfg["k"], c_l)

    s_tr = transition_distance(cfg["v_s1"], cfg["thrust_vr"], cfg["weight"], c_l, c_d)

    a_tr = climb_angle(cfg["thrust_vr"], cfg["weight"], c_l, c_d)
    r = transition_radius(cfg["v_s1"])
    h_tr = transition_height(r, a_tr)

    to_distance = cfg["s_gr"] + s_tr

    if h_tr < h_obst:
        h_climb = climb_distance(h_obst, h_tr, a_tr)
        to_distance = to_distance + h_climb

    return to_distance

@pytest.mark.parametrize(
    "h_obst,expected,msg",
    [
        (30.0, 1505, "transition greater than obstacle"),
        (50.0, 1538, "transition less than obstacle"),
    ]
)
def test_take_off_distance(h_obst: float, expected: int, msg: str):
    cfg = TakeOffConfiguration(
        v_s1=108.0,
        thrust_vr=908,
        weight=3400,
        c_dmin=0.0350,
        c_lmax=1.69,
        s=144.9,
        k=0.04207,
        s_gr=1038.0,
    )
    output = take_off_distance(h_obst, cfg)
    assert round(output) == expected, msg
