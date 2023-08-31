#define LEDPIN 11

void setup() {
  //setup serial for monitor and setup Serial1 for bluetooth
  Serial.begin(9600);
  Serial1.begin(9600);
Serial.println("starting Downstream communication");
  pinMode(LEDPIN,OUTPUT);
}

void loop(){
  //Process commands from bluetooth first.
  if(Serial1.available()>0){
    String str= Serial1.readString().substring(1);
    Serial.println(str);
    if(str=="LED_ON"){
      digitalWrite(LEDPIN,HIGH);
      Serial.println("LED ON");
    } else if(str=="LED_OFF"){
      digitalWrite(LEDPIN,LOW);
      Serial.println("LED OFF");
    }
  }
}