# Loxberry-Plugin-Mihome



Nach dem Herunterladen das Skript im Ordner /data/scripts/ öffnen und in der Datei run-mihome.py die Zeilen nach Bedarf anpassen:

  #Loxone Adresse und Port     
  
  UDP_IP = '192.168.178.32'   
  UDP_PORT = 5666

Dies ist die IP-Adresse Ihres Loxone Miniservers und der Port, auf den die Daten gesendet werden sollen.

##

In meiner Beispieldatei sendet die Anwendung Loxone-Daten an Port 5666, so dass es notwendig ist, die entsprechende virtuelle UDP-Eingabe in Loxone zu erstellen. Als Senderadresse können Sie die IP des Loxberry verwenden oder leer lassen:

![udpeingang](https://user-images.githubusercontent.com/32929378/36340498-3757a5e0-13de-11e8-83db-c82fe800b24d.png)

##

Nach Erstellung des UDP Eingangs, den UDP-Monitor öffnen um zu sehen, ob die Gateway-Daten erscheinen :


![digitalsensor erstellen](https://user-images.githubusercontent.com/32929378/36340528-358ec0ee-13df-11e8-9329-e4438ecc25d3.png)

Jetzt geht es nur darum, alle Features zu durchlaufen und deine UDP-Befehle zu erstellen. Jedes Gerät hat seine eindeutige Kennung, so gibt es also keine Konflikte.

##

* Gateway   
Helligkeit / "illumination \v"

* Taster 1-f    
Taste gedrückt (keine Flankenauswertung) / "click 1"    
Batteriespannung / "voltage \v"
* Würfel    
90° Drehung / "status flip90"   
180° Drehung / "status flip180"   
Verschieben / "status move"   
2x Klopfen / "status tap_twice"   
Schütteln / "status shake_air"    
Batteriespannung / "voltage \v"   
* Temperatur- und Feuchtemesser mini   
Temperatur / "temperature \v"   
Luftfeuchtigkeit / "humidity \v"    
Batteriespannung / "voltage \v"   
