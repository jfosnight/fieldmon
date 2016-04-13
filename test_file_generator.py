import random

f = open('test_data.csv', 'w')

f.write("temperature,humidity,soil_moisture,timestamp\r\n")

temp = random.randint(32,100)
humidity = random.randint(10,90)
soil_moisture = random.randint(10,90)

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

    m_sign = random.randint(0,1)
    if m_sign:
        soil_moisture += random.random()
    else:
        soil_moisture -= random.random()

    f.write("%.2f,%.2f,%.2f,%s\r\n" % (temp, humidity, soil_moisture, i,))

f.close()
