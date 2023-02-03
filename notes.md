All atmospheric data ias based on US Standard Atmosphere 1976, and in the troposphere (under 36,089 ft).

## 17.2 Take-off Run

table 17.2, T-O run segments
|Segment|Symbol|Airspeed|Section|
|:--|:--:|:--:|:--|
|Ground Roll|$S_G$|$V_R$|17.3.1 - 17.3.3|
|Rotation|$S_R$|$V_{LOF}$|7.3.4|
|Transition|$S_{TR}$|$V_{TR}$|17.3.5|
|Climb|$S_C$|$V_2$|17.3.6|

$V_1$ is the airspeed at which the aircraft can both be stopped by braking before the end of the runway, or still accelerated to lift-off in time (assuming a single engine fails on a multi-engine take off).
If below $V_1$ then stop on the brakes, if above $V_1$ then accelerate to take off.

table 17.3, Ground Roll Friction Coefficients, $\mu$
|Surface Type|Brakes Off|Braking|
|:--|:--:|:--:|
|Dry asphalt or concrete|0.03 - 0.05|0.3 - 0.5|


17.4; Acceleration on a flat runway:
Equation of motion for an aircraft during the ground run on a perfectly horizontal and flat runway:
$$
\frac{\delta{V}}{\delta{t}} = \frac{g}{W} \left[T - D - \mu(W - L) \right]
$$

$D$ = drag as a function of $V$, in $lb_f$ or $N$

$g$ = acceleration due to gravity, $ft/s^2$ or $m/s^2$

$L$ = lift as a function of $V$, in %lb_f$ or $N$

$T$ = thrust, in $lb_f$ or $N$

$W$ = weight, assumed constant in $lb_f$ or $N$

$\mu$ = ground friction coefficient taken from table 17.3

17.5 Acceleration on a sloped runway:
Runway with an uphill or downhill sloped runway.

$$
\frac{\delta{V}}{\delta{t}} = \frac{g}{W} \left[T - D - \mu(W \cos{\lambda} - L) - W \sin{\lambda} \right]
$$

where $\lambda$ = slope of runway in degrees (positive if uphill, negative if downhill)

17.6 Acceleration on a sloped runway in terms of thrust-to-weight ratio:
$$
\frac{\delta{V}}{\delta{t}} = g \left[\frac{T}{W} - \frac{D}{W} - \mu(\cos{\lambda} - \frac{L}{W}) - \sin{\lambda} \right]
$$


---

Lift Coefficient $C_L$:
$$
C_L = \frac{2W}{\rho V^2 S}
$$

Drag Coefficient $C_D$:
$$
C_D = C_Dmin + k C^2_L
$$

Climb Angle $\theta_{climb}$:
$$
\theta_{climb} = \sin^{-1} \left( \frac{T}{W} - \frac{1}{L/D} \right)
$$

Transition radius $R$:
$$
R \approx 0.2156 V^2_{S1}
$$

Transition distance $S_{TR}$:
$$
S_{TR} \approx 0.2156 \times V^2{S1} \times \left( \frac{T}{W} - \frac{1}{L/D} \right)
$$

Transition height $h_{TR}$:
$$
h_{TR} = R \left( 1 - \cos \theta_{climb} \right)
$$

Climb distance $S_C$:
$$
S_C = \frac{h{obst} - h{TR}}{\tan \theta_{climb}}
$$