<!--

// ******************************************************************
//  Define Global Variables
// ******************************************************************

  var nodeLabelsActive, nodeDebugActive, drawAxis, drawVectorArrows, drawLineToCenter;
  var inMotion;
  var activeNodes;
  var zoomFactor, nextZoomFactor;

  var hInterval, intervalValue;

  var dCanvas, dCanvasContext;

  var nodeArray;
  var nodeCount;
  var chargeMoveMultiplier, vectorArrowMultiplier;
  var defaultPosCharge, defaultNegCharge;
  var defaultPosMass, defaultNegMass;
  var drawFunctionIdle;
  var disableSpawnThisCycle;

  var defaultFillStyle;
  var defaultStrokeStyle;
  var defaultLineWidth;
  var defaultFontSize;
  var defaultPosFillStyle, defaultNegFillStyle;
  var lockedNodeFillStyle;
  var defaultVectorArrowStrokeStyle = 'rgb(255,128,0)';


// ******************************************************************
//  Function:   init(void)
//  Return:     void
// ******************************************************************

  function init()
  {
    // init environmental variables
    nodeLabelsActive = false;
    nodeDebugActive = false;
    drawVectorArrows = false;
    drawLineToCenter = false;
    drawAxis = false;
    inMotion = false;

    // init global defines
    chargeMoveMultiplier = 1;
    vectorArrowMultiplier = 1000;

    defaultFillStyle = 'rgb(64,64,64)';
    defaultStrokeStyle = 'rgb(64,64,64)';
    defaultLineWidth = '2';
    defaultPosFillStyle = 'rgb(128,0,255)';
    defaultNegFillStyle = 'rgb(255,0,200)'
    lockedNodeFillStyle = 'rgb(255,255,255)';

    // init global variables
    activeNodes = new Array();
    nodeArray = new Array();
    nodeCount = 0;
    defaultPosCharge = 400;
    defaultNegCharge = -400;
    defaultPosMass = 20;
    defaultNegMass = 20;

    intervalValue = 4;

    zoomFactor = 70;
    nextZoomFactor = 70;
    drawFunctionIdle = true;
    disableSpawnThisCycle = false;

    // attach mouse wheel handler
    var mousewheelevt=(/Firefox/i.test(navigator.userAgent))? "DOMMouseScroll" : "mousewheel" //FF doesn't recognize mousewheel as of FF3.x

/* Debug - disable zoom
*/
    if (document.attachEvent) //if IE (and Opera depending on user setting)
        document.attachEvent("on"+mousewheelevt, mouseWheelHandler)
    else if (document.addEventListener) //WC3 browsers
        document.addEventListener(mousewheelevt, mouseWheelHandler, false)

     // set mainCanvas left, top parameters for correct cursor position calculation
     document.getElementById('mainCanvas').style.left = '10px';
     document.getElementById('mainCanvas').style.top = '10px';

     // init canvas
    dCanvas=document.getElementById('mainCanvas');
    if(dCanvas.getContext)
    if(1)
    {
      // canvas element is supported so set properties
      dCanvasContext = dCanvas.getContext('2d');
      // set general drawing properties
      dCanvasContext.fillStyle = defaultFillStyle;
      dCanvasContext.strokeStyle = defaultStrokeStyle;
      dCanvasContext.lineWidth = defaultLineWidth;
      dCanvasContext.font = 'bold 8px Verdana';
      defaultFontSize = 8;
    }
    else
      alert('HTML5 "canvas" element not supported!');

    dCanvas.setAttribute('centerX', parseInt(dCanvas.width)/2);
    dCanvas.setAttribute('centerY', parseInt(dCanvas.height)/2);

    // spawn some ions
    var numInitialNodes = 100;
    var toggle = true;
    while (numInitialNodes) {
      toggle ^= true;
      newNode(
        parseInt(dCanvas.width) / (Math.random() * 10),
        parseInt(dCanvas.height) / (Math.random() * 10),
        defaultNegMass,
        toggle ? defaultNegCharge : defaultPosCharge,
        'visible',
        'free',
        toggle ? defaultNegFillStyle : defaultPosFillStyle,
      );
      numInitialNodes -= 1;
    }

    document.getElementById('showAxis').checked = drawAxis;
    document.getElementById('showLabels').checked = nodeLabelsActive;
    document.getElementById('showVectors').checked = drawVectorArrows;
    document.getElementById('showInfo').checked = nodeDebugActive;
    document.getElementById('showLineToCenter').checked = drawLineToCenter;

    document.getElementById('defaultPosCharge').value = defaultPosCharge;
    document.getElementById('defaultNegCharge').value = defaultNegCharge;
    document.getElementById('defaultPosMass').value = defaultPosMass;
    document.getElementById('defaultNegMass').value = defaultNegMass;
    document.getElementById('zoomVal').value = zoomFactor;
    document.getElementById('animSpeed').value = intervalValue;

    // call draw() once to set vector arrows
    inMotion = true;
    draw();


    // set interval to auto-align test node to center
    hInterval = setInterval('draw()', intervalValue);
  }


-->
