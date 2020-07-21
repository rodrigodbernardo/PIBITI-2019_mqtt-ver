#include <Arduino.h>
#include <vector>

using namespace std;

class MPU {
  public:
    void setup();
    void write(int REG, int VAL);
    void read();
    void capture(int nCapture,int nSample,int sampleRate);
    
    //int16_t buff[7];
    vector<int16_t> buff;
    vector<vector<int16_t> > sensorData;
    int16_t temp;
  private:
    //futuramente, posso transformar essas constantes em variaveis no construtor da classe
    const uint8_t ACCEL_XOUT = 0x3B;
    const uint8_t MPU_ADDR = 0x68;

    const uint8_t PWR_MGMT_1 = 0x6B;
    const uint8_t GYRO_CONFIG = 0x1B;
    const uint8_t ACCEL_CONFIG = 0x1C;
    const uint8_t GYRO_SCALE = 0b00000000;  //Escala do giroscopio: +-250 °/s
    const uint8_t ACCEL_SCALE = 0b00001000; //Escala do acelerometro: +- 4 G
};
