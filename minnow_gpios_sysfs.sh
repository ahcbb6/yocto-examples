######################################################
#  ****************************************
#  Testing GPIOS on Minnowboard Max       \
#  Using Yocto                            /
#                                         \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

# Minnowboard MAX with Calamari LURE

# Good read:
# http://elinux.org/Calamari_Lure

# LEDs
#  R = GPIO_S5_0    : MRAA 21 : Linux Sysfs GPIO = gpio338
#  G = GPIO_S5_0    : MRAA 23 : Linux Sysfs GPIO = gpio339
#  B = ILB_8254_SPKR    : MRAA 26 : Linux Sysfs GPIO = gpio464

# Assumes root permissions & proper kernel modules loaded

# Export GPIOS on SysFS
echo "338" > /sys/class/gpio/export
echo "339" > /sys/class/gpio/export
echo "464" > /sys/class/gpio/export

# Set GPIOS as outputs
echo "out" > /sys/class/gpio/gpio338/direction
echo "out" > /sys/class/gpio/gpio339/direction
echo "out" > /sys/class/gpio/gpio464/direction

# Turn on specific color
echo 1 > /sys/class/gpio/gpio338/value
#echo 1 > /sys/class/gpio/gpio339/value
#echo 1 > /sys/class/gpio/gpio464/value

# Turn off specific color
echo 0 > /sys/class/gpio/gpio338/value
#echo 0 > /sys/class/gpio/gpio339/value
#echo 0 > /sys/class/gpio/gpio464/value
