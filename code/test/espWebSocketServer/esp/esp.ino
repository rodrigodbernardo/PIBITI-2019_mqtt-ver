#include <ESP8266WiFiMulti.h>

ESP8266WiFiMulti wifiMulti

void setup(){

}

void loop(){

}

///////////
///////////

void setupWiFi(){
    // ----> A FAZER
    //  ADICIONAR FUNÇÃO WPS.

    WiFi.mode(WIFI_STA);
    wifiMulti.addAP("FLAVIO_02","8861854611");

    Serial.print("Trying to connect to WiFi");
    while(wifiMulti.run() != WL_CONNECTED){
        delay(500);
        Serial.print(".");
    }
    Serial.println("\n\nWiFi connected successfully!");
    Serial.println(WiFi.localIP());
}