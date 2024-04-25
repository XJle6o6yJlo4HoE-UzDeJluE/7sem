import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac  = [8, 11, 7, 1, 0, 5, 12, 6]
troyka = 13
comp = 14

bits = len(dac)
levels = 2 ** bits

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)

def dec2bin(val):
    return [int(i) for i in bin(val)[2:].zfill(8)]

def adc():
    level = 0
    for i in range(bits - 1, -1, -1):
        level += 2**i
        GPIO.output(dac, dec2bin(level))
        time.sleep(0.01)
        comp_val  = GPIO.input(comp)
        if (comp_val == 1):
            level -= 2**i
    return level

def bin_num_leds(val):
    aboba = dec2bin(val)
    GPIO.output(dac, aboba)
    return aboba

data = []
data_times = []

try:
    # GPIO.output(troyka, 1)
    # time1 = time.time()
    # val = 0
    # while(val < 200):
    #     val = adc()
    #     bin_num_leds(val)
    #     data.append(val)
    #     data_times.append(time.time() - time1)
    #     print("volt - {:3}".format(val / levels * 3.3))
    # GPIO.output(troyka, 0)
    # while (val > 2):
    #     val = adc()
    #     bin_num_leds(val)
    #     data.append(val)
    #     data_times.append(time.time() - time1)
    # time2 = time.time()
    # with open("./settings.txt", "w") as f:
    #     f.write(str((time2 - time1) / len(data)))
    #     f.write("\n")
    #     f.write(str(3.3 / 256))
    start_time = time.time()
    val = 0

    GPIO.output(troyka, 1)
    while(val < 75):
        val = adc()
        print(val, "volts - {:3}".format(val / levels * 3.3))
        bin_num_leds(val)
        data.append(val)
        data_times.append(time.time() - start_time)

    GPIO.output(troyka, 0)
    while(val > 50 and val < 76):
        val = adc()
        print(val, "**volts - {:3}".format(val/levels * 3.3))
        bin_num_leds(val)
        data.append(val)
        data_times.append(time.time() - start_time)

    end_time = time.time()

    with open("./settings.txt", "w") as file:
        file.write(str((end_time - start_time) / len(data)))
        file.write(("\n"))
        file.write(str(3.3 / 256))

    print(end_time - start_time, " time\n", len(data) / (end_time - start_time), "\n", 3.3 / 256)

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

data_str = [str(i) for i in data]
data_times_str = [str(i) for i in data_times]

with open("./data.txt", "w") as f:
    f.write("\n".join(data_str))

plt.plot(data_times, data)
plt.show()