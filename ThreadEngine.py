from queue import Queue
from threading import Thread
from PyQt5.QtCore import pyqtSignal
import random
import time
import data

global kecepatan
global jarak_tempuh
global temp_jarak_tempuh
global daya

kecepatan               = 0
jarak_tempuh            = 0
temp_jarak_tempuh       = 0
daya                    = 30000
pesan_aksi_sensor_jarak = ''

def sensorDepan(queueDepan):
    while True:
        value = random.randint(100, 3000)
        queueDepan.put(value)
        ui.txtSensorDepan.setText(translate("MainWindow", str(value/100)))
        time.sleep(1)

def sensorBelakang(queueBelakang):
    while True:
        value = random.randint(200, 3000)
        queueBelakang.put(value)
        ui.txtSensorBelakang.setText(translate("MainWindow", str(value/100)))
        time.sleep(1)

def sensorKanan(queueKanan):
    while True:
        value = random.randint(50, 500)
        queueKanan.put(value)
        ui.txtSensorKanan.setText(translate("MainWindow", str(value/100)))
        time.sleep(1)

def sensorKiri(queueKiri):
    while True:
        value = random.randint(50, 500)
        queueKiri.put(value)
        ui.txtSensorKiri.setText(translate("MainWindow", str(value/100)))
        time.sleep(1)

def sensorDepanKiri(queueDepanKiri):
    while True:
        value = random.randint(50, 500)
        queueDepanKiri.put(value)
        ui.txtSensorDepanKiri.setText(translate("MainWindow", str(value/100)))
        time.sleep(1)

def sensorDepanKanan(queueDepanKanan):
    while True:
        value = random.randint(50, 500)
        queueDepanKanan.put(value)
        ui.txtSensorDepanKanan.setText(translate("MainWindow", str(value/100)))
        time.sleep(1)

def tambahKecepatan(up):
    global kecepatan
    kecepatan += up

def kurangiKecepatan(down):
    global kecepatan
    kecepatan -= down

def kontrolJarak(sensor_depan, sensor_kiri, sensor_kanan, sensor_depan_kanan, sensor_depan_kiri):
    global kecepatan
    global pesan_aksi_sensor_jarak

    pesan_aksi_sensor_jarak = 'Jarak aman'

    if sensor_depan in range(0, 200):
        pesan_aksi_sensor_jarak = 'Jarak depan terlalu dekat. rem perlahan'
        if kecepatan in range(30, 60):
            kurangiKecepatan(20)

    if sensor_kiri in range(0, 200):
        pesan_aksi_sensor_jarak = 'Geser ke kanan'

    if sensor_kanan in range(0, 200):
        pesan_aksi_sensor_jarak = 'Geser ke kiri'

    if sensor_depan_kanan in range(50, 150):
        pesan_aksi_sensor_jarak = 'Geser serong kiri'

    if sensor_depan_kiri in range(50, 150):
        pesan_aksi_sensor_jarak = 'Geser serong kanan'

def kontrolKecepatan(sensor_depan):
    global kecepatan

    if sensor_depan in range(1000, 3000):
        if kecepatan > 65:
            kurangiKecepatan(5)
        else:
            tambahKecepatan(7)
    elif sensor_depan in range(700, 1000):
        if kecepatan > 65:
            kecepatan = 45
            kurangiKecepatan(5)
        else:
            tambahKecepatan(4)
    elif sensor_depan in range(400, 700):
        if kecepatan > 40:
            kecepatan = 30
            kurangiKecepatan(5)
        else:
            tambahKecepatan(2)

    elif sensor_depan in range(200, 400):
        if kecepatan > 40:
            kecepatan = 20
            kurangiKecepatan(5)
        else:
            tambahKecepatan(2)

def kontrolDaya():
    global kecepatan
    global daya

    if daya > 0:
        daya -= int(kecepatan / 3.6)
    else:
        time.sleep(10)

