/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

/* Authors: Yoonseok Pyo, Leon Jung, Darby Lim, HanCheol Cho, Gilbert */

#include "turtlebot3.h"

Turtlebot3MotorDriver motor_driver;
float goal_velocity[2] = {0.1,0};
/*******************************************************************************
* Setup function
*******************************************************************************/
void setup()
{
  motor_driver.init(NAME);
}

void loop()
{
  //if (DEBUG_SERIAL.available())
  //{
  //int64_t received_data = int64_t(DEBUG_SERIAL.read());
  motor_driver.controlMotor(WHEEL_RADIUS, WHEEL_SEPARATION, goal_velocity);
  /*
  if (received_data == 'w' || received_data = 'W')
  {
    
  }

  else if (received_data == 'x' || received_data = 'X')
  {
    
  }

  else if (received_data == 'a' || received_data = 'A')
  {
    
  }

  else if (received_data == 'd' || received_data = 'D')
  {
    
  }

  else if (received_data == 's' || received_data = 'S')
  {
    
  }
  
  }
  */
  }
//}
/*
void write_angle(int id, int angle)
{
  dxl_comm_result = packetHandler->write4ByteTxRx(portHandler, id, 116, angle, &dxl_error);
    if (dxl_comm_result != COMM_SUCCESS)
    {
      Serial.print(packetHandler->getTxRxResult(dxl_comm_result));
    }
    else if (dxl_error != 0)
    {
      Serial.print(packetHandler->getRxPacketError(dxl_error));
    }
}
*/
