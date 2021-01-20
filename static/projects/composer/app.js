'use_strict';
//import Audio from './audio.js';

function getUrlNodes () {
  const params = new URLSearchParams(window.location.search);
  let nodes = [];
  for (let pair of params.getAll('node[]')) {
    nodes.push(pair.split(',').map(s => parseInt(s)));
  }
  return nodes;
}


function init () {
  const audio = new Audio();
  const visual = new Visual(getUrlNodes());

  visual.addTouchHandler((x, y) => {
    audio.play(visual.canvas.height - y, 'triangle',  0.5);
  });

  visual.addTouchHandler((x, y, retrigger) => {
    if (retrigger) return;
    const pathname = window.location.pathname;
    const search = window.location.search;
    const c = search.length ? '&' : '?';
    window.history.replaceState(
      {}, 'Title', pathname + search + `${c}node[]=${x},${y}`);
  });

  // Register reset handler.
  $(document).keypress(e => {
    if (e.key === 'r') {
      window.location = window.location.pathname;
    }
  });
}

$(document).ready(init);
