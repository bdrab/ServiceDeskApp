#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <SoftwareSerial.h>

#define rxPin D5
#define txPin D6

SoftwareSerial sim800(14, 12);
String data = "";


ESP8266WebServer server(80);
 
const char* ssid = "***";
const char* password =  "***";
 
void setup() {
 
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    sim800.begin(9600);
    sim800.println("AT+CMGF=1");

    while (WiFi.status() != WL_CONNECTED) {
 
        delay(500);
        Serial.println("Waiting to connect...");
 
    }
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
 
    server.on("/sms", smsHandler);
    server.onNotFound(otherHandler); 
    server.begin();
    Serial.println("Server listening");
    delay(2000);

}
 
void loop() {
    server.handleClient();
}
 
void smsHandler() {
  if (server.hasArg("text") == true){
    sendSMS(server.arg("phone"), server.arg("text"));
    server.send(200, "text/plain", "SMS has been sent.");
    return;
  } else{
    server.send(200, "text/plain", "SMS has not been sent.");
    return;
  }
}


void otherHandler(){
  String message = "Body received:\n";
  for(uint8_t i = 0; i< server.args(); i++){
    message +=server.argName(i) + " : " + server.arg(i) + "\n";
  }
  server.send(200, "text/plain", message);
  Serial.println(message);
}

void sendSMS(String phone, String text)
{
  if(text == "") {
    return;
  }
  sim800.print("AT+CMGF=1\r");
  delay(1000);
  sim800.print("AT+CMGS=\""+ phone +"\"\r");
  delay(1000);
  sim800.print(text);
  delay(100);
  sim800.write(0x1A);
  delay(1000);
  Serial.println("SMS Sent");
}