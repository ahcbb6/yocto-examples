/*
  #######################################################

  ****************************************
  Neural Network Color Classification    \
  Using Yocto & Numpy                    /
  Training Network Using Arduino IDE     \
                                         /
  Alejandro Enedino Hernandez Samaniego  \
  alejandro.hernandez@linux.intel.com    /
  alejandro.hernandez@intel.com          \
  aehs29@ieee.org                        /
  ****************************************

  ######################################################
*/

char category;
char * filename = "/opt/neural_training";
char TrainFlag = '0';
char TestFlag = '0';

void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  analogReadResolution(12);
}

void loop() {

  /* Check for serial command and react accordingly */

  if (Serial.available()){
    char cmd;
    cmd =  Serial.read();

    if (TrainFlag == '1' || TestFlag == '1') {
      if (cmd == 's'){
        // Stop Training
        TrainFlag = '0';
                TestFlag = '0';
        Serial.println("Stopping Training");
      }
    }
    else {
      switch (cmd){
      case 'r':
        //Train for Red
        Serial.println("Training for Red");
        TrainFlag = '1';
        category='1';
        break;
      case 'g':
        //Train for Green
        Serial.println("Training for Green");
        TrainFlag = '1';
        category='2';
        break;
      case 'b':
        //Train for Blue
        Serial.println("Training for Blue");
        TrainFlag = '1';
        category='3';
        break;
      case 'n':
        //Train for Nothing
        Serial.println("Training for Nothing");
        TrainFlag = '1';
        category='4';
        break;
      case 't':
        //Testing Measurement
        Serial.println("Testing Measurement");
        TestFlag = '1';
        break;
      }
    }
  }

  if (TrainFlag == '1'){
    // Read the input on analog pin 0
    int sensorValue = analogRead(A0);
    String output = String(sensorValue) + "," + category + "\n";
    char output_array [50];
    output.toCharArray(output_array,sizeof(output));
    FILE *fp;
    fp = fopen(filename, "a+");
    fputs(output_array,fp);
    fclose(fp);
    // Print out the value
    Serial.println(sensorValue);
    delay(50);        // delay in between reads for stability
  }

  if (TestFlag == '1'){
    // Read the input on analog pin 0
    int sensorValue = analogRead(A0);
    Serial.println(sensorValue);
    }
}
