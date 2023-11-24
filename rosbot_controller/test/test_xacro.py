# Copyright 2023 Husarion
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
# limitations under the License.

import os
import xacro
import itertools
from ament_index_python.packages import get_package_share_directory


def test_rosbot_description_parsing():
    mecanum_values = ["true", "false"]
    use_sim_values = ["true", "false"]
    use_gpu_values = ["true", "false"]
    simulation_engine_values = ["ignition-gazebo", "webots"]  # 'gazebo-classic'
    tf_prefixes = ["rosbot2r", "rosbot2pro", "husarion", "", "None"]

    all_combinations = list(
        itertools.product(
            mecanum_values, use_sim_values, use_gpu_values, simulation_engine_values, tf_prefixes
        )
    )

    for combination in all_combinations:
        mecanum, use_sim, use_gpu, simulation_engine, tf_prefix = combination
        mappings = {
            "mecanum": mecanum,
            "use_sim": use_sim,
            "use_gpu": use_gpu,
            "simulation_engine": simulation_engine,
            "tf_prefix": tf_prefix,
        }
        rosbot_description = get_package_share_directory("rosbot_description")
        xacro_path = os.path.join(rosbot_description, "urdf/rosbot.urdf.xacro")
        try:
            urdf = xacro.process_file(xacro_path, mappings=mappings)

            namespace = tf_prefix

            links = urdf.getElementsByTagName("link")
            for link in links:
                link_name = link.getAttribute("name")
                if namespace != "None":
                    if tf_prefix not in link_name:
                        assert False, f"Link name '{link_name}' does not contain '{namespace}'"
                else:
                    if tf_prefix in link_name:
                        assert False, f"Link name '{link_name}' does not contain '{namespace}'"

            joints = urdf.getElementsByTagName("joint")
            for joint in joints:
                joint_name = joint.getAttribute("name")
                if namespace != "None":
                    if tf_prefix not in joint_name:
                        assert False, f"Joint name '{joint_name}' does not contain '{namespace}'"
                else:
                    if tf_prefix in joint_name:
                        assert False, f"Joint name '{joint_name}' does not contain '{namespace}'"

        except xacro.XacroException as e:
            assert False, (
                f"xacro parsing failed: {str(e)} for mecanum: {mecanum}, use_sim:"
                f" {use_sim}, use_gpu: {use_gpu}, simulation_engine: {simulation_engine}"
            )
