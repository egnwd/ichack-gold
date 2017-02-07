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
uint32_t find_root(uint32_t state);

World world;
World next_world; // Used as a buffer for the synchronous update

int main() {

  // Find the root for the 'O' state
  // printf("%d\n", find_root(11043370));

  set_world(7532594);
  show_world(world);

  for (int i = 0; i < 28; i++) {
    update();
    show_world(world);
    printf("%d\n", get_world());
  }

  return(0);
}

uint32_t find_root(uint32_t leaf) {
  
  if (leaf == 0) { return 0; }

  int n_states = pow(2, (5*5));
  uint32_t *states = (uint32_t*) malloc(sizeof(uint32_t)*n_states);
  uint32_t *trail = (uint32_t*) malloc(sizeof(uint32_t)*n_states);
  for (uint32_t i=0; i < n_states; i++) {
    set_world(i);
    update();
    states[i] = get_world();
  }

  int current = 0;
  int end = 1;
  trail[0] = leaf;
  states[leaf] = 0; // Remove the fixed point (bit hacky)

  printf("Calculated table\n");

  while (current != end) {
    for (uint32_t i=0; i < n_states; i++) {
      if (states[i] == trail[current]) {
        trail[end] = i;
        end++;
      }
    }
    current++;
    printf("Current: %d\nEnd: %d\n\n", current, end);
    if (current % 4096 == 0) {
      printf("VALUE: %d\n", trail[end-1]);
    }
  }
  
  uint32_t root = trail[end-1];
  free(states);
  free(trail);
  return root;
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
