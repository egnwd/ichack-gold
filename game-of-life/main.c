#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

static const int world_width  = 5;
static const int world_height = 5;

typedef bool World[world_width][world_height];

void show_world();

World world;

int main() {
  world[1][1] = true;
  show_world(world);
  return(0);
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
