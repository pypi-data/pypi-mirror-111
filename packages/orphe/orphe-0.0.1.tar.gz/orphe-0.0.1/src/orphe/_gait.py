# Copyright 2020 Aptpod, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
import pandas
from typing import Callable, List, Union

class Gait(object):
    time : pandas.Timedelta
    quaternion_w : float = None
    quaternion_x : float = None
    quaternion_y : float = None
    quaternion_z : float = None
    angular_velocity_x : float = None
    angular_velocity_y : float = None
    angular_velocity_z : float = None
    acc_x : float = None
    acc_y : float = None
    acc_z : float = None
    gravity_x : float = None
    gravity_y : float = None
    gravity_z : float = None
    euler_x : float = None
    euler_y : float = None
    euler_z : float = None

    analyzed : bool = False

    stride : float = None
    cadence : float = None
    speed : float = None
    pronation : float = None
    landing_force : float = None

    duration : float = None
    swing_phase_duration : float = None
    stance_phase_duration : float = None
    continuous_stance_phase_duration : float = None

    strike_angle : float = None
    toe_off_angle : float = None

    stride_maximum_vertical_height : float = None

    def __init__(self, time : pandas.Timedelta) -> None:
        self.time = time
    
    def _set(self, key : str, value : float):
        if key == "SHOES_QUATERNION_W":
            self.quaternion_w : float = value
        elif key == "SHOES_QUATERNION_X":
            self.quaternion_x : float = value
        elif key == "SHOES_QUATERNION_Y":
            self.quaternion_y : float = value
        elif key == "SHOES_QUATERNION_Z":
            self.quaternion_z : float = value
        elif key == "SHOES_ANGULAR_VELOCITY_X":
            self.angular_velocity_x : float = value
        elif key == "SHOES_ANGULAR_VELOCITY_Y":
            self.angular_velocity_y : float = value
        elif key == "SHOES_ANGULAR_VELOCITY_Z":
            self.angular_velocity_z : float = value
        elif key == "SHOES_ACC_X":
            self.acc_x : float = value
        elif key == "SHOES_ACC_Y":
            self.acc_y : float = value
        elif key == "SHOES_ACC_Z":
            self.acc_z : float = value
        elif key == "SHOES_ACC_OF_GRAVITY_X":
            self.gravity_x : float = value
        elif key == "SHOES_ACC_OF_GRAVITY_Y":
            self.gravity_y : float = value
        elif key == "SHOES_ACC_OF_GRAVITY_Z":
            self.gravity_z : float = value
        elif key == "SHOES_EULER_ANGLE_X":
            self.euler_x : float = value
        elif key == "SHOES_EULER_ANGLE_Y":
            self.euler_y : float = value
        elif key == "SHOES_EULER_ANGLE_Z":
            self.euler_z : float = value
        elif key == "STRIDE":
            self.analyzed = True
            self.stride : float = value
        elif key == "CADENCE":
            self.analyzed = True
            self.cadence : float = value
        elif key == "SPEED":
            self.analyzed = True
            self.speed : float = value
        elif key == "PRONATION":
            self.analyzed = True
            self.pronation : float = value
        elif key == "LANDINGFORCE":
            self.analyzed = True
            self.landing_force : float = value
        elif key == "DURATION":
            self.analyzed = True
            self.duration : float = value
        elif key == "SWINGPHASEDURATION":
            self.analyzed = True
            self.swing_phase_duration : float = value
        elif key == "STANCEPHASEDURATIONE":
            self.analyzed = True
            self.stance_phase_duration : float = value
        elif key == "CONTINUOUSSTANSPHASEDURATION":
            self.analyzed = True
            self.continuous_stance_phase_duration : float = value
        elif key == "STRIKEANGLE":
            self.analyzed = True
            self.strike_angle : float = value
        elif key == "TOEOFFANGLE":
            self.analyzed = True
            self.toe_off_angle : float = value
        elif key == "STRIDEMAXIMUMVERTICALHEIGHT":
            self.analyzed = True
            self.stride_maximum_vertical_height : float = value

class GaitAnalysis(object):
    left : Union[List[Gait], Gait] = []
    right : Union[List[Gait], Gait] = []        
