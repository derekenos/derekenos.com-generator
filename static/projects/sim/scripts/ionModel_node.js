<!--
  

// ******************************************************************
//  Function:   newNode(x,y,mass,visibility,mobility,fillStyle,pulsar)
//  Return:     node
// ******************************************************************

  function newNode(x,y,mass,charge,visibility,mobility,fillStyle,pulsar,fatty)
  {
    var node = {
      id: nodeCount++,
      x: x,
      y: y,
      lastX: x/((nextZoomFactor/10 >= 1)?(nextZoomFactor/10):1),
      lastY: y/((nextZoomFactor/10 >= 1)?(nextZoomFactor/10):1),
      mass: mass/((nextZoomFactor/10 >= 1)?(nextZoomFactor/10):1),
      normalX: x,
      normalY: y,
      normalMass: mass,
      normalCharge: Math.abs(charge),
      charge: Math.abs(charge)/((nextZoomFactor/10 >= 1)?(nextZoomFactor/10):1),
      polarity: (charge >= 0)?'+':'-',
      mobility: mobility,
      fillStyle: (fillStyle == 'default')?defaultPosFillStyle:fillStyle,
      visibility: visibility,
      distances: [],
      charges: [],
      angles: [],
      summedAngle: 0,
      summedCharge: 0,
      locked: false,
      pulsar: ((pulsar==true)?true:false),
      pulsarCycle: 0,
      fatty: ((fatty==true)?true:false),
      // draw functions defined in 'ionModel_draw,js'
      draw: drawNode,
      drawLineToCenter: drawLineToCenter
    }
    
    nodeArray.push(node);
  }


// ******************************************************************
//  Function:   removeNodeFromArray(int nodeNum)
//  Return:     void
// ******************************************************************

  function removeNodeFromArray(nodeNum)
  {
    // wait for draw to be idle
    while(!drawFunctionIdle){}

    if(nodeNum < nodeArray.length)
    {
      // remove the element
      nodeArray.splice(nodeNum, 1);
      nodeCount--;
      // update all node.id values based on new locations
      for(var i = 0; i < nodeArray.length; i++)
      {
        nodeArray[i].id = i;
        // reduces internal array sizes
        nodeArray[i].distances.pop();
        nodeArray[i].charges.pop();      
        nodeArray[i].angles.pop();      
      }
      disableSpawnThisCycle = true;
    }
  }
  
-->

