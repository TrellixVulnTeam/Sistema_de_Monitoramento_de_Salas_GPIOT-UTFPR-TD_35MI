#include <PubSubClient.h>
#include <ESP8266WiFi.h>

#define WIFI_AP "WIFI ESSID"
#define WIFI_PASSWORD "PASSWORD WIFI"

#define TOKEN "TOKEN"

// DHT
#define DHTPIN 2
#define DHTTYPE DHT22

char thingsboardServer[] = "IP SERVER";

WiFiClient wifiClient;

// Initialize DHT sensor.
//DHT dht(DHTPIN, DHTTYPE);

PubSubClient client(wifiClient);

int status = WL_IDLE_STATUS;
unsigned long lastSend;

int PIR = D5;

void setup()
{
  Serial.begin(115200);
//  dht.begin();
  delay(10);
  InitWiFi();
  pinMode(PIR,INPUT);
  client.setServer( thingsboardServer, 1883 );
  lastSend = 0;
}

void loop()
{
  if ( !client.connected() ) {
    reconnect();
  }

  if ( millis() - lastSend > 1000 ) { // Update and send only after 1 seconds
    getData();
    lastSend = millis();
  }

  client.loop();
}

void getData()
{
  int t = digitalRead(PIR);

  if ( isnan(t)) {
    return;
  }
  Serial.print( "Sensor de Presença [" );
  Serial.print( Status );
  Serial.print( "]   -> " );
  String payload = "{";
  payload += "\"Status\":"; payload += Status;
  payload += "}";
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
