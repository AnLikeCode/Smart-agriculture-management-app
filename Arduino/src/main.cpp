#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>
#include <SoftwareSerial.h>
#include <MQUnifiedsensor.h>

//-- Define các thành phần cần thiết
#define timewait 8500                       
#define rxZigbee 10
#define txZigbee 11
#define DHTPIN 2                             // Định nghĩa chân
#define DHTTYPE DHT11                        // Định nghĩa loại cảm biến sử dụng (DHT11, DHT22, DHT21)
#define BOARD "Arduino UNO"                  
#define PIN A0                               // Định nghĩa chân
#define VOLTAGE 5 
#define ADC_BIT_RESOLUTION 10                // Đặt Analog to digital converter bit là 10
#define RATIO_MQ135_CLEAN_AIR 3.6            // Tỷ lệ Không khí ô nhiễm / không khí sạch là 3.6 -> Được nhà sản xuất cảm biến cung cấp thông số

//-- Khởi tạo Sensor Object
BH1750 LightSensor;                          // Ở đây khởi tạo 2 đối tượng cảm biến là lightMeter thuộc kiểu BH1750 và dht thuộc DHT
DHT dht(DHTPIN, DHTTYPE);                    // Hàm này có 2 tham số, chân kết nối và loại cảm biến -> Do đó cần phải định nghĩa ở đoạn code 5 và 6
SoftwareSerial ZigbeeCom(rxZigbee, txZigbee);             
MQUnifiedsensor MQ135(BOARD, VOLTAGE, ADC_BIT_RESOLUTION, PIN, "MQ-135");

//-- Tạo Packet Logic gửi qua Serial Zigbee
String Packet(float lux, float temperature, float humidity, float co2, float smoke, float SoilHumidityPercent) {
  String data = "";
  data += String(lux) + ",";
  data += String(temperature) + ",";
  data += String(humidity) + ",";
  data += String(co2) + ",";
  data += String(smoke) + ",";
  data += String(SoilHumidityPercent);
  return data;
}

float calculate_soil_moisture_percentage(int SoilSensorValue){
  return 100 - (SoilSensorValue / 1023.0) * 100; ;
}

void setup() {
  Wire.begin();                              // Khởi tạo giao tiếp I2C trên Arduino.
  ZigbeeCom.begin(9600);                     // Khởi tạo cổng Serial với tốc độ 9600 bps
  LightSensor.begin();          
  dht.begin(); 
  MQ135.setRegressionMethod(1);              // Phương pháp hồi quy tuyến tính
  MQ135.init();                              // Khởi tạo cảm biến   
  //-- Hiệu chỉnh R0 trên MQ135
  float tmp = 0;                             // Khởi tạo biến tạm để tính cộng dồn giá trị R0 -> R0 là giá trị điện trở của cảm biến trong không khí sạch
  for (int i = 1; i <= 10; i++) {
    MQ135.update();
    tmp += MQ135.calibrate(RATIO_MQ135_CLEAN_AIR);
  }
  tmp = tmp / 10;                            // Tính trung bình R0
  MQ135.setR0(tmp);  
  pinMode(A1, INPUT);
}

void loop() {
  MQ135.update();
  //-- Đọc nồng độ CO2
  MQ135.setA(605.18);                         // Hằng số A cho CO2 (theo datasheet)
  MQ135.setB(-3.937);                         // Hằng số B cho CO2 (theo datasheet)
  MQ135.update();
  float co2 = MQ135.readSensor();
  
  //-- Đọc nồng độ khói -> Để báo cháy
  MQ135.setA(110.47);                         // Hằng số A cho khói
  MQ135.setB(-2.862);                         // Hằng số B cho khói
  MQ135.update();     
  float smoke = MQ135.readSensor();

  //-- Đọc dữ liệu từ cảm biến và Gán vào các biến
  float lux = LightSensor.readLightLevel();
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float SoilHumidityPercent = calculate_soil_moisture_percentage(analogRead(A1));                  
  //-- Gửi Packet qua Serial Zigbee
  if (isnan(lux) || isnan(temperature) || isnan(humidity) || isnan(co2) || isnan(smoke) || isnan(SoilHumidityPercent) ) { 
    //-- Check coi giá trị của mấy biến này -> Nếu là NaN (tức là một giá trị đặc biệt gì đó) thì print lỗi
    Serial.println("Failed to read from Sensors!");
  } else {
    ZigbeeCom.println(Packet(lux, temperature, humidity, co2, smoke, SoilHumidityPercent));
  }
  delay(timewait); 
}