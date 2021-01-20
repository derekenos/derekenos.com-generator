<!--
  
// ******************************************************************
//  Function:   getDistanceBetweenNodes(obj nodeA, obj nodeB)
//  Return:     float
// ******************************************************************

  function getDistanceBetweenNodes(nodeA, nodeB)
  {
    // formula for distance between two cartesian graph points
    // d = sqrt((x2-x1)E2 + (y2 - y1)E2)
        
    var retVal;
    
    // distance between different nodes must not == 0 or bad things will happen during charge/vector calcs
    if(((retVal = Math.sqrt(Math.pow((nodeA.x - nodeB.x), 2) + Math.pow((nodeA.y - nodeB.y), 2))) == 0) && (nodeA.id != nodeB.id))
      return 1;
    else
      return retVal;
  }

// ******************************************************************
//  Function:   getChargeBetweenNodes(obj nodeA, obj nodeB)
//  Return:     float
// ******************************************************************

  function getChargeBetweenNodes(nodeA, nodeB)
  {
    // return charge of 0 if passed nodes are identical
    if(nodeA.id == nodeB.id)
    {
      // since this event will happen once ever draw cycle, also take this opportunity to process pulsar charge state
      if(nodeA.pulsar && !nodeA.locked && inMotion)
      {
        if(nodeA.pulsarCycle == 0) // pulsar charge is decreasing
        {
          nodeA.charge -= parseInt(nodeA.normalCharge/10); 
          if(nodeA.fatty)
            nodeA.mass -= ((nodeA.mass - nodeA.normalMass/10) >= 1)?nodeA.normalMass/10:0;
          else
            nodeA.mass = nodeA.normalMass;
          
          if(nodeA.charge <= 1)
          {
            nodeA.charge = 1;
            // charge has reached 0, switch cycle to increase
            nodeA.pulsarCycle = 1;          
          }
        }
        else // pulsar charge is increasing
        {
          nodeA.charge += parseInt(nodeA.normalCharge/10);
          if(nodeA.fatty)
            nodeA.mass += ((nodeA.mass + nodeA.normalMass/10) <= nodeA.normalMass)?nodeA.normalMass/10:0;
          else
            nodeA.mass = nodeA.normalMass;

          if(nodeA.charge >= nodeA.normalCharge)
          {
            nodeA.charge = nodeA.normalCharge;
            nodeA.pulsarCycle = 0;          
          }
        }
        var colorValue;
        if(nodeA.polarity == '+')        
        {
          colorValue = (parseInt(255 - (nodeA.charge / nodeA.normalCharge) * 255)).toString(10);
        }
        else
        {
          colorValue = (parseInt(255 - (nodeA.charge / nodeA.normalCharge) * 255)).toString(10);
        }

//        nodeA.fillStyle = nodeA.fillStyle.substr(0,(nodeA.fillStyle.lastIndexOf(',') + 1)) + colorValue + ')';
        nodeA.fillStyle = 'rgb(' + colorValue + ',' + colorValue + ',' + colorValue + ')';
      }      
      return 0;
    }      
      
    // if charges have opposite polarities then simply add charges.  opposite polarities attract
    // if charges have same polarity then add charges and negate.  same polarities repel
    var charge = (nodeA.charge * 1/nodeA.distances[nodeB.id]) + (nodeB.charge * 1/nodeA.distances[nodeB.id]);

    if(charge == 'Infinity')
    alert('charge == infinity!');

    if(nodeA.polarity == nodeB.polarity)
    charge = -charge;

    // if charge will cause overlap then equalize to just contact
    if(charge > (nodeA.distances[nodeB.id] - (nodeA.mass + nodeB.mass)))
      charge = (nodeA.distances[nodeB.id] - (nodeA.mass + nodeB.mass));

    return charge
  }


