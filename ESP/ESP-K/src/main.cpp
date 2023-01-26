#include <Arduino.h>

// Tasks
TaskHandle_t TSelectUpdate, TButtonUpdate, TGameTimer, TReset;

// Button variables
int led_pins[] = {17, 4, 5, 6, 16, 7, 15};
int button_pins[] = {8, 18, 3, 9, 11, 46, 10};
int button_states[] = {0, 0, 0, 0, 0, 0, 0}; // 0 = not pressed, 1 = pressed
int led_length = sizeof(led_length) / sizeof(int);
int button_length = sizeof(button_pins) / sizeof(int);
int sel_button_index = -1;
int prev_sel_button = -1;

// Game variables
int game_timer = 30000;
int counter_time = 3;
int start_blink_time = 1000;
float select_timer = 1000;
bool update_game = false;
int start_button_index = 3;
int score = 0;
int result_timer = 10000;
bool is_idle = false;

// ESP_L
bool reset_update = false;
int plus_pin = 1;
int reset_pin = 42;

/// @brief method which picks the next button that should be hit
/// @param pvParameters 
void select_update(void *pvParameters)
{
  Serial.print("SelectUpdate running on core\n");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    // Only update if the game has started
    if (update_game) {
      do
      {
        // Select a random led to turn on, try again if it repeats the same leds
        sel_button_index = random(0, led_length + 1);
      } while (prev_sel_button == sel_button_index);
      prev_sel_button = sel_button_index;

      // Enable the led
      Serial.printf("Pin: %d\n", sel_button_index);
      digitalWrite(led_pins[sel_button_index], HIGH);

      // Disable the led after x seconds
      delay(select_timer);
      digitalWrite(led_pins[sel_button_index], LOW);
    }

    delay(200);
  }
}

/// @brief Method which updates the states of the buttons
/// @param pvParameters 
void button_update(void *pvParameters)
{
  Serial.print("ButtonUpdate running on core\n");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    // Only update if the game has started
    if (update_game) {
      
      // Check the states of all the buttons
      for (size_t i = 0; i < button_length; i++)
      {
        int buttonState = digitalRead(button_pins[i]);

        // Check if the button is pressed
        if (buttonState == LOW) {
          if (button_states[i] == 0) {
            button_states[i] = 1;

            if (sel_button_index == i) {
              // Process the hit, disable led, increase points, reset buttonindex
              digitalWrite(led_pins[sel_button_index], LOW);
              score++;
              sel_button_index = -1;

              // Communicate to ESP-L that it has to increase the score
              digitalWrite(plus_pin, HIGH);
              delay(1);
              digitalWrite(plus_pin, LOW);
            } else {
              // Subtract a point from the score
              score--;
            }
          }
        } else if (buttonState == HIGH && button_states[i] == 1) {
          // Set the state of the button so we only fire the score functionality once
          button_states[i] = 0;
        }
      }
    }
    
    delay(100); 
  }
}

/// @brief Method which shows the results of the played session
void ShowResults() {
  digitalWrite(led_pins[sel_button_index], LOW);
  sel_button_index = -1;
  update_game = false;

  Serial.print("STATUS: Results");
  Serial.printf("Score: %d", score);
  delay(result_timer);
  idle();
}

/// @brief Task which handles the game progression
/// @param pvParameters 
void GameTimer(void *pvParameters) {
  Serial.print("ButtonUpdate running on core\n");
  Serial.println(xPortGetCoreID()); 
  for (;;)
  {
    // Only update if the game has started
    if (update_game) {
      
      // Wait until we complete this session
      delay(game_timer);
      ShowResults();
      delay(100);
    }
    delay(1);
  }
}

/// @brief Method which starts a counter
void start_counter(int time) {
  for (size_t i = 0; i < time; i++)
  {
    Serial.printf("%d\n", i);
    delay(1000);
  }

  Serial.print("GO!\n");
}

/// @brief Method whih starts the game after the counter has passed
void start_game() {
  Serial.println("STATUS: starting game...\n");

  // Start the counter before starting the game
  start_counter(counter_time);
  update_game = true;
}

/// @brief Method will handle if we need to start the game
void idle() {
  Serial.println("STATUS: Starting Idle...\n");

  // Reset the game values
  update_game = false;
  reset_update = true;
  score = 0;

  // Send a Signal to the ESP-L to restart the program
  digitalWrite(reset_pin, LOW);
  delay(1);
  digitalWrite(reset_pin, HIGH);

  // Set the values of the start button
  int led_status = HIGH;
  int toggle_time = start_blink_time;
  digitalWrite(led_pins[start_button_index], led_status);
  bool start = false;
  
  while (true) {
    // Check if the user pressed the start button so we can start the game
    int buttonState = digitalRead(button_pins[start_button_index]);
    toggle_time--;
    if (buttonState == LOW) {
      // Break out of the whileloop
      start = true;
      break;
    } else if (toggle_time < 0) {
      // Check if we should toggle the led
      toggle_time = start_blink_time;
      led_status = led_status == LOW ? HIGH : LOW;
      digitalWrite(led_pins[start_button_index], led_status);
    }
  }

  // Disable the start led if needed
  if (led_status == HIGH) {
    digitalWrite(led_pins[start_button_index], LOW);
  }

  // Start the game
  start_game();
}

/// @brief Method which handles if the ESP-L should be restarted
/// @param pvParameters 
void update_reset_pin(void *pvParameters) {
  for(;;) {

    // Always signal the reset pin to be active unless we have to reset.
    if (!reset_update) {
      digitalWrite(reset_pin, HIGH);
    }
    delay(1);
  }
}

/// @brief Method which creates the tasks for the game
void create_game_tasks()
{
  xTaskCreatePinnedToCore(update_reset_pin, "update_reset_pin", 10000, NULL, 1, &TReset, 0);
  xTaskCreatePinnedToCore(select_update, "SelectUpdate", 10000, NULL, 1, &TSelectUpdate, 0);
  xTaskCreatePinnedToCore(button_update, "ButtonUpdate", 10000, NULL, 1, &TButtonUpdate, 0);
  xTaskCreatePinnedToCore(GameTimer, "GameTimer", 10000, NULL, 1, &TGameTimer, 0);
}

/// @brief Method which handles the boot process of the game.
void setup()
{
  Serial.begin(115200);
  delay(200);
  Serial.println("STATUS: Booting...\n");

  // Button and Led setup
  for (size_t i = 0; i < button_length; i++)
  {
    pinMode(button_pins[i], INPUT_PULLUP);
  }
  for (size_t i = 0; i < led_length; i++)
  {
    pinMode(led_pins[i], GPIO_MODE_OUTPUT);
  }

  // ESP-L pin setup
  pinMode(plus_pin, GPIO_MODE_OUTPUT);
  pinMode(reset_pin, GPIO_MODE_OUTPUT);

  create_game_tasks();
  Serial.println("STATUS: Initialize complete...\n");
  idle();
}

void loop() { }