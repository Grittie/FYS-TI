#include <Arduino.h>

// Tasks
TaskHandle_t TSelectUpdate, TButtonUpdate, TGameTimer, TReset;

// Buttons
int led_pins[] = {17, 4, 5, 6, 16, 7, 15};
int button_pins[] = {8, 18, 3, 9, 11, 46, 10};
int button_states[] = {0, 0, 0, 0, 0, 0, 0}; // 0 = not pressed, 1 = pressed
int led_length = sizeof(led_length) / sizeof(int);
int button_length = sizeof(button_pins) / sizeof(int);
int sel_button_index = -1;
int prev_sel_button = -1;

// Games
int game_timer = 30000;
float select_timer = 1000;
bool update_game = false;
int start_button_index = 3;
int score = 0;
int result_timer = 10000;
bool is_idle = false;

bool reset_update = false;

// ESP_L
int plus_pin = 1;
int reset_pin = 42;

void SelectUpdate(void *pvParameters)
{
  Serial.print("SelectUpdate running on core\n");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    if (update_game) {
      // Select a random led to turn on
      do
      {
        sel_button_index = random(0, led_length + 1);
      } while (prev_sel_button == sel_button_index);
      prev_sel_button = sel_button_index;

      Serial.printf("Pin: %d\n", sel_button_index);
      digitalWrite(led_pins[sel_button_index], HIGH);

      delay(select_timer);
      digitalWrite(led_pins[sel_button_index], LOW);
    }

    delay(200);
  }
}

void ButtonUpdate(void *pvParameters)
{
  Serial.print("ButtonUpdate running on core\n");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    if (update_game) {
      for (size_t i = 0; i < button_length; i++)
      {
        int buttonState = digitalRead(button_pins[i]);

        // Check if the button is pressed
        if (buttonState == LOW) {
          if (button_states[i] == 0) {
            Serial.printf("Pin: %d, LOW \n", i);
            button_states[i] = 1;

            if (sel_button_index == i) {
              Serial.print("ADD POINT \n");
              digitalWrite(led_pins[sel_button_index], LOW);
              score++;
              sel_button_index = -1;
              digitalWrite(plus_pin, HIGH);
              delay(1);
              digitalWrite(plus_pin, LOW);
            } else {
              Serial.print("REMOVE POINT \n");
              score--;
            }
          }
        } else if (buttonState == HIGH && button_states[i] == 1) {
          button_states[i] = 0;
          Serial.printf("Pin: %d, HIGH \n", i);
        }
      }
    }
    
    delay(100); 
  }
}

void start_game() {
  Serial.println("STATUS: starting game...\n");
  // for (size_t i = 0; i < 3; i++)
  // {
  //   Serial.printf("%d\n", i);
  //   delay(1000);
  // }

  // Serial.print("GO!\n");
  update_game = true;
}

void idle() {
  Serial.println("STATUS: Starting Idle...\n");

  update_game = false;
  bool start = false;

  score = 0;
  reset_update = true;
  digitalWrite(reset_pin, LOW);
  delay(1);
  digitalWrite(reset_pin, HIGH);

  int led_status = LOW;
  do
  {
    int buttonState = digitalRead(button_pins[start_button_index]);
    digitalWrite(led_pins[start_button_index], HIGH);
    if (buttonState == LOW) {
      start = true;
    } else {
      //led_status = led_status == LOW ? HIGH : LOW;
      //digitalWrite(led_pins[start_button_index], led_status);
      //delay(500);
    }
  } while (!start);

  digitalWrite(led_pins[start_button_index], LOW);
  start_game();
}

void ShowResults() {
  digitalWrite(led_pins[sel_button_index], LOW);
  sel_button_index = -1;
  update_game = false;

  Serial.print("STATUS: Results");
  Serial.printf("Score: %d", score);
  delay(result_timer);
  idle();
}

void GameTimer(void *pvParameters) {
  Serial.print("ButtonUpdate running on core\n");
  Serial.println(xPortGetCoreID()); 

  for (;;)
  {
    if (update_game) {
      delay(game_timer);
      ShowResults();
      delay(100);
    } else {
      delay(100);
    }
    delay(1);
  }
}

void update_reset_pin(void *pvParameters) {
  for(;;) {
    if (!reset_update) {
      digitalWrite(reset_pin, HIGH);
    }
    delay(1);
  }
}

void create_game_tasks()
{
  xTaskCreatePinnedToCore(update_reset_pin, "update_reset_pin", 10000, NULL, 1, &TReset, 0);
  xTaskCreatePinnedToCore(SelectUpdate, "SelectUpdate", 10000, NULL, 1, &TSelectUpdate, 0);
  delay(200);
  xTaskCreatePinnedToCore(ButtonUpdate, "ButtonUpdate", 10000, NULL, 1, &TButtonUpdate, 0);
  delay(200);
  xTaskCreatePinnedToCore(GameTimer, "GameTimer", 10000, NULL, 1, &TGameTimer, 0);
}

void setup()
{
  Serial.begin(115200);
  delay(200);

  Serial.println("STATUS: Booting...\n");

  // Button setup
  button_length = 
  led_length = sizeof(led_pins) / sizeof(led_pins[0]);

  for (size_t i = 0; i < button_length; i++)
  {
    // Serial.printf("Pin: %d\n", button_pins[i]);
    pinMode(button_pins[i], INPUT_PULLUP);
  }

  for (size_t i = 0; i < led_length; i++)
  {
    // Serial.printf("Pin: %d\n", led_pins[i]);
    pinMode(led_pins[i], GPIO_MODE_OUTPUT);
  }

  pinMode(plus_pin, GPIO_MODE_OUTPUT);
  pinMode(reset_pin, GPIO_MODE_OUTPUT);

  Serial.println("STATUS: Button setup complete...\n");
  create_game_tasks();
  idle();
}

void loop()
{
  // put your main code here, to run repeatedly:
}