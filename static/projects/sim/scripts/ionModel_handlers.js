<!--

// ******************************************************************
//  Function:   buttonHandler(obj el)
//  Return:     void
// ******************************************************************

  function buttonHandler(el) {
    switch(el.id)
    {
      case 'goPause':
        if(!inMotion)
        {
          inMotion = true;
          el.innerHTML = 'pause';
        }
        else
        {
          inMotion = false;
          el.innerHTML = 'go';
        }
      break;
            
      case 'reset':
        window.location.reload();
      break;
      
      case 'showAxis':
        drawAxis = el.checked;
      break;
      case 'showLabels':
        nodeLabelsActive = el.checked;
      break;
      case 'showVectors':
        drawVectorArrows = el.checked;
      break;
      case 'showInfo':
        nodeDebugActive = el.checked;
      break;
      case 'showLineToCenter':
      drawLineToCenter = el.checked;
      break;
      
      default:
      break;      
    }      
  }
  

// ******************************************************************
//  Function:   canvasMouseMoveHandler(event e)
//  Return:     void
// ******************************************************************
  function canvasMouseMoveHandler(e) {
     // check for any locked nodes and set x/y to mousex/y when first is found
    for(var i = 0; i < nodeArray.length; i++)
    {
      if(nodeArray[i].locked)
      {
        nodeArray[i].lastX = nodeArray[i].x;
        nodeArray[i].lastY = nodeArray[i].y;    
        nodeArray[i].x = e.pageX - parseInt(document.getElementById('mainCanvas').style.left);
        nodeArray[i].y = e.pageY - parseInt(document.getElementById('mainCanvas').style.top);
      }
    }
  }
  
  
// ******************************************************************
//  Function:   canvasMouseDownHandler(event e)
//  Return:     void
// ******************************************************************

  function canvasMouseDownHandler(e) {    
    // grab ion if click occurs within path
    var mouseX = e.pageX - parseInt(document.getElementById('mainCanvas').style.left);
    var mouseY = e.pageY - parseInt(document.getElementById('mainCanvas').style.top);
    var nodeId;
    
    // wait for draw to be idle so that position is known
    while(!drawFunctionIdle){}
    
    // check if cursor position lay inside defined ion body
    if((nodeId = isPointInNode(mouseX,mouseY)) >= 0)
    {
      // mouse was clicked inside node so lock it for manual dragging
      nodeArray[nodeId].locked = true;
      nodeArray[nodeId].fillStyle = lockedNodeFillStyle;
    }
  }


// ******************************************************************
//  Function:   canvasClickHandler(event e)
//  Return:     void
// ******************************************************************

  function canvasClickHandler(e)
  {    
    var mouseX = e.pageX - parseInt(document.getElementById('mainCanvas').style.left);
    var mouseY = e.pageY - parseInt(document.getElementById('mainCanvas').style.top);
    var anyLocked = false;
    
    // if there are any locked nodes, release them and skip spawn
    for(var i = 0; i < nodeArray.length; i++)
    {
      if(nodeArray[i].locked)
      {
        anyLocked = true;
        nodeArray[i].locked = false;
        nodeArray[i].fillStyle = (nodeArray[i].polarity == '+')?defaultPosFillStyle:defaultNegFillStyle;
      }
    }
              
    if(!anyLocked && !disableSpawnThisCycle) // disableSpawnThisCycle set by delete function
    {
      // read charges from text boxes
      defaultPosCharge = parseInt(document.getElementById('defaultPosCharge').value);
      defaultNegCharge = parseInt(document.getElementById('defaultNegCharge').value);    
      // read masses from text boxes
      defaultPosMass = parseInt(document.getElementById('defaultPosMass').value);
      defaultNegMass = parseInt(document.getElementById('defaultNegMass').value);    
      var pulsar = document.getElementById('addPulsar').checked;
      var fatty = document.getElementById('addFatty').checked;
          
      if(document.getElementById('addBlue').checked && document.getElementById('addFree').checked)
        newNode(mouseX,mouseY,defaultPosMass,defaultPosCharge,'visible','free','default',pulsar,fatty);
      else if(document.getElementById('addBlue').checked && document.getElementById('addAnchored').checked)
        newNode(mouseX,mouseY,defaultPosMass,defaultPosCharge,'visible','anchored','default',pulsar,fatty);
      else if(document.getElementById('addPink').checked && document.getElementById('addFree').checked)
        newNode(mouseX,mouseY,defaultNegMass,defaultNegCharge,'visible','free',defaultNegFillStyle,pulsar,fatty);
      else if(document.getElementById('addPink').checked && document.getElementById('addAnchored').checked)
        newNode(mouseX,mouseY,defaultNegMass,defaultNegCharge,'visible','anchored',defaultNegFillStyle,pulsar,fatty);
  
      if(!inMotion)
      {
        // call draw() once to set vector arrows
        inMotion = true;
        draw();
        inMotion = false;
      }
    }
    else if(disableSpawnThisCycle)
      disableSpawnThisCycle = false;
  }


