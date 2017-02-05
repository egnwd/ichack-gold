function Circle(x, y) {
  this.x = x;
  this.y = y;
  this.r = 1;
  this.t = 0;
  this.growing = true;

  this.grow = function() {
    if (this.growing) {
      this.r += 0.1;
    }
  }

  this.show = function(i) {
    r = 120 * noise(this.t, i) + 40 * noise(i, this.t);
    g = 150 + 50 * noise(this.t+0.2, i) + 50 * noise(i, this.t+1);
    b = 40 + 120 * noise(this.t+0.5, i) + 40 * noise(i, this.t+2);
    fill(color(r, g, b));
    noStroke();
    ellipse(this.x, this.y, this.r * 2, this.r * 2);
    this.t += 0.02;
  }

  this.edges = function() {
    return (this.x + this.r >= width || this.x - this.r <= 0 || this.y + this.r >= height || this.y - this.r <= 0)
  }
}
