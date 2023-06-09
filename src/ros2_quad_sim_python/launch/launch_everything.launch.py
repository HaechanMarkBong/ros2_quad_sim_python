import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
   town = LaunchConfiguration('town')
   town_launch_arg = DeclareLaunchArgument(
      'town',
      default_value='Town01'
   )
   carla_bridge = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('carla_ros_bridge'), 'carla_ros_bridge.launch.py')]
      ),
      launch_arguments={'town': town}.items(),
      )
   objects_definition_file = LaunchConfiguration('objects_definition_file')
   objects_definition_file_arg = DeclareLaunchArgument(
      'objects_definition_file',
      default_value=os.path.join(get_package_share_directory('ros2_quad_sim_python'),'cfg/flying_sensor.json')
   )
   carla_spawn_objects = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('carla_spawn_objects'), 'carla_spawn_objects.launch.py')]),
      launch_arguments={'objects_definition_file': objects_definition_file}.items(),
      )
   
   quad_params = {
         'target_frame': 'flying_sensor', 
         'map_frame': 'map', 
         'init_pose': '[0,0,2,0,0,0]',
         # Position P gains
         'Px': '5.0',
         'Py': '5.0',
         'Pz': '2.0',
         # Velocity PID gains
         "Pxdot" : '5.0',
         "Dxdot" : '0.5',
         "Ixdot" : '5.0',
         "Pydot" : '5.0',
         "Dydot" : '0.5',
         "Iydot" : '5.0',
         "Pzdot" : '4.0',
         "Dzdot" : '0.5',
         "Izdot" : '5.0',
         # Attitude P gains
         "Pphi"   : '4.0',
         "Ptheta" : '4.0',
         "Ppsi"   : '1.5',
         # Rate P-D gains
         "Pp" : '1.5',
         "Dp" : '0.04',
         "Pq" : '1.5',
         "Dq" : '0.04',
         "Pr" : '1.0',
         "Dr" : '0.1',
         # Max Velocities (x,y,z) [m/s]
         "uMax" : '50.0',
         "vMax" : '50.0',
         "wMax" : '50.0',
         "saturateVel_separately" : 'True',
         # Max tilt [degrees]
         'tiltMax': '30.0',
         # Max Rate [rad/s]
         "pMax" : '200.0',
         "qMax" : '200.0',
         "rMax" : '150.0',
         # Minimum velocity for yaw follow to kick in [m/s]
         "minTotalVel_YawFollow" : '0.1',
         # Include integral gains in linear velocity control
         "useIntegral" : 'True',
         }
   quad_params_lcgf = {k: LaunchConfiguration(k) for k in quad_params.keys()}
   quad_params_arg = [DeclareLaunchArgument(k, default_value=v) for k,v in quad_params.items()]
   quad = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('ros2_quad_sim_python'), 'quad.launch.py')]),
      launch_arguments=quad_params_lcgf.items(),
      )

   return LaunchDescription([
      town_launch_arg,
      carla_bridge,
      objects_definition_file_arg,
      carla_spawn_objects,
      *quad_params_arg,
      quad,
      Node(
         package='rviz2',
         executable='rviz2',
         name='rviz2',
         arguments=['-d', os.path.join(get_package_share_directory('ros2_quad_sim_python'), 'cfg/rviz_flying_sensor.rviz')]
      )
   ])