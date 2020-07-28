#include <ESP8266WiFiMulti.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <ArduinoOTA.h>
#include <Wire.h>

#include <vector>
#include "key.h"
//#include "lib-MPU.h"
//#include "lib-nodemcu.h"

using namespace std;

#define SDA D6
#define SCL D5

const uint8_t ACCEL_XOUT = 0x3B;
const uint8_t MPU_ADDR = 0x68;

const uint8_t PWR_MGMT_1 = 0x6B;
const uint8_t GYRO_CONFIG = 0x1B;
const uint8_t ACCEL_CONFIG = 0x1C;
const uint8_t GYRO_SCALE = 0b00000000;  //Escala do giroscopio: +-250 °/s
const uint8_t ACCEL_SCALE = 0b00001000; //Escala do acelerometro: +- 4 G

int16_t buff[7];
int16_t accel[3000][3];
int16_t gyro[3000][3];
int16_t temp[3000];
//vector<vector<int16_t>> sensorData;
//int16_t temp;
unsigned long prevTime = 0;
bool liveFlag = 0;
long liveInterval = 1000;
String msg;

ESP8266WiFiMulti wifiMulti;
StaticJsonDocument<200> data;

WiFiClient wifiClient;
PubSubClient MQTT(wifiClient);

void setupSensor();
void writeSensor(int REG, int VAL);
void readSensor();
void captureSensor(int nCapture, int nSample, int sampleRate);
void setupMQTT();
void setupWiFi();
void setupOTA();

void setup()
{
  Serial.begin(500000);
  Wire.begin(SDA, SCL);
  setupWiFi(wifiMulti);

  setupOTA();
  setupSensor();

  MQTT.setServer(broker_addr, broker_port);
  MQTT.setCallback(inputMQTT);
}

void loop()
{

  if (!MQTT.connected())
  {
    setupMQTT();
  }

  //aguarda OTA ou comando MQTT
  ArduinoOTA.handle();
  MQTT.loop();

  //só entrará nessa rotina a cada 'liveInterval' de tempo.
  unsigned long curTime = millis();
  if (curTime - prevTime >= liveInterval)
  {
    prevTime = curTime;

    //Funcao de analise em tempo real.
    if (liveFlag)
    {
      readSensor();

      msg = "[\t";
      for (int i = 0; i < 7; i++)
      {
        msg += buff[i];
        msg += "\t";
      }
      msg += "]";
      //msg+="hey";
      Serial.print("\n");
      Serial.print(msg);
      //Serial.print("hey");
      //MQTT.publish(outTopic, "Essa é uma captura");
    }
  }

  //  1
  //verifica wifi
  //se o wifi esta desconectado, tenta realizar conexao

  //tenta conectar ao broker
  //caso conectado, espera por um comando.

  //verifica o comando
  //caso seja 'captura em lote',
  //  2
  //receber detalhes da captura
  //conectar ao firebase (ordem pode ser invertida com o proximo passo)
  //realizar captura
  //transferir dados ao firebase
  //enviar status por MQTT
  //deve continuar?
  //caso positivo, retornar ao ponto '2'
  //caso negativo, fechar conexao com o broker e retornar ao ponto '1'

  //caso seja 'analise em tempo real',
  //  3
  //realizar captura
  //transferir captura (talvez por mqtt)
  //verificar se deve continuar
  //caso positivo, retornar ao ponto '3'
  //caso negativo, fechar conexao com o broker e retornar ao ponto '1'
}

///////////
///////////

void inputMQTT(char *topic, byte *payload, unsigned int length)
{
  String msg;

  for (int i = 0; i < length; i++)
  {
    char c = (char)payload[i];
    msg += c;
  }

  Serial.println("Input: " + msg);
  deserializeJson(data, msg);

  /*
      A mensagem recebida tem o formato:
      {"cmd":"xxxx","nCapture":yyyy,"nSample":zzzz,"sampleRate":aaaa}
  */

  if (data["cmd"] == "cmd_capt")
  {
    liveFlag = 0;
    Serial.println("\nCapture Mode.");

    Serial.print("Num. of captures: ");
    Serial.println(data["nCapture"].as<String>());
    Serial.print("Num. of samples:  ");
    Serial.println(data["nSample"].as<String>());
    Serial.print("Sample rate (ms): ");
    Serial.println(data["sampleRate"].as<String>());

    int nCapture = data["nCapture"];
    int nSample = data["nSample"];
    int sampleRate = data["sampleRate"];

    captureSensor(nCapture, nSample, sampleRate);
  }
  else if (data["cmd"] == "cmd_live")
  {
    liveFlag = 1;
    Serial.println("\nLive Mode.");

    liveInterval = data["sampleRate"];
  }
  else if (data["cmd"] == "cmd_stop")
  {
    liveInterval = 0;
    Serial.print("Parando operação...");
  }
  else
  {
    liveFlag = 0;
    Serial.println("Comando desconhecido. Tente novamente.\n");
  }
}

