// Actuator 1 pins
const int RPWM_Output_1 = 11;
const int LPWM_Output_1 = 10;
const int R_EN_1 = 13;
const int L_EN_1 = 12;

// Actuator 2 pins
const int RPWM_Output_2 = 6;
const int LPWM_Output_2 = 5;
const int R_EN_2 = 4;
const int L_EN_2 = 3;

enum Direction { STOPPED, EXTEND, RETRACT };

struct Actuator {
  int RPWM;
  int LPWM;
  int REN;
  int LEN;

  bool running = false;
  unsigned long startTime = 0;
  unsigned long duration = 0;
  Direction dir = STOPPED;

  Actuator(int r_pwm, int l_pwm, int r_en, int l_en) {
    RPWM = r_pwm;
    LPWM = l_pwm;
    REN = r_en;
    LEN = l_en;
  }

  void setupPins() {
    pinMode(RPWM, OUTPUT);
    pinMode(LPWM, OUTPUT);
    pinMode(REN, OUTPUT);
    pinMode(LEN, OUTPUT);
    stop();
  }

  void extend(unsigned long dur) {
    analogWrite(RPWM, 0);
    analogWrite(LPWM, 255);
    digitalWrite(REN, HIGH);
    digitalWrite(LEN, HIGH);
    startTime = millis();
    duration = dur;
    running = true;
    dir = EXTEND;
  }

  void retract(unsigned long dur) {
    analogWrite(RPWM, 255);
    analogWrite(LPWM, 0);
    digitalWrite(REN, HIGH);
    digitalWrite(LEN, HIGH);
    startTime = millis();
    duration = dur;
    running = true;
    dir = RETRACT;
  }

  void stop() {
    digitalWrite(REN, LOW);
    digitalWrite(LEN, LOW);
    running = false;
    dir = STOPPED;
  }

  void update() {
    if (running && millis() - startTime >= duration) {
      stop();
    }
  }
};

// Global actuator instances
Actuator actuator1(RPWM_Output_1, LPWM_Output_1, R_EN_1, L_EN_1);
Actuator actuator2(RPWM_Output_2, LPWM_Output_2, R_EN_2, L_EN_2);

void setup() {
  Serial.begin(115200);
  actuator1.setupPins();
  actuator2.setupPins();
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    int commaIndex = input.indexOf(',');
    if (commaIndex > 0) {
      String command = input.substring(0, commaIndex); // like "e1", "r2"
      String durationStr = input.substring(commaIndex + 1);
      int duration = durationStr.toInt();

      if (duration >= 100 && duration <= 750) {
        if (command == "e1") actuator1.extend(duration);
        else if (command == "r1") actuator1.retract(duration);
        else if (command == "e2") actuator2.extend(duration);
        else if (command == "r2") actuator2.retract(duration);
        else Serial.println("Invalid command");
      } else {
        Serial.println("Invalid duration (100–750 ms allowed)");
      }
    }
  }

  actuator1.update();
  actuator2.update();
}
