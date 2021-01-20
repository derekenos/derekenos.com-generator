<!--
  
// ******************************************************************
//  Function:   draw()
//  Return:     void
// ******************************************************************

  function draw() {    
    drawFunctionIdle = false;
    
    // clear canvas
    dCanvasContext.clearRect(0,0,dCanvas.width,dCanvas.height);      
    
    // draw axis
    if(drawAxis)
    {
      dCanvasContext.beginPath();
      dCanvasContext.moveTo(0, dCanvas.height/2)
      dCanvasContext.lineTo(dCanvas.width, dCanvas.height/2);
      dCanvasContext.moveTo(dCanvas.width/2, 0)
      dCanvasContext.lineTo(dCanvas.width/2, dCanvas.height);
      dCanvasContext.closePath();
      dCanvasContext.strokeStyle = 'rgb(64,128,255)';
      dCanvasContext.stroke();    
      dCanvasContext.strokeStyle = defaultStrokeStyle;
    }
    
    // draw nodes
    for(var i = 0; i < nodeArray.length; i++)
    {
      // calculate vectors
      for(var d = 0; d < nodeArray.length; d++)
      {
        nodeArray[i].distances[d] = getDistanceBetweenNodes(nodeArray[i], nodeArray[d]);
        nodeArray[i].charges[d] = getChargeBetweenNodes(nodeArray[i], nodeArray[d]);        
        nodeArray[i].angles[d] = getAngleOfInfluenceBetweenNodes(nodeArray[i], nodeArray[d]);
      }

      // sum calculated vectors
      sumVectors(nodeArray[i]);

    // move if node is not locked
    if(!nodeArray[i].locked)
    {
        // move stuff
        if(inMotion && (nodeArray[i].mobility == 'free'))
          moveOnVector(i);
    }
    
      // draw stuff            
      if(nodeArray[i].visibility == 'visible')
        nodeArray[i].draw();         
    }    

/* DEBUG - disable zoom
*/
    if(zoomFactor != nextZoomFactor)
      zoom();

    drawFunctionIdle = true;
    
    if(document.getElementById('animSpeed').value != intervalValue && document.getElementById('animSpeed') != document.activeElement)
    {
      intervalValue = parseInt(document.getElementById('animSpeed').value)
      clearInterval(hInterval);
      hInterval = setInterval('draw()', intervalValue);
    }

  }


// ******************************************************************
//  Function:   drawNode(Node this)
//  Return:     node
// ******************************************************************

  function drawNode() {
    if(this == null)
      alert('drawNode received null object!');
      
    if(drawLineToCenter)
    {
      // draw line to center
      dCanvasContext.beginPath();
      dCanvasContext.moveTo(this.x, this.y)
      dCanvasContext.lineTo(dCanvas.getAttribute('centerX'), dCanvas.getAttribute('centerY'));
      dCanvasContext.closePath();
      dCanvasContext.stroke();
    }

    dCanvasContext.beginPath();
    dCanvasContext.moveTo(this.x + Math.abs(this.mass),this.y)
    dCanvasContext.fillStyle = this.fillStyle;
    dCanvasContext.arc(this.x,this.y,Math.abs(this.mass),0,Math.PI*2,true);
    dCanvasContext.closePath();
    dCanvasContext.fill();
    dCanvasContext.stroke();    
    if(nodeLabelsActive)
    {
      // label node number
      dCanvasContext.fillStyle = 'rgb(255,255,255)';
      dCanvasContext.fillText(this.id, this.x, this.y - 2);
      dCanvasContext.fillStyle = defaultFillStyle;
    }
    // don't draw vector arrow when node is locked
    if(drawVectorArrows && !this.locked && (this.mobility == 'free'))
    {
      // draw an arrow indicating the resultant vector of node
      dCanvasContext.beginPath();
      dCanvasContext.moveTo(this.x,this.y)
      dCanvasContext.lineTo(this.x + (this.x - this.lastX)*vectorArrowMultiplier,this.y + (this.y - this.lastY)*vectorArrowMultiplier);
      dCanvasContext.closePath();
      dCanvasContext.strokeStyle = defaultVectorArrowStrokeStyle;
      dCanvasContext.stroke();        
      dCanvasContext.strokeStyle = defaultStrokeStyle;      
    }
    if(nodeDebugActive)
    {
      // label node mass, polarity and coord
      dCanvasContext.fillText('mass:' + this.mass + ' chrg:' + this.charge + ' pol:' + this.polarity + ' [x:' + parseInt(this.x) + ' y:' + parseInt(this.y) + ']', this.x + Math.abs(this.mass) + 8, this.y);
        

      // label distances, charges and angles
      for(var d = 0; d < this.distances.length; d++)
      {
        dCanvasContext.fillText('[' + d + '] dist: ' + this.distances[d].toString().substr(0,6) + '  chrg: ' + this.charges[d].toString().substr(0,6) + ' ang: ' + this.angles[d].toString().substr(0,6), this.x + Math.abs(this.mass) + 8, this.y + (d+1)*defaultFontSize);
      }
      
      // label summed vectors
      dCanvasContext.fillText('sumCharge: ' + this.summedCharge.toString().substr(0,6) + '  sumAngle: ' + this.summedAngle.toString().substr(0,6), this.x + Math.abs(this.mass) + 8, this.y + (nodeArray.length+1)*defaultFontSize);          
    }            
  }      



