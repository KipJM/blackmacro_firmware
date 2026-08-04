## Global hardware definitions. Is this good architecture? probably not. ##
from micropython import const

## GPIO
# Switch
P_MT_COL1 = const(0); " Input, External pull-downs "
P_MT_COL2 = const(1); " Input, External pull-downs "
P_MT_COL3 = const(2); " Input, External pull-downs "
P_MT_COL4 = const(3); " Input, External pull-downs "

P_MT_CTRL1 = const(20); " Output "
P_MT_CTRL2 = const(21); " Output "
P_MT_CTRL3 = const(22); " Output "

# Regular encoders
P_RENC1_A = const(12); " Input "
P_RENC1_B = const(13); " Input "
P_RENC2_A = const(14); " Input "
P_RENC2_B = const(15); " Input "

# Others
P_CHRG    = const(19        ); " Input " # btw this can't be used to detect if usb is connected. This will turn off when the battery is full
P_VBUS    = const("WL_GPIO2"); " Input "
P_PWRSAVE = const("WL_GPIO1"); " Output  "


## I2C
ID_I2C      = const(0          )
P_I2C_SDA   = const(4          )
P_I2C_SCL   = const(5          )
I2C_FREQ    = const(400000     )
I2C_TIMEOUT = const(2000 * 1000) # microseconds

## MagEnc
ID_MAG_SSI   = const(0      )
P_MAG_DO     = const(16     )
P_MAG_CSN    = const(17     )
P_MAG_CLK    = const(18     )
MAG_SSI_FREQ = const(1000000) # Default 1MHz, max 8MHz
MAG_SSI_CPOL = const(1      ) # clock idle high
MAG_SSI_CPHA = const(0      ) # data sampled at falling edge

MSK_MAG_ANGL  = const(0b111111111111110000000000) ; SHFT_MAG_ANGL  = 10
MSK_MAG_FIELD = const(0b000000000000001100000000) ; SHFT_MAG_FIELD = 8
MSK_MAG_PUSH  = const(0b000000000000000010000000) ; SHFT_MAG_PUSH  = 7
MSK_MAG_STAT  = const(0b000000000000000001000000) ; SHFT_MAG_STAT  = 6
MSK_MAG_CHECK = const(0b000000000000000000111111) ; SHFT_MAG_CHECK = 0

## LED
P_LED     = const(26); " Output, NeoPixel "
COUNT_LED = const(21)

## Motor
# PWM
P_MOTR_UH = const(6 ); " Output, PWM "
P_MOTR_UL = const(7 ); " Output, PWM "
P_MOTR_VH = const(8 ); " Output, PWM "
P_MOTR_VL = const(9 ); " Output, PWM "
P_MOTR_WH = const(10); " Output, PWM "
P_MOTR_WL = const(11); " Output, PWM "

# Control
P_MOTR_VIO  = const(27); " Output "
P_MOTR_DIAG = const(28); " Input "

# mod is not included. if you wanna deal with that write your own firmware lol


# === Battery ===

BATTERY_CAPACITY          = const(6000                )
BATTERY_ENERGY            = int(BATTERY_CAPACITY * 3.7) # mWh, can't be made constant
BATTERY_TERMINATE_VOLTAGE = const(3000                )
BATTERY_TAPER_CURRENT     = const(1200 * 0.1          ) # HTP4056: 1.2A max charging, CV stops at 0.1 of charging current


# === HID EMULATION ===
HID_TIMEOUT = 10 # ms, max blocking time for hid send report