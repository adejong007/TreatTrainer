#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


#define servoPin    18
#define servoLow    50
#define servoHigh   100


int main (void)
{
    printf ("Raspberry Pi wiringPi test program\n") ;

    if (wiringPiSetupGpio() == -1)
        exit (1) ;


    pinMode(servoPin,PWM_OUTPUT);
    pwmSetMode(PWM_MODE_MS);
    pwmSetClock(384);
    pwmSetRange (1000) ;
    pwmWrite (18, servoLow);

    delay (1000);
    for(int i=0;i<5;i++)
    {
        pwmWrite(18,servoHigh);
        delay(1000);
        pwmWrite(18,servoLow);
        delay(1000);
    
    }

    return 0;
}