// ******************************************************************
//  Function:   drawTriangle(a,b,c)
//  Return:     void
// ******************************************************************

  function drawTriangle(ax,ay,bx,by,cx,cy,stroke) {
    dCanvasContext.beginPath();
    dCanvasContext.moveTo(ax,ay)
    dCanvasContext.lineTo(bx,by);
    dCanvasContext.lineTo(cx,cy);
    dCanvasContext.closePath();
    if(stroke != null)
      dCanvasContext.strokeStyle = stroke;      
    dCanvasContext.stroke();
    dCanvasContext.strokeStyle = defaultStrokeStyle;    
  }


// ******************************************************************
//  Function:   drawVectorMeasurementTriangles(a,b,c)
//  Return:     void
// ******************************************************************

  function drawVectorMeasurementTriangle(srcNode, destNode)
  {
    if((srcNode >= 0) && (srcNode < nodeArray.length) && (destNode >= 0) && (destNode < nodeArray.length))
    {
      // draw vector calulation triangle from srcNode to destNode
        drawTriangle(nodeArray[srcNode].x, nodeArray[srcNode].y, nodeArray[destNode].x, nodeArray[srcNode].y, nodeArray[destNode].x, nodeArray[destNode].y);
    }
  }


// ******************************************************************
//  Function:   drawVectorTriangle(int nodeNum)
//  Return:     void
// ******************************************************************

  function drawVectorTriangle(nodeNum)
  {
    var xLeg, yLeg, angle, quad, arrowPointX, arrowPointY;
    
    // circular node degree relationship
    // ()->       0 degress
    // () bottom  90 degress
    // <-()       180 degress
    // () top     270 degrees
    
    // check if angle is perpendicular to either axis
    if((nodeArray[nodeNum].summedAngle == 0) || (nodeArray[nodeNum].summedAngle % 90 == 0))
    {
    }    
    else // angle is not perpendicular to axis
    {
      // correct angle calulation based on quadrant relative to x-axis
      if(nodeArray[nodeNum].summedAngle < 90)
      {
        angle = nodeArray[nodeNum].summedAngle;
        quad = 1;
      }
      else if(nodeArray[nodeNum].summedAngle > 90 && nodeArray[nodeNum].summedAngle < 180)
      {
        angle = 180 - nodeArray[nodeNum].summedAngle;
        quad = 2;
      }
      else if(nodeArray[nodeNum].summedAngle > 180 && nodeArray[nodeNum].summedAngle < 270)
      {
        angle = nodeArray[nodeNum].summedAngle - 180;
        quad = 3;
      }
      else if(nodeArray[nodeNum].summedAngle > 270)
      {
        angle = 360 - nodeArray[nodeNum].summedAngle;      
        quad = 4;
      }

      // calulate y translation based on angle and scale charged as x
      
      // convert angle from degrees to radians
      angle = angle * (Math.PI / 180);
      
      // cosA = b/c
      // cosA * c = b
      xLeg = Math.cos(angle) * nodeArray[nodeNum].summedCharge * 120;
      // sinA = a/c
      // sinA * c = a      
      yLeg = Math.sin(angle) * nodeArray[nodeNum].summedCharge * 120;
            
      switch(quad)
      {
        case 1:
          arrowPointX = nodeArray[nodeNum].x + xLeg;
          arrowPointY = nodeArray[nodeNum].y + yLeg;          
        break;

        case 2:
          arrowPointX = nodeArray[nodeNum].x - xLeg;
          arrowPointY = nodeArray[nodeNum].y + yLeg;          
        break;

        case 3:
          arrowPointX = nodeArray[nodeNum].x - xLeg;
          arrowPointY = nodeArray[nodeNum].y - yLeg;          
        break;

        case 4:
          arrowPointX = nodeArray[nodeNum].x + xLeg;
          arrowPointY = nodeArray[nodeNum].y - yLeg;          
        break;        
      }      

    }

    drawTriangle(nodeArray[nodeNum].x,nodeArray[nodeNum].y, arrowPointX,nodeArray[nodeNum].y, arrowPointX,arrowPointY, 'rgb(255,220,100)');
  }
  

// ******************************************************************
//  Function:   zoom(void)
//  Return:     void
// ******************************************************************
  function zoom() {
    // shrink all masses and shift all x/ys
    for(var i = 0; i < nodeArray.length; i++)
    {
      var el = nodeArray[i];
      var divisor = (nextZoomFactor/10 >= 1)?(nextZoomFactor/10):1;
      el.mass = el.normalMass / divisor;
      el.x = el.normalX / divisor;
      el.y = el.normalY / divisor;
      el.lastX = el.normalX / divisor;
      el.lastY = el.normalY / divisor;
    }
    
    zoomFactor = nextZoomFactor;
  }
  
  
-->