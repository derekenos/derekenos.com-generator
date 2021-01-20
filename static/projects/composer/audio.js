'use strict';

//export default
class Audio {

  constructor () {
    const context = new window.AudioContext();
    this.context = context;

    // Create a compressor node and set it as the output node.
    const compressor = context.createDynamicsCompressor();
    compressor.threshold.setValueAtTime(-50, context.currentTime);
    compressor.knee.setValueAtTime(40, context.currentTime);
    compressor.ratio.setValueAtTime(12, context.currentTime);
    compressor.attack.setValueAtTime(0, context.currentTime);
    compressor.release.setValueAtTime(0.25, context.currentTime);
    compressor.connect(context.destination);
    this.output = compressor;

    this.oscillators = [];
  }

  play (frequency, type, initialGain) {
    const oscillator = new OscillatorNode(this.context, {
      'frequency': frequency,
      'type': type
    });

    const gainNode = new GainNode(this.context);
    gainNode.connect(this.output);
    oscillator.connect(gainNode);

    const now = this.context.currentTime;
    gainNode.gain
      .setValueAtTime(initialGain, now)
      .exponentialRampToValueAtTime(0.001, now + 2)
      .setValueAtTime(0, now + 2.1);

    oscillator.start();
    oscillator.stop(now + 2.1);


    this.oscillators.push(oscillator);
    return oscillator;
  }

}