// ******************************************************************
//  Function:   getAngleOfInfluenceBetweenNodes(obj nodeA, obj nodeB)
//  Return:     float
// ******************************************************************

  function getAngleOfInfluenceBetweenNodes(nodeA, nodeB)
  {
    var xLeg, yLeg, angle;
    
    // circular node degree relationship
    // ()->       0 degress
    // () bottom  90 degress
    // <-()       180 degress
    // () top     270 degrees
    
    // return error if passed nodes are identical or if they share the same coordinates
    if((nodeA.x == nodeB.x) && (nodeA.y == nodeB.y))
      return 0

    // nodes are different and do not share same coordinates
    
    // check if nodes share either axis
    if(nodeA.x == nodeB.x)
    {
      // nodes have same x axis value
      // returned angle is relative to nodeA so..
      if(nodeA.y < nodeB.y)
        return 90;
      else
        return 270;
    }
    else if(nodeA.y == nodeB.y)
    {
      // nodes have same y axis value
      // returned angle is relative to nodeA so..
      if(nodeA.x < nodeB.x)
        return 0;
      else
        return 180;
    }
    else // nodes do not share either axis
    {
      // calculate length of right triangle legs
      // difference in x is always going be adjacent leg so that value is relative to axis
      xLeg = Math.abs(nodeA.x - nodeB.x);
      yLeg = Math.abs(nodeA.y - nodeB.y);
      // given distance, calculate angle from nodeA
      // cosA = (bE2 + cE2 - aE2) / 2bc, where b & c are adjcent legs from the angle 'A' you want to find
      angle = (Math.acos((Math.pow(xLeg, 2) + Math.pow(nodeA.distances[nodeB.id], 2) - Math.pow(yLeg, 2)) / (2 * xLeg * nodeA.distances[nodeB.id]))) * 360 / (Math.PI * 2);

      // correct angle calulation based on positional relationship between nodes
      if(nodeA.x < nodeB.x && nodeA.y < nodeB.y)
        angle = de_quadrantize360(angle, 1);
      else if(nodeA.x > nodeB.x && nodeA.y < nodeB.y)
        angle = de_quadrantize360(angle, 2);
      else if(nodeA.x > nodeB.x && nodeA.y > nodeB.y)
        angle = de_quadrantize360(angle, 3);
      else if(nodeA.x < nodeB.x && nodeA.y > nodeB.y)
        angle = de_quadrantize360(angle, 4);
    }

    return angle;    
  }


// ******************************************************************
//  Function:   sumVectors(obj nodeA)
//  Return:     void
// ******************************************************************

  function sumVectors(nodeA)
  {

    var xComponents = 0;
    var yComponents = 0;
    var angle, quad;
    
    if(nodeArray.length > 2)
    {
      // step through the node array summing vector components for nodeA
      for(var i = 0; i < nodeArray.length; i++)
      {
        // get quadrant and normalized angle
        quad = getQuadrant(nodeA.angles[i]);
        angle = quadrantize360(nodeA.angles[i]);
        
        // do not calculate for self
        if(i != nodeA.id)
        {
          if(nodeA.charges[i] < 0)
          {
            // charge is negative so invert angle by inverting quad
            if((quad += 2) > 4)
              quad -= 4;
          }

          // make sure to convert degrees to radians for calculation
          if(quad == 1 || quad == 4)
            xComponents += (Math.abs(nodeA.charges[i]) * Math.cos(angle * (Math.PI / 180)));
          else
            xComponents -= (Math.abs(nodeA.charges[i]) * Math.cos(angle * (Math.PI / 180)));
          if(quad == 1 || quad == 2)
            yComponents += (Math.abs(nodeA.charges[i]) * Math.sin(angle * (Math.PI / 180)));
          else
            yComponents -= (Math.abs(nodeA.charges[i]) * Math.sin(angle * (Math.PI / 180)));
        }
      }
  
      // set quad based on component results
      if(xComponents >= 0 && yComponents >= 0)
        quad = 1;
      else if(xComponents < 0 && yComponents >= 0)
        quad = 2;
      else if(xComponents < 0 && yComponents < 0)
        quad = 3;
      else if(xComponents >= 0 && yComponents < 0)
        quad = 4;
      
      // math here: http://hyperphysics.phy-astr.gsu.edu/hbase/vect.html
  
/*
      // debug - throw exception if nodeA.angles[] contains power of 90
      for(var o = 0; o < nodeA.angles.length; o++){if(nodeA.id!=o && nodeA.angles[o] % 90 == 0){throw('node['+nodeA.id+'].angles['+o+'] contains power of 90 angle');}}
*/

      // calculate summed charge
      nodeA.summedCharge = Math.sqrt(Math.pow(xComponents, 2) + Math.pow(yComponents, 2));
      
      // calculate summed angle and convert from radians to degrees
      nodeA.summedAngle = Math.abs(Math.atan(yComponents / xComponents) * 360 / (Math.PI * 2));
  
      nodeA.summedAngle = de_quadrantize360(nodeA.summedAngle, quad);
      
    }
    else // nodeArray.length <= 2 so skip calculating
    {
      for(var i = 0; i < nodeArray.length; i++)
      {
        // skip self
        if(i != nodeA.id)
        {
          nodeA.summedAngle = nodeA.angles[i];
          nodeA.summedCharge = nodeA.charges[i];
        }
      }      
    }       
  }


