#include <string.h>
#include <ESP8266WiFi.h>  //essa biblioteca j� vem com a IDE. Portanto, n�o � preciso baixar nenhuma biblioteca adicional
#include <PubSubClient.h> // Importa a Biblioteca PubSubClient


WiFiClient clientMQTT;
WiFiClient client;
long ultimo_envio;
PubSubClient MQTT(clientMQTT); // Instancia o Cliente MQTT passando o objeto clientMQTT

int states;

#define SSID_REDE     "tapodi"    // nome da rede 
#define SENHA_REDE    "naolembro"        // senha da rede 
#define IP_BROKER     "192.168.100.3"       // IP DO BROKER LOCAL
#define TOPICO         "home/sala/janela/01/status/" //  IoT Windows
// "bloco/E/lab/302/SENSOR/JANELA/1"

int switcher = 13;

void setup(){
  Serial.begin(115200);
  initWiFi();
  initMQTT();
  ultimo_envio = 0;
  pinMode(switcher,INPUT);
  
}

void loop() {
 
 char getData[100];
  strcpy(getData,PegarDado());  
 
  delay(50);
  
  VerificaConexoesWiFIEMQTT(); 
  
if(!client.connected())
    {
        VerificaConexoesWiFIEMQTT(); 
    }
 
    //verifica se � o momento de enviar informa��es via MQTT
    if ((millis() - ultimo_envio) > 100)
    {
         Serial.println(getData);
         MQTT.publish(TOPICO, getData);
         ultimo_envio = millis();
    }
    
    delay(100);
  
}

void initWiFi() 
{
    delay(10);
    Serial.println("------Conexao WI-FI------");
    Serial.print("Conectando-se na rede: ");
    Serial.println("qual e a senha");
    Serial.println("Aguarde");
    reconectWiFi();
}


void initMQTT() 
{
    MQTT.setServer(IP_BROKER, 1883);   //informa qual broker e porta deve ser conectado
    MQTT.setCallback(mqtt_callback);            //atribui fun��o de callback (fun��o chamada quando qualquer informa��o de um dos t�picos subescritos chega)
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) 
{
        
}




void reconectWiFi() 
{
    if (WiFi.status() == WL_CONNECTED)
        return;
         
    WiFi.begin(SSID_REDE, SENHA_REDE); // Conecta na rede WI-FI
     
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(100);
        Serial.print(".");
    }
   
    Serial.println();
    Serial.print("Conectado com sucesso na rede ");
    Serial.print("qual e a senha");
    Serial.println("IP obtido: ");
    Serial.println(WiFi.localIP());
}

void reconnectMQTT() 
{
    while (!MQTT.connected()) 
    {
        Serial.print("* Tentando se conectar ao Broker MQTT: ");
        Serial.println(IP_BROKER);
        if (MQTT.connect("IoT:01")) 
        {
            Serial.println("Conectado com sucesso ao broker MQTT!");
            MQTT.subscribe("IoT: 01 ONLINE"); 
        } 
        else
        {
            Serial.println("Falha ao reconectar no broker.");
            Serial.println("Havera nova tentatica de conexao em 2s");
            delay(2000);
        }
    }
}

void VerificaConexoesWiFIEMQTT(void)
{
    if (!MQTT.connected()) 
        reconnectMQTT(); //se n�o h� conex�o com o Broker, a conex�o � refeita
     
     reconectWiFi(); //se n�o h� conex�o com o WiFI, a conex�o � refeita
}

 
char* PegarDado(){
  states  =   digitalRead(switcher);
  static char data[100];
  sprintf(data, "%d ",states);
  return data;
}
