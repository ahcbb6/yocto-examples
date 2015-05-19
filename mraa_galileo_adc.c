/*
######################################################
#  ****************************************
#  MRAA Test on C                         \
#  Read Analog values using Yocto & MRAA  /
#  Compilation inside Galileo Gen 2       \
#                                         /
#  Alejandro Enedino Hernandez Samaniego  \
#  alejandro.hernandez@linux.intel.com    /
#  alejandro.hernandez@intel.com          \
#  aehs29@ieee.org                        /
#  ****************************************
######################################################

Circuit:
Galileo Gen 2

Photoresistor   ADC0


Pass libMRAA to the linker:
gcc-lmraa mraa_galileo_adc.c -o mraa_adc

*/

#include <mraa/aio.h>
#include <time.h>

int main(){

        /* Delay to sleep for human sight*/
        struct timespec a,b;

        a.tv_sec = 0;
        a.tv_nsec = 500000000L;

        /* Golden Rule */
        mraa_aio_context adc_a0;
        uint16_t adc_value = 0;
        float adc_value_float = 0.0;

        /* Initialize Pin */
        adc_a0 = mraa_aio_init(0);
        if (adc_a0 ==NULL){
                return 1;
        }

        /* Read and print values Loopy-Loop */
        for(;;){
                adc_value = mraa_aio_read(adc_a0);
                adc_value_float = mraa_aio_read_float(adc_a0);
                fprintf(stdout, "ADC A0: %d\n", adc_value, adc_value);
                fprintf(stdout, "ADC A0 float: %.3f\n", adc_value_float);
                if(nanosleep(&a,&b)<0){
                        return 1;
                }
        }

        mraa_aio_close(adc_a0);
        return MRAA_SUCCESS;
}
