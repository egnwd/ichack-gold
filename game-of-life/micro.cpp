nclude "MicroBit.h"
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

#define MOD(a,b) (((a) + (b)) % (b))

static const int world_width  = 5;
static const int world_height = 5;

typedef bool World[world_height][world_width];

void set_world(uint32_t val);
void show_world();
void update();

World world;
World next_world; // Used as a buffer for the synchronous update

MicroBit uBit;

int main()
{
    // Initialise the micro:bit runtime.
    uBit.init();
    uBit.display.setDisplayMode(DISPLAY_MODE_BLACK_AND_WHITE);
    
    set_world(7532594);
    show_world();

    int old_x = uBit.accelerometer.getX();
    int old_y = uBit.accelerometer.getY();
    int old_z = uBit.accelerometer.getZ();
    
    bool triggered = false;
    
    while(!triggered)
    {
        int x = uBit.accelerometer.getX();
        int y = uBit.accelerometer.getY();
        int z = uBit.accelerometer.getZ();
        
        triggered = (abs(x - old_x) > 100 || abs(y - old_y) > 100 || abs(y - old_y) > 100);
        
        old_x = x;
        old_y = y;
        old_z = z;        
        
        uBit.sleep(100);
    }

//    set_world(2012505);
//    set_world(17187395);
    
    while (true) {
        update();
        show_world();
        uBit.sleep(300);   
    }
}

void update() {
  for (int i=0; i < world_height; i++) {
    for (int j=0; j < world_width; j++) {
      int nbs = 0;
      // Add neightbours in a clockwise direction from Top-Left
      nbs += world[MOD((i-1), world_height)][MOD((j-1), world_width)]; // T-L
      nbs += world[MOD((i-1), world_height)][j];                       // T
      nbs += world[MOD((i-1), world_height)][MOD((j+1), world_width)]; // T-R
      nbs += world[i][MOD((j+1), world_width)];                        // R
      nbs += world[MOD((i+1), world_height)][MOD((j+1), world_width)]; // B-R
      nbs += world[MOD((i+1), world_height)][j];                       // B
      nbs += world[MOD((i+1), world_height)][MOD((j-1), world_width)]; // B-L
      nbs += world[i][MOD((j-1), world_width)];                        // L
      
      if (world[i][j]) {
        if (nbs == 2 || nbs == 3) {
          next_world[i][j] = true;
        } else {
          next_world[i][j] = false;
        }
      } else {
        next_world[i][j] = (nbs == 3);
      }
    }
  }

  // Update the world synchronously
  memcpy(world, next_world, sizeof(World));
}

void show_world() {
  for (int i=0; i < world_height; i++) {
    for (int j=0; j < world_width; j++) {
        uBit.display.image.setPixelValue(j,i,world[i][j]);
    }
  }
  printf("\n");
}

// Set the global world from its bit represenation
void set_world(uint32_t val) {
  uint32_t offset;
  for (int i=0; i < world_height; i++) {
    for (int j=0; j < world_width; j++) {
       offset = (world_height * i) + j;
       world[i][j] = (val & (1 << offset)) != 0;
    }
  }
}

