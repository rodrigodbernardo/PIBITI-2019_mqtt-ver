class Nodemcu {
  public:
    void setupMQTT(ESP8266WiFiMulti wifiMulti,PubSubClient MQTT);
    void setupWiFi(ESP8266WiFiMulti wifiMulti);
    void setupOTA();
  private:
    const char* SSID_01   = "FLAVIO_02";
    const char* PASS_01   = "8861854611";
};
