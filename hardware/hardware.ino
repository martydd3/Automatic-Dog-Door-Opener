
int door_pin = 12;
int bell_pin = 11;
int led_pin = 13;

boolean door_on = false;
boolean bell_on = false;

unsigned long door_on_time;
unsigned long bell_on_time;

unsigned long door_delay = 1000UL;
unsigned long bell_delay = 500UL;

void setup() {
  // start serial port at 9600 bps:
  Serial.begin(9600);
  pinMode(door_pin, OUTPUT);
  pinMode(bell_pin, OUTPUT);
  pinMode(led_pin, OUTPUT);

  digitalWrite(led_pin, LOW);
  digitalWrite(door_pin, HIGH);
  digitalWrite(bell_pin, HIGH);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {

  if (Serial.available() > 0) {
    char inByte = Serial.read();

    if(inByte == 'd'){
      if(door_on){
        Serial.write('w');
      } else {
        Serial.write('r');
      }
      Serial.flush();
      
      door_on = true;
      door_on_time = millis();
      digitalWrite(led_pin, HIGH);
      digitalWrite(door_pin, LOW);
    }

    if(inByte == 'b'){
      if(bell_on){
        Serial.write('w');
      } else {
        Serial.write('r');
      }
      Serial.flush();
      
      bell_on = true;
      bell_on_time = millis();
      digitalWrite(led_pin, HIGH);
      digitalWrite(bell_pin, LOW);
    }
  }

  unsigned long current_time = millis();
  if(bell_on && (unsigned long)(current_time - bell_on_time) >= bell_delay){
    bell_on = false;
    digitalWrite(led_pin, LOW);
    digitalWrite(bell_pin, HIGH);
  }

  if(door_on && (unsigned long)(current_time - door_on_time) >= door_delay){
    door_on = false;
    digitalWrite(led_pin, LOW);
    digitalWrite(door_pin, HIGH);
  }
}
