<!--

######################################################
#  ****************************************
#  Nginx + PHP Home Automation Server     \
#  Using Yocto                            /
#  Reading sensors, using outputs         \
#  & using a weather API (Yahoo)          /
#                                         \
#  Alejandro Enedino Hernandez Samaniego  /
#  alejandro.hernandez@linux.intel.com    \
#  alejandro.hernandez@intel.com          /
#  aehs29@ieee.org                        \
#  ****************************************
######################################################

Circuit

Galileo Gen 2

LED         Pin 2 (GPIO)
Photoresistor       ADC 0
Temperature Sensor  ADC 1

-->

<html>
<head>
</head>
<body>
<!-- Display query results   -->
<script>
  var callbackFunction = function(data) {
    var loc = data.query.results.channel.location;
        var astronomy= data.query.results.channel.astronomy;
        var item = data.query.results.channel.item;
        document.write("<h2>Clima para: " + loc.city + " " + loc.country +"");
        document.write("<p> Sunrise: " + astronomy.sunrise + "</p>");
        document.write("<p> Sunset: " + astronomy.sunset + "</p>");
        document.write("<p> Temperatura: " + item.condition.temp + " &deg;C </p>");
  };
</script>

<!--Request to get weather from Yahoo's RESTful API  -->

<script src="https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='zapopan,jal')&format=json&callback=callbackFunction"></script>

<?php
        // Turn On/Off LED
        function turnOn() {
                $gpioval = "/sys/class/gpio/gpio12/value";
                file_put_contents($gpioval,"1");
        }

        function turnOff() {
                $gpioval = "/sys/class/gpio/gpio12/value";
                file_put_contents($gpioval,"0");
        }

        // Call function according to POST value
        if ($_POST['on'] == 'On') {
                turnOn();
        }
        else{
                turnOff();
        }

        // Variables
        $A0file = "/sys/bus/iio/devices/iio:device0/in_voltage0_raw";
        $A1file = "/sys/bus/iio/devices/iio:device0/in_voltage1_raw";
        $uptimefile = "/proc/uptime";
        $gpioval = "/sys/class/gpio/gpio12/value";

        // Read Voltage from ADC's
        $A0 = file_get_contents($A0file);
        $A1 = file_get_contents($A1file);
        $ledstate = file_get_contents($gpioval);

    // Restore LED value
        $gpiodirection = "/sys/class/gpio/gpio12/direction";
        $gpiomuxerdir = "/sys/class/gpio/gpio28/direction";
        $gpiomuxer = "/sys/class/gpio/gpio28/value";
        file_put_contents($gpiodirection,"out");
        file_put_contents($gpiomuxerdir,"out");
        file_put_contents($gpiomuxer,"0");
        file_put_contents($gpioval,$ledstate);

        // Get system's uptime
        $uptime = file_get_contents($uptimefile);
        $uptmarray = explode(" ",$uptime);

        // Display results
        echo "Iluminacion: " . $A0 . "<p>";
        echo "Temperatura Cocina: " . $A1*.1220 .  " &degC; <p>";
        echo "Uptime: " . $uptmarray[0] . " segundos <p>";
        echo "Actuador (LED): " . $ledstate . "<p>";
?>

<!-- Forms to use the actuator -->

<form action="index.php" method="post"><input type="submit" name="on" value="On" style="height:50px; width:350px"/></>
<form action="index.php" method="post"><input type="submit" name="on" value="Off" style="height:50px; width:350px"/></>

</body>
</html>
