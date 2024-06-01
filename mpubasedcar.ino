#include "Wire.h"
#include <MPU6050_light.h>

const float MAX_SPEED = 255; // Maximum motor speed (0-255)
const float STRAIGHT_ANGLE = 0.0; // Target Z-angle for straight line (degrees)
const float ANGLE_TOLERANCE = 3.0;

const int motor1Pin1 = 3;
const int motor1Pin2 = 4;
const int motor2Pin1 = 5;
const int motor2Pin2 = 6;
const int motorEnable1 = 9;
const int motorEnable2 = 10;

MPU6050 mpu(Wire);
unsigned long timer = 0;
float zAngle; // Using zAngle from MPU6050_light library

struct MotorSpeeds {
    int leftSpeed;
    int rightSpeed;
};

void setup() {
    Serial.begin(9600);
    Wire.begin();

    byte status = mpu.begin();
    Serial.print(F("MPU6050 status: "));
    Serial.println(status);
    while (status != 0) {} // stop everything if could not connect to MPU6050

    Serial.println(F("Calculating offsets, do not move MPU6050"));
    delay(1000);
    mpu.calcOffsets(); // gyro and accelero
    Serial.println("Done!\n");

    pinMode(motor1Pin1, OUTPUT);
    pinMode(motor1Pin2, OUTPUT);
    pinMode(motor2Pin1, OUTPUT);
    pinMode(motor2Pin2, OUTPUT);
    pinMode(motorEnable1, OUTPUT);
    pinMode(motorEnable2, OUTPUT);

    // Set initial motor speeds
    analogWrite(motorEnable1, MAX_SPEED);
    analogWrite(motorEnable2, MAX_SPEED);

    // Set initial direction (both motors forward)
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
}

void loop() {
    mpu.update();
    zAngle = mpu.getAngleZ(); // Update the zAngle with the current reading

    if ((millis() - timer) > 10) {
        Serial.print("\tZ : ");
        Serial.println(zAngle);
        timer = millis();
        
        // Calculate the motor speeds based on the zAngle
        float angleError = STRAIGHT_ANGLE - zAngle;
        int leftSpeed, rightSpeed;
        
        // Map angleError to z
        float z = angleError;
        if (z > 15) z = 15;
        if (z < -15) z = -15;

        // Adjust speeds based on z
        MotorSpeeds speeds = adjust_speeds(z);
        leftSpeed = speeds.leftSpeed;
        rightSpeed = speeds.rightSpeed;
        
        // Apply the calculated speeds to the motors
        analogWrite(motorEnable1, leftSpeed);
        analogWrite(motorEnable2, rightSpeed);

        // Set motor directions based on the speeds
        if (leftSpeed >= rightSpeed) {
            // Left motor goes forward, right motor adjusts
            digitalWrite(motor1Pin1, HIGH);
            digitalWrite(motor1Pin2, LOW);
            digitalWrite(motor2Pin1, HIGH);
            digitalWrite(motor2Pin2, LOW);
        } else {
            // Right motor goes forward, left motor adjusts
            digitalWrite(motor1Pin1, HIGH);
            digitalWrite(motor1Pin2, LOW);
            digitalWrite(motor2Pin1, HIGH);
            digitalWrite(motor2Pin2, LOW);
        }
    }
}

// Function to adjust motor speeds based on the angle error
MotorSpeeds adjust_speeds(float z) {
    MotorSpeeds speeds;
    
    // Base value when z is between -3 and 3
    if (-3 <= z && z <= 3) {
        speeds.leftSpeed = 255;
        speeds.rightSpeed = 255;
    } else if (z > 3) { // Positive z between 3 and 30
        speeds.leftSpeed = 175 + (z - 3) * (255 - 175) / (15 - 3);
        speeds.rightSpeed = 175 - (z - 3) * (175 - 0) / (15 - 3);
    } else if (z < -3) { // Negative z between -3 and -30
        speeds.rightSpeed = 175 + (abs(z) - 3) * (255 - 175) / (15 - 3);
        speeds.leftSpeed = 175 - (abs(z) - 3) * (175 - 0) / (15 - 3);
    }

    Serial.print("\tleftS : ");
    Serial.println(speeds.leftSpeed);
    Serial.print("\trightS : ");
    Serial.println(speeds.rightSpeed);


    return speeds;
}