// ******************************************************************
//  Function:   moveOnVector(int nodeNum)
//  Return:     void
// ******************************************************************

  function moveOnVector(nodeNum)
  {
    var xLeg, yLeg, angle, quad, nextX, nextY;
    
    // circular node degree relationship
    // ()->       0 degress
    // () bottom  90 degress
    // <-()       180 degress
    // () top     270 degrees
    
    // check if angle is perpendicular to either axis
    if((nodeArray[nodeNum].summedAngle == 0) || (nodeArray[nodeNum].summedAngle % 90 == 0))
    {
      switch(nodeArray[nodeNum].summedAngle)
      {
        case 0:
          nextX = nodeArray[nodeNum].x + nodeArray[nodeNum].summedCharge * chargeMoveMultiplier;
          nextY = nodeArray[nodeNum].y;
        break;
        case 90:
          nextX = nodeArray[nodeNum].x;
          nextY = nodeArray[nodeNum].y + nodeArray[nodeNum].summedCharge * chargeMoveMultiplier;
        break;
        case 180:
          nextX = nodeArray[nodeNum].x - nodeArray[nodeNum].summedCharge * chargeMoveMultiplier;
          nextY = nodeArray[nodeNum].y;
        break;
        case 270:
          nextX = nodeArray[nodeNum].x;
          nextY = nodeArray[nodeNum].y - nodeArray[nodeNum].summedCharge * chargeMoveMultiplier;
        break;
      }        
    }    
    else // angle is not perpendicular to axis
    {
      // correct angle calulation based on quadrant relative to x-axis
      angle = quadrantize360(nodeArray[nodeNum].summedAngle);
      
      // convert angle from degrees to radians
      angle = angle * (Math.PI / 180);
      
      // cosA = b/c
      // cosA * c = b
      xLeg = Math.cos(angle) * nodeArray[nodeNum].summedCharge * chargeMoveMultiplier;
      // sinA = a/c
      // sinA * c = a      
      yLeg = Math.sin(angle) * nodeArray[nodeNum].summedCharge * chargeMoveMultiplier;
     
      switch(getQuadrant(nodeArray[nodeNum].summedAngle))
      {
        case 1:
          nextX = nodeArray[nodeNum].x + xLeg;
          nextY = nodeArray[nodeNum].y + yLeg;          
        break;

        case 2:
          nextX = nodeArray[nodeNum].x - xLeg;
          nextY = nodeArray[nodeNum].y + yLeg;          
        break;

        case 3:
          nextX = nodeArray[nodeNum].x - xLeg;
          nextY = nodeArray[nodeNum].y - yLeg;          
        break;

        case 4:
          nextX = nodeArray[nodeNum].x + xLeg;
          nextY = nodeArray[nodeNum].y - yLeg;          
        break;        
      }      
    }

/* Debug - still crashes, yay!
    if(nextX == null || nextX == NaN || nextX == undefined || nextY == null || nextY == NaN || nextY == undefined)
      throw('oh nos');
*/    
    nodeArray[nodeNum].lastX = nodeArray[nodeNum].x;
    nodeArray[nodeNum].lastY = nodeArray[nodeNum].y;    

    // enforce constrainToWindow if set
    if(document.getElementById('worldSizeWindow').checked == true)
    {
      if(nextX + nodeArray[nodeNum].mass > dCanvas.width)
        nextX = dCanvas.width - nodeArray[nodeNum].mass;
      else if(nextX - nodeArray[nodeNum].mass < 0)
        nextX = nodeArray[nodeNum].mass;
        
      if(nextY + nodeArray[nodeNum].mass > dCanvas.height)
        nextY = dCanvas.height - nodeArray[nodeNum].mass;
      else if(nextY - nodeArray[nodeNum].mass < 0)
        nextY = nodeArray[nodeNum].mass;
    }
        
    nodeArray[nodeNum].x = nextX;
    nodeArray[nodeNum].y = nextY;
  }


