import math

def dms2dec(grad, min, seg):
    """
    Convierte coordenadas de grados minutos a segundos a decimal
    """
    if grad > 0:
        dec = grad + min/60.0 + seg/3600.0
    else:
        dec = grad - min/60.0 - seg/3600.0

    return dec


def dec2dms(coord):
    """
    Convierte de coordenadas Decimal a Grado Minutos Segundos
    """
    sign = -1 if coord < 0 else 1
    coord = abs(coord)
    dd = int(coord)
    mm = int((coord - dd)*60)
    ss = (coord - dd - (mm/60.0))*3600

    return sign*dd, mm, ss


def obtener_p2(lat1, lon1, d, ang12):
    """
    Coordenadas de un punto dada una distancia y acimut a partir del punto P1
    """
    ang12 = 0 if ang12 == 360 else ang12

    lat1rad = math.radians(dms2dec(*lat1))
    lon1rad = math.radians(dms2dec(*lon1))

    # Formula 3
    d_grados = d / 111.18
    d_rad = math.radians(d_grados)
    ang12rad = math.radians(ang12)
    
    # Formula 1
    lat2 = math.asin(math.sin(lat1rad) * math.cos(d_rad) +
        math.cos(lat1rad) * math.sin(d_rad) * math.cos(ang12rad))

    x = math.cos(d_rad) - math.sin(lat1rad) * math.sin(lat2)
    y = math.cos(lat1rad) * math.cos(lat2)
    z = x / y
    if z > 1:
        z = 1
    # Formula 4
    k = math.acos(z)

    # Ajuste en el valor de k
    if ang12 >= 180 and ang12 < 360: k = -k
    
    # Formula 2
    lon2 = lon1rad + k

    return math.degrees(lat2), math.degrees(lon2)


# P1 --> 
lat1=[]
lat1.append(float(input("Ingrese los grados de la latitud de la torre:")))
lat1.append(float(input("Ingrese los minutos de la latitud de la torre:")))
lat1.append(float(input("Ingrese los segundos de la latitud de la torre:")))
lat1 = tuple(lat1)

lon1=[]
lon1.append(float(input("Ingrese los grados de la longitud de la torre:")))
lon1.append(float(input("Ingrese los minutos de la longitud de la torre:")))
lon1.append(float(input("Ingrese los segundos de la longitud de la torre:")))
lon1 = tuple(lon1)

distancia_general = [2, 10, 20, 50, 100]


opc = input(str('\n \n¿Desea colocar distancias especificas?(s o n) '))
distancia_opcional = []
if opc == "s":
    distancia_opcional.append(float(input("Ingrese la distancia")))
    opc = input(str('\n \n¿Desea colocar otra distancia?(s o n)'))
    while opc == "s":
        distancia_opcional.append(float(input("Ingrese la distancia: ")))
        opc = input(str('\n \n¿Desea colocar otra distancia?(s o n) '))
    
def convertidor(grado):
    grado = grado + 180
    if grado > 360:
        grado = grado -360
    return grado

ang_max = convertidor(int(input('Ingrese el ángulo de máximo lóbulo de radiación de la antena: \n')))
angulo = (ang_max, ang_max + 90, ang_max + 180, ang_max + 270)

print(f'\n \n \nAngulo de máximo lóbulo:{convertidor(ang_max)}')

for ang12 in angulo:
    if ang12 > 360:
        ang12 = ang12 - 360
    if ang12 != angulo[0]:print(f'Angulo:{convertidor(ang12)}')
    if distancia_opcional != []:
        distancia = distancia_opcional
    else:
        distancia = distancia_general
    distancia = list(map(lambda x: x / 1000, distancia))
    for d in distancia:
        lat2, lon2 = obtener_p2(lat1, lon1, d, ang12)
        print(f'    Distancia:{d * 1000} m')

        print('''      Latitud: {lat2[0]}° {lat2[1]}' {lat2[2]}"S \n      Longitud: {lon2[0]}° {lon2[1]}' {lon2[2]}"O\n'''.format(lat2=dec2dms(lat2), lon2=dec2dms(lon2))
        )
        #12 03 43.93
        #75 11 07.41