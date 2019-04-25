#include <PubSubClient.h>
#include <ESP8266WiFi.h>

#define WIFI_AP "tapodi"
#define WIFI_PASSWORD "naolembro"
/***
* rede cabeana( arduino )
* 1x arduino  ( makete )
* 1x arduino  ( Sala )
* LDR, PIR, cabo flat (lixo eletronico)
* Manter V1, Manter V2
* testar Magnetic Contacts 
* RF Magnetic Contacts
placa para agregar alimentação dos sensores
* passar documentação financeira e valor para Edson
**/

#define TOKEN "xcyA1kC19wc3tI99MOHC"


char thingsboardServer[] = "192.168.100.2";

WiFiClient wifiClient;

// Initialize DHT sensor.
//DHT dht(DHTPIN, DHTTYPE);

PubSubClient client(wifiClient);

int status = WL_IDLE_STATUS;
unsigned long lastSend;

int ldr = A0;
int PIR = D7;
int Switcher = D5;
void setup()
{
  Serial.begin(115200);
  delay(10);
  InitWiFi();
  pinMode(ldr,INPUT);
  pinMode(PIR,OUTPUT);
  pinMode(Switcher,OUTPUT);
  client.setServer( thingsboardServer, 1883 );
  lastSend = 0;
}

void loop()
{
  if ( !client.connected() ) {
    reconnect();
  }

  if ( millis() - lastSend > 500 ) { // Update and send only after 1 seconds
    getData();
    lastSend = millis();
  }

  client.loop();
}

void getData()
{
  int t = analogRead(ldr);
  int pir = digitalRead(PIR);
  int swh = digitalRead(Switcher); // swicther 
  if ( isnan(t)) {
    return;
  }
  if (isnan(pir)) {
    return;
  }
  if (isnan(swh)){
    return;
  }

  Serial.print("Luminosidade: ");
  Serial.print(t);

  Serial.print("PIR: ");
  Serial.print(pir);

  Serial.print("Switcher: ");
  Serial.print(swh);


  String Status = String(t);
  String Status_pir = String(pir);
  String Status_swh = String(swh);


  // Just debug messages
  Serial.print( "Sensor de Luminosidade [" ); 
  Serial.print( Status );
  Serial.print( "]   -> " );

  // Prepare a JSON payload string
  String payload = "{";
  payload += "\"Status\":"; payload += Status;
  payload += "\"Status_PIR\":"; payload += Status_PIR; payload += ",";
  payload += "\"Status_switch\":"; payload += Status_swh;
  payload += "}";

  // Send payload
  char attributes[100];
  payload.toCharArray( attributes, 100 );
  client.publish( "v1/devices/me/telemetry", attributes );
  Serial.println( attributes );

}

void InitWiFi()
{
  Serial.println("Connecting to AP ...");
  // attempt to connect to WiFi network

  WiFi.begin(WIFI_AP, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to AP");
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    status = WiFi.status();
    if ( status != WL_CONNECTED) {
      WiFi.begin(WIFI_AP, WIFI_PASSWORD);
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
      Serial.println("Connected to AP");
    }
    Serial.print("Connecting to ThingsBoard node ...");
    // Attempt to connect (clientId, username, password)
    if ( client.connect("ESP8266 Device", TOKEN, NULL) ) {
      Serial.println( "[DONE]" );
    } else {
      Serial.print( "[FAILED] [ rc = " );
      Serial.print( client.state() );
      Serial.println( " : retrying in 5 seconds]" );
      // Wait 5 seconds before retrying
      delay( 5000 );
    }
  }
}