// ******************************************************************
//  Function:   deCollide(void)
//  Return:     int
// ******************************************************************

  function deCollide()
  {
    // search for collisions and separate nodes if necessary
    for(var i = 0; i < nodeArray.length; i++)
    {
      for(var j = 0; j < nodeArray.length; j++)
      {
      }
    }
  }


// ******************************************************************
//  Function:   getQuadrant(int degrees)
//  Return:     int
// ******************************************************************

  function getQuadrant(degrees)
  {
    var degreesTmp = degrees;
    
    // ensure that degrees value is positive
    while(degreesTmp < 0)
      degreesTmp += 360;
          
    if(degreesTmp < 90)
    {
      return 1;
    }
    else if(degreesTmp >= 90 && degreesTmp < 180)
    {
      return 2;
    }
    else if(degreesTmp >= 180 && degreesTmp < 270)
    {
      return 3;
    }
    else if(degreesTmp >= 270)
    {
      return 4;
    }
  }
  
// ******************************************************************
//  Function:   quadrantize360(int degrees)
//  Return:     int
// ******************************************************************

  function quadrantize360(degrees)
  {
    var degreesTmp = degrees;
    
    // ensure that degrees value is positive
    while(degreesTmp < 0)
      degreesTmp += 360;
          
    switch(getQuadrant(degreesTmp))
    {
      case 1:
        return degreesTmp;
      break;
      case 2:
        return 180 - degreesTmp;
      break;
      case 3:
        return degreesTmp - 180;
      break;
      case 4:
        return 360 - degreesTmp;
      break;
    }    
  }

// ******************************************************************
//  Function:   de_quadrantize360(int degrees, int quad)
//  Return:     int
// ******************************************************************

  function de_quadrantize360(degrees, quad)
  {
    switch(quad)
    {
      case 1:
        return degrees;
      break;
      case 2:
        return 180 - degrees;
      break;
      case 3:
        return degrees + 180;
      break;
      case 4:
        return 360 - degrees;
      break;      
    }
  }


// ******************************************************************
//  Function:   isPointInNode(int x, int y)
//  Return:     int node.id
// ******************************************************************
// returns id of node that the coords are located within, or
// returns -1 if coords are not within any node shape path
  function isPointInNode(x,y)
  {
    for(var i = 0; i < nodeArray.length; i++)
    {
      // create shape path for current node
      dCanvasContext.beginPath();
      dCanvasContext.moveTo(nodeArray[i].x + Math.abs(nodeArray[i].mass),nodeArray[i].y)
      dCanvasContext.arc(nodeArray[i].x,nodeArray[i].y,Math.abs(nodeArray[i].mass),0,Math.PI*2,true);      
      // check if point lay within path
      if(dCanvasContext.isPointInPath(x,y))
        // return first detected ion id
        return nodeArray[i].id;              
    }
    return -1;
  }

-->