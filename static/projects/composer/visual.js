'use strict';

//export default

class TouchIndicator {
  constructor (context, x, y, size) {
    this.context = context;
    this.x = x;
    this.y = y;
    this.size = size;
    this.alpha = 1;
    this.isActive = true;
    this.draw();
  }

  draw () {
    let ctx = this.context;
    ctx.save();
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size / 2, 0, 2 * Math.PI);
    ctx.globalAlpha = this.alpha;
    ctx.fill();
    ctx.restore();
    // For each 16mS frame, decrement alpha such that it will change from 1.0
    // to 0.0 in 2 seconds time.
    this.alpha -= 1 / (2 / .016);
    if (this.alpha <= 0)
      this.isActive = false;
  }
}


class XScanLine {
  constructor (context) {
    this.context = context;
    this.x = 0;
    this.lastX = 0;
    this.minX = 0;
    this.maxX = this.context.canvas.width;
    this.isActive = true;
    this.draw();
  }

  toggle () {
    this.minX = 0;
    this.maxX = this.context.canvas.width;
    this.lastX = this.x = 0;
    this.isActive ^= true;
  }

  setCurrentAsMin () {
    this.minX = this.x;
  }

  setCurrentAsMax (x) {
    this.maxX = this.x;
  }

  draw () {
    let ctx = this.context;
    ctx.save();
    ctx.fillStyle = '#ccc';
    ctx.fillRect(this.x, 0, 8, ctx.canvas.height);
    ctx.restore();
    this.lastX = this.x;

    if (this.isActive) {
      this.x += 8;
      if (this.x < this.minX) {
        this.x = this.minX;
      }
      else if (this.x >= this.maxX) {
        this.x = this.minX;
      }
    }
  }
}


class YScanLine {
  constructor (context) {
    this.context = context;
    this.y = 0;
    this.lastY = 0;
    this.isActive = false;
    this.draw();
  }

  toggle () {
    this.lastY = this.y = 0;
    this.isActive ^= true;
  }

  draw () {
    let ctx = this.context;
    ctx.save();
    ctx.fillStyle = '#ccc';
    ctx.fillRect(0, this.y, ctx.canvas.width, 8);
    ctx.restore();
    this.lastY = this.y;

    if (this.isActive) {
      this.y += 4;
      if (this.y >= ctx.canvas.height)
        this.y = 0;
    }
  }
}


class Visual {
  constructor (initialNodeCoordinates) {
    this.canvas = document.getElementById('canvas');
    this.$canvas = $(this.canvas);
    const $window = $(window);
    this.context = this.canvas.getContext('2d');
    this.canvas.width = window.innerWidth;
    // Using window.innerWidth instead of $window.innerWidth() because the
    // latter doesn't seem to work correctly in Firefox.
    this.canvas.height = window.innerHeight;

    this.touchIndicators = [];
    this.addTouchHandler((x, y) => this.touchIndicators.push(
      new TouchIndicator(this.context, x, y, (y / this.canvas.height) * 100)));

    this.xScanLine = new XScanLine(this.context);
    this.yScanLine = new YScanLine(this.context);

    // Register keypress handler.
    $(document).keypress(e => {
      switch (e.key) {
      case "x":
        this.xScanLine.toggle();
        break;
      case "z":
        this.xScanLine.setCurrentAsMin();
        break;
      case "c":
        this.xScanLine.setCurrentAsMax();
        break;
      case "y":
        this.yScanLine.toggle();
        break;
      }
    });

    for (let coord of initialNodeCoordinates) {
      this.triggerTouchHandler(...coord);
    }

    this.draw();
  }


  draw () {
    // Clear the canvas.
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Iterate through touch indicators, drawing and collecting those which are
    // still active.
    const indicators = this.touchIndicators.slice(0);
    this.touchIndicators = [];
    for (let indicator of indicators) {
      if (indicator.isActive) {
        indicator.draw();
        this.touchIndicators.push(indicator);
      }
      else if ((this.xScanLine.lastX <= indicator.x
                && indicator.x < this.xScanLine.x) ||
               (this.yScanLine.lastY <= indicator.y
                && indicator.y < this.yScanLine.y)) {
        this.triggerTouchHandler(indicator.x, indicator.y);
      } else {
        this.touchIndicators.push(indicator);
      }
    }

    // DEBUG
//    console.log(this.touchIndicators.length);
    $(document).keypress(e => {
      let _this = this;
      if (e.key === "d") {
        debugger;
      }
    });

    // Draw the scan line,
    this.xScanLine.draw();
    this.yScanLine.draw();

    // Schedule the next callback.
    window.requestAnimationFrame(this.draw.bind(this));
  }

  addTouchHandler (f) {
    this.$canvas.click(e => f(e.offsetX, e.offsetY, e.retrigger));
  }

  triggerTouchHandler (x, y) {
    this.$canvas.triggerHandler(
      $.Event('click', {
        offsetX: x,
        offsetY: y,
        retrigger: true
      })
    );
  }
}
