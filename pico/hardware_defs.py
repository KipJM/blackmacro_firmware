## Global hardware definitions. Is this good architecture? probably not. ##

## GPIO
# Switch
P_MT_COL1 = 0; " Input, External pull-downs "
P_MT_COL2 = 1; " Input, External pull-downs "
P_MT_COL3 = 2; " Input, External pull-downs "
P_MT_COL4 = 3; " Input, External pull-downs "

P_MT_CTRL1 = 20; " Output "
P_MT_CTRL2 = 21; " Output "
P_MT_CTRL3 = 22; " Output "

# Regular encoders
P_RENC1_A = 12; " Input "
P_RENC1_B = 13; " Input "
P_RENC2_A = 14; " Input "
P_RENC2_B = 15; " Input "

# Others
P_CHRG    = 19        ; " Input " # btw this can't be used to detect if usb is connected. This will turn off when the battery is full
P_VBUS    = "WL_GPIO2"; " Input "
P_PWRSAVE = "WL_GPIO1"; " Output  "


## I2C
ID_I2C = 0
P_SDA  = 4
P_SCL  = 5

## MagEnc
ID_MAG_SSI = 0
P_MAG_DO   = 16
P_MAG_CSN  = 17
P_MAG_CLK  = 18

## LED
P_LED     = 26; " Output, NeoPixel "
COUNT_LED = 21

## Motor
# PWM
P_MOTR_UH = 6 ; " Output, PWM "
P_MOTR_UL = 7 ; " Output, PWM "
P_MOTR_VH = 8 ; " Output, PWM "
P_MOTR_VL = 9 ; " Output, PWM "
P_MOTR_WH = 10; " Output, PWM "
P_MOTR_WL = 11; " Output, PWM "

# Control
P_MOTR_VIO  = 27; " Output "
P_MOTR_DIAG = 28; " Input "

# mod is not included. if you wanna deal with that write your own firmware lol