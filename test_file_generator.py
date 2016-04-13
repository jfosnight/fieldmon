import random

f = open('test_data.csv', 'w')

f.write("temperature,humidity,timestamp\r\n")

temp = random.randint(32,100)
humidity = random.randint(10,90)

for i in range(0,100):
    t_sign = random.randint(0,1)
    if t_sign:
        temp += random.random()
    else:
        temp -= random.random()

    h_sign = random.randint(0,1)
    if h_sign:
        humidity += random.random()
    else:
        humidity -= random.random()

    f.write("%.2f,%.2f,%s\r\n" % (temp, humidity, i,))

f.close()