// ******************************************************************
//  Function:   mouseWheelHandler(event e)
//  Return:     void
// ******************************************************************

  function mouseWheelHandler(e) {
    var evt=window.event || e //equalize event object
    var delta=evt.detail? evt.detail*(-120) : evt.wheelDelta //check for detail first so Opera uses that instead of wheelDelta
    nextZoomFactor = zoomFactor + parseInt(delta/3);
    if(nextZoomFactor < 1)
      nextZoomFactor = 1;
    else if(nextZoomFactor > 100)
      nextZoomFactor = 100;

    document.getElementById('zoomVal').value = parseInt(nextZoomFactor);
  }


// ******************************************************************
//  Function:   globalKeyPressHandler(event e)
//  Return:     void
// ******************************************************************

  function globalKeyPressHandler(e) {
    var keynum = e.which
    var lockedNodeId = -1;
    
    // get id of first locked node
    for(var i = 0; i < nodeArray.length; i++)
    {
      if(nodeArray[i].locked)
      {
        lockedNodeId = i;
        break;
      }
    }
    
    if(lockedNodeId != -1)
    {
      switch(keynum)
      {
        case 68: // 'd'
          // delete locked node from array
          removeNodeFromArray(lockedNodeId);
        break;
        case 65: // 'a'
          // toggle mobility
          nodeArray[lockedNodeId].mobility = (nodeArray[lockedNodeId].mobility == 'free')?'anchored':'free';
        break;
        case 80: // 'p'
          // toggle pulsar mode
          nodeArray[lockedNodeId].pulsar = !nodeArray[lockedNodeId].pulsar;
          if(!nodeArray[lockedNodeId].pulsar)
            nodeArray[lockedNodeId].charge = nodeArray[lockedNodeId].normalCharge;
        break;
        case 70: // 'f'
          // toggle between normal/fatty
          nodeArray[lockedNodeId].fatty = !nodeArray[lockedNodeId].fatty;
        break;
      }
    }
    else // lockedNodeId == -1
    {
      switch(keynum)
      {
        case 65: // 'a'
          // toggle new ion mobility
          var x = document.getElementById('addAnchored').checked;
          document.getElementById('addAnchored').checked = document.getElementById('addFree').checked;
          document.getElementById('addFree').checked = x;
        break;
        case 80: // 'p'
          // toggle new ion pulsar mode
          var x = document.getElementById('addStatic').checked;
          document.getElementById('addStatic').checked = document.getElementById('addPulsar').checked;
          document.getElementById('addPulsar').checked = x;
        break;
        case 88: // 'x'
          // toggle between blue/pink
          var x = document.getElementById('addBlue').checked;
          document.getElementById('addBlue').checked = document.getElementById('addPink').checked;
          document.getElementById('addPink').checked = x;
        break;
        case 70: // 'f'
          // toggle between blue/pink
          var x = document.getElementById('addNormal').checked;
          document.getElementById('addNormal').checked = document.getElementById('addFatty').checked;
          document.getElementById('addFatty').checked = x;
        break;
      }
    }    
  }    
   
   
   
   
   
   
-->