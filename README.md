# 🌱 ỨNG DỤNG WEB QUẢN LÝ NÔNG NGHIỆP THÔNG MINH  
**Triển khai với mạch nhúng & mạng Zigbee**

---
  
## 📄 Tóm tắt  
  
Project tập trung vào việc tìm hiểu tổng quan, chuyên sâu về công nghệ mạng Zigbee, các thiết bị phần cứng, cảm biến, các mạch nhúng, cùng với đó là tìm hiểu về các cơ sở dữ liệu công khai được cung cấp thông qua Cloud như Firebase, dịch vụ Neon Serverless Postgres. Ngoài ra, Project cũng tìm hiểu về cách cài đặt, triển khai hệ điều hành Ubuntu, hệ thống nhúng Raspberry Pi 3 để tiếp nhận dữ liệu từ các mạch nhúng và thực hiện giao tiếp với cơ sở dữ liệu công khai. Cuối cùng là tập trung tìm hiểu về cách xây dựng ứng dụng web phục vụ cho việc theo dõi, quản lý dữ liệu thu thập được từ các cảm biến để hỗ trợ phân tích và hậu xử lý.

---
  
## 🏗 Kiến trúc hệ thống  
  
![System Architecture](https://blogwithanio.notion.site/image/attachment%3Aa7bdf84e-1c0b-43d1-a7b9-f81fe0f235c8%3Aiotproject.png?table=block&id=250695a7-6e5a-802f-a847-f2221cbe0a6f&spaceId=6e2e73db-19d0-473a-98f9-56a3b327b51e&width=2000&userId=&cache=v2)  

---
  
## 🚀 Tính năng chính  
  
- Ghi nhận, giám sát các thông số môi trường (nhiệt độ, độ ẩm, ánh sáng, v.v.). 
- Hỗ trợ kết nối phân tán và truyền dữ liệu qua mạng Zigbee. 
- Ứng dụng Web hiển thị và theo dõi dữ liệu thời gian thực. 
- Hỗ trợ lưu trữ dữ liệu lâu dài phục vụ quản lý và phân tích sau. 
- Báo cháy, hỏa hoạn đến người dùng thông qua Telegram khi chỉ số khói vượt ngưỡng.

---
  
## 📂 Cấu trúc thư mục  
  
```plaintext
Embedded-System/      # Mã nguồn hệ thống nhúng (Arduino, cảm biến, Zigbee)
PythonCode/           # Ứng dụng Python (Dashboard, xử lý dữ liệu, kết nối DB)
SmartAgricultureApplicationsFirebaseServiceAccount.json # Tài khoản dịch vụ Firebase (ẩn thông tin)
.gitignore            # Cấu hình bỏ qua file/thư mục trong Git
README.md             # Tài liệu mô tả dự án
```

---
  
## 🛠 Ngôn ngữ & Công nghệ sử dụng
  
| Lĩnh vực | Công nghệ / Ngôn ngữ |
| :--- | :--- |
| **Ngôn ngữ lập trình** | • C++ <br> • Python |
| **Mạng và Truyền thông** | • Zigbee (chuẩn IEEE 802.15.4) <br> • UART TTL <br> • I2C |
| **Cơ sở dữ liệu & Cloud** | • Firebase Realtime Database <br> • Neon Serverless Postgres <br> • Streamlit Cloud |
| **Framework & Công cụ** | • Streamlit <br> • PlatformIO IDE <br> • Telegram API |


---
  
## ⚙ Thiết bị phần cứng & Thông số kỹ thuật
  
| Thiết bị | Thông số kỹ thuật |
| :--- | :--- |
| **Module RF Zigbee CC2530** | • **Model:** DL-20 <br> • **IC:** CC2530 <br> • **Điện áp hoạt động:** 3 ~ 5.5 VDC <br> • **Dòng tiêu thụ:** < 30mA <br> • **Tốc độ truyền:** Lên đến 3300Bps <br> • **Khoảng cách truyền:** 250m (điều kiện lý tưởng) <br> • **Chuẩn sóng:** Zigbee 2.4G <br> • **Giao thức:** UART TTL <br> • **Baudrate:** 2400 đến 115200 |
| **Arduino Uno R3** | • **Vi điều khiển:** ATmega328 (8-bit) <br> • **Điện áp hoạt động:** 5 ~ 12V DC <br> • **Tần số hoạt động:** 16 MHz <br> • **Chân I/O:** 14 Digital (6 PWM), 6 Analog <br> • **Bộ nhớ:** 32 KB Flash, 2 KB SRAM, 1 KB EEPROM <br> • **Dòng tối đa/chân I/O:** 30 mA |
| **Raspberry Pi 3 Model B+**| • **CPU:** Broadcom BCM2837B0, quad-core ARM Cortex-A53 @ 1.4GHz <br> • **RAM:** 1GB LPDDR2 SDRAM <br> • **Kết nối:** Wi-Fi 2.4/5GHz, Bluetooth 4.2/BLE, Ethernet <br> • **GPIO:** 40 chân mở rộng <br> • **Nguồn:** 5V/2.5A qua microUSB hoặc 5V qua GPIO, hỗ trợ PoE |
| **Các cảm biến** | • **Cảm biến chất lượng không khí:** MQ-135 <br> • **Cảm biến cường độ ánh sáng:** Lux BH1750 <br> • **Cảm biến nhiệt độ và độ ẩm:** DHT11 <br> • **Cảm biến độ ẩm đất** |

---
  
## 🤝 Đóng góp
Mọi ý kiến đóng góp đều được hoan nghênh!