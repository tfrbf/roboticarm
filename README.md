# Robotic Arm with Force Feedback Control


## Overview

This repository contains the code and documentation for a robotic arm with force feedback control, developed as an undergraduate thesis project at [University of Tabriz](https://tabrizu.ac.ir/en), Faculty of Electrical and Computer Engineering under the supervision of [Dr.Badamchizadeh](https://scholar.google.com/citations?user=edtNtXAAAAAJ&hl=en). The project utilizes an Arduino microcontroller and a smart glove equipped with an FSR sensor to enable the robotic arm to apply force similar to a human hand.
### Applications 

 One prominent application of force feedback robots is in surgical procedures. Surgeons can utilize haptic feedback to perform minimally invasive surgeries with greater precision and control. By providing real-time force feedback, surgeons can better navigate delicate tissues and organs, reducing the risk of damage and improving patient outcomes. Additionally, force feedback robots enable remote surgeries, allowing expert surgeons to perform procedures from distant locations, potentially increasing access to specialized medical care in underserved areas.

In manufacturing, force feedback robots are crucial in assembly and quality control processes. These robots can delicately handle fragile components and perform intricate tasks with a high degree of accuracy. By providing operators with tactile feedback, force feedback robots enable them to detect defects or inconsistencies in products during the assembly process, ensuring high-quality standards and reducing waste.

Force feedback robots also find applications in virtual reality (VR) and augmented reality (AR) environments. By integrating haptic feedback into VR and AR simulations, users can experience a more immersive and realistic environment. This technology is particularly valuable in training simulations for tasks that require manual dexterity and tactile interaction, such as surgical training, vehicle operation, or equipment maintenance.


https://github.com/user-attachments/assets/ee541548-3434-4398-8c85-c36fef1b4215



## Components

1. Arduino Microcontroller(at least UNO)
2. Robotic Arm
3. [FSR sensors](https://www.amazon.com/Flexible-Resistors-Pressure-Compatible-microbit/dp/B08P8ZJ6KM/ref=sr_1_1?crid=1KHRGL5X0TVUJ&dib=eyJ2IjoiMSJ9.6ybxotGsCsxp8FxyL5e5-40k5xDhuIzEDWVSpX-RSSDTAhnEXbHKPzovYV4UPcNU.T0v7rWu6mG02m5Ld_45DwqRqr3NR29PGl4i74sZyq6I&dib_tag=se&keywords=fsr+sensor&qid=1725211210&sprefix=fsr+s%2Caps%2C293&sr=8-1) * 4 
4. [Servo motors](https://www.amazon.com/Miuzei-MG996R-Torque-Digital-Helicopter/dp/B0BZ4N367M/ref=sr_1_5?crid=2OBDSKIVTXU6K&dib=eyJ2IjoiMSJ9.H04An3S3wm6x0RUDr0virMG0F48JmxJ_VtqrtIOAsGeqnuu6cPx_y3PoNgJ_Ezi6hsyCx0FAtQsj8KclB8OGepWVMpm2Ccwt6W0h989P8edXsWwEV1FmIsJNuQJkNixAmdXfdX9KdMLkEdHTpHbjLr4SIgfBKxdYFqtgrz36zG6EwJJYtbA_2XOvbnJk3pJA3XtG_tl6V2P1ly1SLz_7ZXFMRTzIhQ9dnxF5MKxOvq4uSWGbVwhhk1o4BgOoWmhoLYnENefF07YaAeregMY_OtS7h7u9ZzuQsU9zRhYBSks.QJKESjWMaRz0y9q5GZ-b9r17GlAZdHDq7ojQVwXi5pw&dib_tag=se&keywords=servo%2Bmotor&qid=1725211297&sprefix=serv%2Caps%2C273&sr=8-5&th=1) * 6



## Setup Instructions:

1. **Hardware Setup:**
   - Please connect the robotic arm components (motors, grippers, etc.) to the Arduino board according to the circuit diagram provided in the documentation.
   - Ensure proper calibration and connection of the dynamometer sensor within the smart glove.

2. **Software Installation:**
   - Clone or download the repository from GitHub to your local machine.
   - Upload the Arduino sketch provided in the 'src' directory to the Arduino board using the Arduino IDE.

3. **Configuration:**
   - Adjust any parameters or constants in the Arduino sketch according to your specific hardware setup.
   - Calibrate the force feedback algorithm based on the dynamometer sensor readings to achieve the desired performance.
