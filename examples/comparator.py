# Simple demo of continuous ADC conversion mode for channel 0 of the ADS1x15 ADC
# with the comparator enabled.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

# Start continuous ADC conversions on channel 0 using the previously set gain
# value, and with the comparator enabled.  See the comparator section of the
# datasheet for information on what the comparator does, but at a high level
# the comparator can trigger the ALERT pin when an ADC value falls within
# (or outside) a provided threshold range.  The comparator can be configured with
# these parameters:
# - active_low: Boolean that indicates if ALERT is pulled low or high
#               when active/triggered.  Default is true, active low.
# - traditional: Boolean that indicates if the comparator is in traditional
#                mode where it fires when the value is within the threshold,
#                or in window mode where it fires when the value is _outside_
#                the threshold range.  Default is true, traditional mode.
# - latching: Boolean that indicates if the alert should be held until
#             get_last_result() is called to read the value and clear
#             the alert.  Default is false, non-latching.
# - num_readings: The number of readings that match the comparator before
#                 triggering the alert.  Can be 1, 2, or 4.  Default is 1.
# The call below will enable the comparator with its defaults and a threshold
# range of 5000-20000.  This means if the ADC value falls within 5000-20000 the
# ALERT pin will briefly be pulled low.
# Note you can also pass an optional data_rate parameter, see the simpletest.py
# example and read_adc function for more infromation.
adc.start_adc_comparator(0,  # Channel number
                         20000, 5000,  # High threshold value, low threshold value
                         active_low=True, traditional=True, latching=False,
                         num_readings=1, gain=GAIN)
# Once continuous ADC conversions are started you can call get_last_result() to
# retrieve the latest result, or stop_adc() to stop conversions.

# Note you can also call start_adc_difference_comparator() to take continuous
# differential readings with comparator enabled.  See the read_adc_difference()
# function in differential.py for more information and parameter description.

# Read channel 0 with comparator for 5 seconds and print out its values.
print('Reading ADS1x15 channel 0 for 5 seconds with comparator...')
start = time.time()
while (time.time() - start) <= 5.0:
    # Read the last ADC conversion value and print it out.
    value = adc.get_last_result()
    # WARNING! If you try to read any other ADC channel during this continuous
    # conversion (like by calling read_adc again) it will disable the
    # continuous conversion!
    print('Channel 0: {0}'.format(value))
    # Sleep for half a second.
    time.sleep(0.5)

# Stop continuous conversion.  After this point you can't get data from get_last_result!
adc.stop_adc()