def GPS(queueGPS):
    global temp_jarak_tempuh
    global kecepatan

    index = 0
    mode = 'berangkat'

    while True : 
        temp_jarak_tempuh += int(kecepatan / 3.6)
        if temp_jarak_tempuh >= 10:

            if index == len(data.coordinates)-1:
                mode = 'pulang'
                kecepatan = 0
                ui.txtSpeedometer.setText(translate("MainWindow", str(kecepatan)))
                time.sleep(2)
            elif index == 0:
                mode = 'berangkat'
                kecepatan = 0
                ui.txtSpeedometer.setText(translate("MainWindow", str(kecepatan)))
                time.sleep(2)

            if mode == 'berangkat':
                index += 1
            else:
                index -= 1

            temp_jarak_tempuh = 0
        
        # set latitude and longitude
        ui.txtLatitude.setText(translate("MainWindow", str(data.coordinates[index][0])))
        ui.txtLongitude.setText(translate("MainWindow", str(data.coordinates[index][1])))

        queueGPS.put(data.coordinates[index])
        time.sleep(1)

def masterKontrol(queueDepan, queueBelakang, queueKanan, queueKiri, queueDepanKanan, queueDepanKiri, queueGPS):
    global daya
    global jarak_tempuh
    global pesan_aksi_sensor_jarak
    global kecepatan
    global barDaya

    ui.txtTotalDistance.setText(translate("MainWindow", str(int(data.getTotalDistance()))+' m'))

    while True:
        depan       = queueDepan.get()
        belakang    = queueBelakang.get()
        kanan       = queueKanan.get()
        kiri        = queueKiri.get()
        depanKanan  = queueDepanKanan.get()
        depanKiri   = queueDepanKiri.get()
        GPS         = queueGPS.get()
        
        # menampilkan kecepatan
        kontrolKecepatan(depan)
        ui.txtSpeedometer.setText(translate("MainWindow", str(kecepatan)))

        # menampilkan jarak tempuh
        jarak_tempuh += int(kecepatan / 3.6)
        ui.txtMileage.setText(translate("MainWindow", str(jarak_tempuh)).zfill(10))

        # menampilkan daya
        kontrolDaya()
        barDaya.emit(daya)
        barDaya.connect(ui.energyBar.setValue)

        # menampilkan pesan aksi sensor jarak
        kontrolJarak(depan, kiri, kanan, depanKanan, depanKiri)
        ui.txtSensorActionMessage.setText(translate("MainWindow", pesan_aksi_sensor_jarak))

        # GPS
        ui.marker.setLatLng(GPS)
        ui.map.setView(GPS, 20)

def go(_ui, _translate, progress):
    global ui
    global translate
    global barDaya

    ui              = _ui
    translate       = _translate
    barDaya         = progress

    queueDepan          = Queue()
    queueBelakang       = Queue()
    queueKanan          = Queue()
    queueKiri           = Queue()
    queueDepanKanan     = Queue()
    queueDepanKiri      = Queue()
    queueGPS            = Queue()

    threadDepan         = Thread(target=sensorDepan, args=(queueDepan,))
    threadBelakang      = Thread(target=sensorBelakang, args=(queueBelakang,))
    threadKanan         = Thread(target=sensorKanan, args=(queueKanan,))
    threadKiri          = Thread(target=sensorKiri, args=(queueKiri,))
    threadDepanKanan    = Thread(target=sensorDepanKanan, args=(queueDepanKanan,))
    threadDepanKiri     = Thread(target=sensorDepanKiri, args=(queueDepanKiri,))
    threadGPS           = Thread(target=GPS, args=(queueGPS,))
    threadMasterKontrol = Thread(target=masterKontrol, args=(queueDepan, queueBelakang, queueKanan, queueKiri, queueDepanKanan, queueDepanKiri, queueGPS,))

    threadDepan.start()
    threadBelakang.start()
    threadKanan.start()
    threadKiri.start()
    threadDepanKanan.start()
    threadDepanKiri.start()
    threadGPS.start()
    threadMasterKontrol.start()