void setupOTA()
{
  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH)
    {
      type = "sketch";
    }
    else
    { // U_FS
      type = "filesystem";
    }

    // NOTE: if updating FS this would be the place to unmount FS using FS.end()
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR)
    {
      Serial.println("Auth Failed");
    }
    else if (error == OTA_BEGIN_ERROR)
    {
      Serial.println("Begin Failed");
    }
    else if (error == OTA_CONNECT_ERROR)
    {
      Serial.println("Connect Failed");
    }
    else if (error == OTA_RECEIVE_ERROR)
    {
      Serial.println("Receive Failed");
    }
    else if (error == OTA_END_ERROR)
    {
      Serial.println("End Failed");
    }
  });
  ArduinoOTA.begin();
  Serial.println("OTA Ready.");
}

void setupWiFi(ESP8266WiFiMulti wifiMulti)
{
  while (wifiMulti.run() != WL_CONNECTED)
  {
    WiFi.mode(WIFI_STA);
    wifiMulti.addAP(SSID_01, PASS_01);
    Serial.println("Trying to connect to WiFi.");
    delay(1000);
  }
  Serial.print("\nWiFi connected. IP ");
  Serial.println(WiFi.localIP());
}

void setupMQTT()
{

  String deviceID = "ESP8266Client-";
  deviceID += String(random(0xffff), HEX);

  Serial.println("Trying to connect to MQTT Broker.");
  if (MQTT.connect(deviceID.c_str()))
  {
    Serial.println("\nBroker connected!");
    MQTT.subscribe(inTopic);
  }
  else
  {
    Serial.println("Error. Trying again in 5 seconds.");
    delay(5000);
  }
}

void setupSensor()
{
  writeSensor(PWR_MGMT_1, 0);
  writeSensor(GYRO_CONFIG, GYRO_SCALE);
  writeSensor(ACCEL_CONFIG, ACCEL_SCALE);
}

void writeSensor(int REG, int VAL)
{
  Wire.beginTransmission(MPU_ADDR); //inicia a comunicacao com o endereço do MPU6050
  Wire.write(REG);                  //envia o registrador com o qual se deseja trabalhar
  Wire.write(VAL);                  //escreve o valor no registrador
  Wire.endTransmission();           //termina a transmissao
}

void readSensor()
{
  //buff.clear();

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(ACCEL_XOUT);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, (uint8_t)14);

  for (int i = 0; i < 7; i++)
  {
    buff[i] = Wire.read() << 8 | Wire.read();
    //buff.push_back(temp);
  }

  yield();
}

void captureSensor(int nCapture, int nSample, int sampleRate)
{
  for (int i = 0; i < nCapture; i++)
  {
    Serial.print("\n\nCaptura ");
    Serial.println(i);
    Serial.println("");
    for (int j = 0; j < nSample; j++)
    {
      readSensor();
      for (int k = 0; k < 3; k++)
      {
        accel[i][j] = buff[j];
        gyro[i][j] = buff[j + 4];
      }
      temp[i] = buff[3];

      //sensorData.push_back(buff);
      //Serial.print("Amostra ");
      //Serial.println(j);
      //adicionar os dados que acabaram de ser lidos ao vector.

      delay(sampleRate);
    }
    Serial.println("OK");
    MQTT.publish(outTopic,"ok");
    MQTT.loop(); // da um mqtt.loop só pra manter o broker conectado. Pode ser removido depois

    //captura x concluida;
    //conectar ao firebase e enviar o vector preenchido
  }
}
