// Actuator 1 pins
const int RPWM_Output_1 = 11;
const int LPWM_Output_1 = 10;
const int R_EN_1 = 24;
const int L_EN_1 = 25;

// Actuator 2 pins
const int RPWM_Output_2 = 9;
const int LPWM_Output_2 = 8;
const int R_EN_2 = 26;
const int L_EN_2 = 27;

enum Direction { STOPPED, EXTEND, RETRACT };

struct Actuator {
  int RPWM;
  int LPWM;
  int REN;
  int LEN;

  bool running = false;
  unsigned long startTime = 0;
  unsigned long duration = 0;
  int pwmSpeed = 255;
  Direction dir = STOPPED;

  unsigned long fadeIn = 0;
  unsigned long fadeOut = 0;

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

  void extend(unsigned long dur, int speed, unsigned long fadeInMs = 0, unsigned long fadeOutMs = 0) {
    analogWrite(RPWM, 0);
    analogWrite(LPWM, 0);
    digitalWrite(REN, HIGH);
    digitalWrite(LEN, HIGH);
    startTime = millis();
    duration = dur;
    pwmSpeed = speed;
    fadeIn = fadeInMs;
    fadeOut = fadeOutMs;
    running = true;
    dir = EXTEND;
  }

  void retract(unsigned long dur, int speed, unsigned long fadeInMs = 0, unsigned long fadeOutMs = 0) {
    analogWrite(RPWM, 0);
    analogWrite(LPWM, 0);
    digitalWrite(REN, HIGH);
    digitalWrite(LEN, HIGH);
    startTime = millis();
    duration = dur;
    pwmSpeed = speed;
    fadeIn = fadeInMs;
    fadeOut = fadeOutMs;
    running = true;
    dir = RETRACT;
  }

  void stop() {
    analogWrite(RPWM, 0);
    analogWrite(LPWM, 0);
    digitalWrite(REN, LOW);
    digitalWrite(LEN, LOW);
    running = false;
    dir = STOPPED;
  }

  void update() {
    if (!running) return;

    unsigned long now = millis();
    unsigned long elapsed = now - startTime;

    if (elapsed >= duration) {
      stop();
      return;
    }

    int outputSpeed = pwmSpeed;

    // Fade-in
    if (fadeIn > 0 && elapsed < fadeIn) {
      float t = (float)elapsed / fadeIn;
      outputSpeed = (int)(pwmSpeed * t * t);
    }

    // Fade-out
    else if (fadeOut > 0 && elapsed > (duration - fadeOut)) {
      float t = (float)(duration - elapsed) / fadeOut;
      outputSpeed = (int)(pwmSpeed * t * t);
    }

    outputSpeed = constrain(outputSpeed, 0, 255);

    if (dir == EXTEND) {
      analogWrite(RPWM, 0);
      analogWrite(LPWM, outputSpeed);
    } else if (dir == RETRACT) {
      analogWrite(RPWM, outputSpeed);
      analogWrite(LPWM, 0);
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

    int c1 = input.indexOf(',');
    int c2 = input.indexOf(',', c1 + 1);
    int c3 = input.indexOf(',', c2 + 1);
    int c4 = input.indexOf(',', c3 + 1);

    if (c1 > 0 && c2 > c1 && c3 > c2) {
      String cmd = input.substring(0, c1);
      int dur = input.substring(c1 + 1, c2).toInt();
      int spd = input.substring(c2 + 1, c3).toInt();

      // Defaults
      int fadeIn = 0;
      int fadeOut = 0;

      if (c4 > c3) {
        fadeIn = input.substring(c3 + 1, c4).toInt();
        fadeOut = input.substring(c4 + 1).toInt();
      } else {
        fadeIn = input.substring(c3 + 1).toInt();
      }

      // Validate core values
      if (dur < 100 || dur > 2000 || spd < 0 || spd > 255) {
        Serial.println("Invalid duration or speed");
        return;
      }

      // Enforce: fadeIn + fadeOut ≤ duration
      if (fadeIn + fadeOut > dur) {
        fadeIn = dur / 2;
        fadeOut = dur - fadeIn;
        Serial.println("Fade-in + fade-out exceeded duration. Adjusted proportionally.");
      }

      // Execute command
      if (cmd == "e1") actuator1.extend(dur, spd, fadeIn, fadeOut);
      else if (cmd == "r1") actuator1.retract(dur, spd, fadeIn, fadeOut);
      else if (cmd == "e2") actuator2.extend(dur, spd, fadeIn, fadeOut);
      else if (cmd == "r2") actuator2.retract(dur, spd, fadeIn, fadeOut);
      else Serial.println("Invalid command");
    } else {
      Serial.println("Invalid format. Use: cmd,duration,speed[,fadeIn[,fadeOut]]");
    }
  }

  actuator1.update();
  actuator2.update();
}
