######################################################
#  ****************************************
#  MRAA Test on Minnowboard Max           \
#  Using Yocto                            /
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

# Minnowboard MAX with Calamari LURE
# Turns on an LED corresponding to the button pressed

# LEDs
#  R = GPIO_S5_0    : MRAA 21 : Linux Sysfs GPIO = gpio338
#  G = GPIO_S5_0    : MRAA 23 : Linux Sysfs GPIO = gpio339
#  B = ILB_8254_SPKR    : MRAA 26 : Linux Sysfs GPIO = gpio464

# Push Buttons
# R = I2S_CLK   : MRAA 14 : Linux Sysfs GPIO = gpio270
# G = UART1_CTS : MRAA 10 : Linux Sysfs GPIO = gpio266
# B = UART1_RTS : MRAA 12 : Linux Sysfs GPIO = gpio268


import mraa
import copy

# Declare GPIOS

# LEDs
rl = mraa.Gpio(21)
gl = mraa.Gpio(23)
bl = mraa.Gpio(26)

leds = [rl,gl,bl]


# Buttons
rb = mraa.Gpio(14)
gb = mraa.Gpio(10)
bb = mraa.Gpio(12)

pushbtns = [rb,gb,bb]


# Initialize resources

for led in leds:
    led.dir(0)    # 0 = MRAA_GPIO_OUT     see http://iotdk.intel.com/docs/master/mraa/gpio_8h.html#afcfd0cb57b9f605239767c4d18ed7304

for btn in pushbtns:
    btn.dir(1)    # 1 = MRAA_GPIO_IN


def turnOn(index):
    leds[index].write(1)

while (True):
    index = 0
    ledstmp = copy.copy(leds)
    for btn in pushbtns:
        if (btn.read()==0):
            turnOn(index)
            ledstmp.pop(index)
        else:
            index += 1
    for led in ledstmp:
        led.write(0)
