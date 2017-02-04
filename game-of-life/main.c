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

void show_world();
void update();
uint32_t get_world();
void set_world(uint32_t val);

World world;
World next_world; // Used as a buffer for the synchronous update

int main() {
//  world[4][1] = true;
//  world[3][1] = true;
//  world[2][1] = true;

  set_world(33035232);
  show_world(world);

//  for (int i = 0; i < 10; i++) {
//    update();
//    show_world(world);
//    printf("%d\n", get_world());
//  }

 return(0);
}

void find_fixed_points() {
  int n_states = pow(2, (5*5));
  uint32_t *states = (uint32_t*) malloc(sizeof(uint32_t)*n_states);
  for (uint32_t i=0; i < n_states; i++) {
    set_world(i);
    update();
    states[i] = get_world();
    if (i == get_world()) {
      printf("Fixed point found! : %d\n", get_world());
      show_world(world);
    }
  }

  free(states);
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

// An integer bit representation of a world (25 bits required)
uint32_t get_world() {
  uint32_t val = 0;
  uint32_t offset;
  for (int i=0; i < world_height; i++) {
    for (int j=0; j < world_width; j++) {
       offset = (world_height * i) + j;
       val |= world[i][j] << offset;
    }
  }
  return val;
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

void show_world() {
  printf("\n");
  for (int i=0; i < world_height; i++) {
    for (int j=0; j < world_width; j++) {
      printf("%s", world[i][j] ? "*" : "-");
      if (j == world_width - 1) {
        printf("\n");
      }
    }
  }
  printf("\n");
}
