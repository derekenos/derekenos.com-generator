
from lib.htmlephant_extensions import Main
from lib.htmlephant import (
    H1,
    OGMeta,
    StdMeta,
    Title,
)

from includes import section
from includes import article_collection

INITIATIVES = (
    (
        'Teaching Arcade',
        """Arcade games are an exciting and well-loved manifestation of physical computing, but in constrast to peoples' burgeoning ability to author game software, creating new, exciting, and specific physical interfaces through which to interact with these games remains largely out of reach. This initiative would create a space to teach physical interface design, programming, and fabrication in conjunction with game software design and programming, with the end goal of creating a physical gaming appliance to be presented in an arcade gallery and/or duplicated for sale. Game design instruction will focus on leveraging modern web technologies (e.g. HTML5, Javascript, Web Components) and development practices (e.g. testing, version control) to maximize the potential of applying what is learned in a professional capacity. Hardware design instruction will focus on leveraging modern, inexpensive, commodity components and modular construction practices."""
    ),

    (
        'Local Manufacturing Cooperative',
        """Inspired by contemporary efforts such as <a href="https://www.opensourceecology.org/">Open Source Ecology</a> and <a href="http://preciousplastic.com/">Precious Plastic</a>, <a href="https://en.wikipedia.org/wiki/Worker_cooperative">worker cooperatives</a>, and the <a href="https://en.wikipedia.org/wiki/Putting-out_system#Cottage_industry">cottage industries</a> of yore, this initiative would create a platform for motivating, organizing, and empowering community members with the resources to establish a distributed manufacturing cooperative in which worker-owners employ automated assembly and digital fabrication tools in the service of producing sellable, made-to-order, customizable products and components. Products would be derived from existing, open-source designs and designed anew by local designers. Fabrication machines would be constructed from existing, open-source plans, e.g. <a href="https://github.com/fellesverkstedet/fabricatable-machines">fabricatable-machines</a>, <a href="https://www.maslowcnc.com/">Maslow CNC</a>, <a href="https://preciousplastic.com/solutions/machines/overview.html">Precious Plastic Machines</a>. Following the Precious Plastic model, plastic waste would be collected and transformed into both finished goods and stock for injection molding. Similarly, aluminum waste could be collected and formed into blocks for injection mold machining. Acknowledging the existence of things like makerspaces, <a href="https://www.fablabs.io/">Fab Labs</a>, <a href="https://100kgarages.com/">100k garages</a>, etc., this effort differs in that it aims to actively productize specific outputs of digital fabrication to the financial gain of its members. CNC furniture would be a reasonable, initial product category, e.g. <a href="http://atfab.co/">http://atfab.co/</a>"""
    ),

    (
        'Frontage',
        """An Airbnb-like platform to connect commercial property owners with small business owners, artists, and makers to facilitate co-habitation of retail spaces (a.k.a co-retail). Similar to Airbnb, the platform would provide a standard operating procedure for owners, process payments, facilitate communication, publish reviews, provide insurance, etc. The ultimate goals are: to enable individuals to pursue their dream of a brick-and-mortar presence without the daunting, and often prohibitive, financial burden of a single-occupancy retail lease, to provide communities with a greater variety of commercial offerings, and to provide property owners with increased revenue, decreased risk, and advanced digital tools to manage their operations."""
    ),
)

VARIATIONS = (
    (
        'Voice-changer Microphone Kit',
        """Design a kit that can be assembled into a hand-held voice-changer microphone (you talk into one end and the processed signal comes out the other) for which the user can create custom audio effects via a web-based interface. The hardware would comprise an enclosure, microphone, speaker, battery holder, buttons, audio amp, and something like an ESP32 for the interface, connectivity and audio processing. It could serve as a fun, gratifying introduction to digital signal processing. <a href="https://duckduckgo.com/?q=voice-changer+microphone&t=h_&iax=images&ia=images">Examples</a>"""
    ),

    (
        'Sound Book Kit',
        """Design a kit that can be assembled into a frame that has audio playback componentry along one side and the ability to affix book pages to the other, providing a means for the reader to create their own interactive experience through the creation of their own pages and audio samples. This could also serve as a platform for playback of stories as read by loved ones. <a href="https://duckduckgo.com/?q=kids+sound+book&t=h_&iar=images&iax=images&ia=images">Examples</a>"""
    )
)

REALIZED_BY_OTHERS = (
    (
        'Column Table',
        """Realized as <a href="http://tangible.media.mit.edu/project/inform/">inFORM</a>. I imagined using it as a game surface for maniuplating the position of a ball, almost exactly like they do <a href="https://vimeo.com/79179138#t=190s">in the video</a>. I also considered rounding the column heads and skinning the surface with a sheet of latex to create a more organic form. Prototyping this was beyond my capabilities at the time."""
    ),

    (
        'Teeny Turner',
        """Realized as <a href="https://github.com/scottbez1/smartknob">SmartKnob</a>. A chainable digital rotary encoder knob with integrated POV (or LCD if you're fancy) display and configurable haptics / physical limits that can be programmed to output a variety of control signals (e.g. SPI, I2C, analog voltage, MIDI, resistance, oscillations)."""
    )
)

SMALL_BITES = (
    (
        'Wave-based Audio Sequencer',
        """An audio sample sequencer that uses complex waveforms and oscilloscope-like triggering strategies to determine when samples will trigger. The waveform for each channel is generated by adjusting a set of ranged inputs that each control the contributed amplitude of a pure sine wave at a fixed (or variable) frequency. The waveform is displayed on a screen. One or more triggers can be configured for each waveform that determine when in the cycle the channel's sample will trigger. The triggers can be configured as delta or threshold, rising or falling, etc. This system would provide for a more organic, analog and less cold, digital, prescriptive sequencing experience."""
    ),
    (
        'Table at the End of the World',
        """A distributed network of standalone garden sheds, each large enough for a table that spans the width of the center and one or two diners on either side. The walls along which the table edges rest are projection screens. Cameras and microphones capture the local diners. Feeds from other sheds are projected onto the screens and played as ambient audio to create a co-dining experience in which participants are seated along a rectangular table that extends virtually into other sheds in both directions. Participants can arrange to sit alongside their friends or be randomly slotted in, <a href="https://youtu.be/Y70vcs3oV14?t=11">Matrix stockroom-style</a> (complete with fans to simulate the airflow).
        """
    ),

    (
        'Sugarcoater',
        """A radio, or standalone audio processing device, for listening to news and other talk programs that has a knob to adjust the tone of what is said. Listening to breakfast jazz with your kids when the news comes on talking about violent subway attacks and virus-related deaths? Turn the reality knob from "Hard, Cold" to "Nerf". See: <a href="#augmented-reality-microphone">Augmented Reality Microphone</a>
        """
    ),

    (
        'Augmented Reality Microphone',
        """A handheld battery-powered device with a microphone on one end and a speaker on the other, similar to a voice-changer mic, that uses an ML model of your voice to produce speech that is different in meaning and/or content from that which was spoken. Mode selection controls the manner of augmentation, e.g. replace words with [ant|syn]onyms, add uncomfortable pauses, interjections, superfluous phrase, etc."""
    ),

    (
        'Guitar Effects Platform',
        """Custom guitar effects pedal platform. Line 6 was doing something like this with their ToneCore DSP product, but it was expensive and prescriptive. The killer feature that I wanted to implement was the ability to clone an existing pedal through automated manipulation of its physical controls in conjunction with input signal generation and target output analysis. Recently, in 2020, there was this <a href="https://teddykoker.com/2020/05/deep-learning-for-guitar-effect-emulation/">Deep Learning for Guitar Effect Emulation</a>."""
    ),

    (
        'Linear Impact MIDI Controller',
        """Large linear sensor with segmented regions that can detect the precise location of a drum stick hit along its length.""",
    ),

    (
        'Voice-controlled Drum Sequencing',
        """Translate breatboxing into a real drum track. There are some recent entrants in this space (e.g. <a href="https://vochlea.com/">Dubler Studio Kit</a>, <a href="https://humbeatz.com/#/">HumBeatz</a>) with rigid and boring products."""
    ),

    (
        'ENDO',
        """View is of a meadow with a tree in the far distance and mountains in the background. With each kick drum hit, the camera moves forward toward the tree. Birds fly through the meadow and clouds move in the sky. It is alive. As you approach the tree, an animal standing under the tree becomes visible. It is a horse. It looks nervous as you approach. It’s mouth is slightly ajar. The kick drum hits move the camera toward the horse’s mouth. The horse looks very nervous. The camera enters the horse’s mouth and travels down the throat. Procedurally generated graphics simulate a journey through the horse’s digestive tract. It’s a multimedia extravaganza."""
    ),

    (
        'Real-time Configurable Touch Screen Button Overlay',
        """Similar to the <a href="https://monome.org/docs/grid/">Monome Grid</a> button matrix but with transparent plastic elements, no peripheral clearance, electronically-actuated internal mechanisms to join adjacent elements into larger groups, and an attached touch screen to serve as illumination and input mechanism."""
    ),

    (
        'Live Local Game Show',
        """Live local show that is basically an intergalactic-space-prison-themed (or other interesting theme) “The Price is Right” with up-for-bid items, sponsorship, and prizes provided by local vendors. Why are there no local game shows? Seems like such an obviously fun thing for folks to attend."""
    ),

    (
        'Sentimental Waveforms',
        """Instead of hanging a child's name of the wall, hang a reproduction of the audio waveform of their spoken name constructed from thread."""
    ),

    (
        'Traffic Wheel Sequencer',
        """Arrange melodies on concentric tracks."""
    ),

    (
        'IRL RC Car AR Game System',
        """Players drive RC cars on a road surface game field rendered using laser projectors. Cameras detect car position to register collisions and goal achievement. Lots of room for fun personalization of vehicles using digital fabrication. An exciting, physical, IRL, AR game experience! Good for culdesacs. Just typing this gets me super-excited about it again; I probably shouldn't publish it. $$$"""
    ),

    (
        'Remote Kids Bike Brake',
        """A handheld device that you can squeeze to apply the rear brake on your kid's bike."""
    ),

    (
        'Plant’s Thirsty',
        """A small, inexpensive, low-power electronic device that monitors a plant’s soil moisture level and plays a sound (e.g. periodic dry cough) when the plant needs water."""
    ),

    (
        'Micro-communities',
        """A digital platform for organizing local families into “pod”s for hyper-local resource pooling and sharing, e.g. batch cooking meals, tool sharing, child caring, etc."""
    ),

    (
        'Spectrographic Synth',
        """A sound synth that derives its sound from the spectrographic properties of vials of liquids. Recipes for creating certain sounds."""
    ),

    (
        'Swarm Care',
        """An all-electric, autonomous grass mowing service using open-source, modular designs."""
    ),

    (
        'Hue-man in the Mirror',
        """A projection-screen mirror with a camera in the middle that can capture a model of an onlooker's face and which displays a model to the onlooker of a previous capture. It would be really cool to be able to examine someone else's face as if it were your own."""
    ),

    (
        'Level Angler',
        """A device that clips onto a carpenter's level to announce the current degrees offset from some gravity-relative reference."""
    ),

    (
        'Chop Saw Feeder / Chopper',
        """A chop saw accessory that automatically feeds and cuts stock to predetermined lengths. Could also be paired with a doctored drill press to make quick work of things like this <a href="http://maslowcommunitygarden.org/Bolt-Together-Maslow-Frame.html">Bolt-Together Maslow Frame</a>."""
    ),

    (
        'Eyes for Podcasts',
        """Automatically generate visuals for audio-only media hosted on video platforms. Imagine a procedurally-generated Dr. Katz or Waking Life with the characters automatically generated and articulated based on the audio."""
    ),

    (
        'Garden Guard',
        """A watering turret w/ camera that sits above a garden and normally waters with a gentle shower but can switch to pulsed water jet mode to deter pests. Deters are captured on video, and optionally published, with exciting video/sound effects (e.g. water jet looks/sounds like laser beam)."""
    ),

    (
        'Make an Entrance',
        """Based on the trope of a person entering a room, accompanied by an enthralled audience, who delivers a final, out-of-context punchline. Stage is a series of themed rooms arranged in a circle with the protagonist and companions continuously making an entrance from one to the next, delivering ever-changing punchlines. Over time the performers become wary, the jokes become tedious and no longer funny. Maybe things eventually take a violent turn."""
    ),

    (
        'Agile Double Dragon',
        """Like Double Dragon but you fight scrum masters, etc."""
    ),

    (
        'Lead Landscape',
        """A large grid of unsharpened, upright pencils to which is attached an articulated robotic arm with pencil sharpener end effector. The arm sharpens pencils to generate a 3D landscape."""
    ),

    (
        'Wind Watcher',
        """A courtyard roof comprising a grid of small DC fans with a ring of LEDs attached to each. A ring glows when the wind drives the fan, with the color dictated by the direction, thus producing a visualization of wind currents withing a controlled space."""
    ),

    (
        'Teleknob',
        """A IOT add-on device for monitoring and controlling the position of physical knobs."""
    ),

    (
        'Robotic Marionette Game',
        """A game in which you control a real marionette, articulated by motors, using a gamepad to navigate a deformable, projection-mapped physical play field."""
    )
)

DESCRIPTION = 'Some things that I have considered making or doing'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title(f'{context.name} | Ideas'),
)

Body = lambda context: (
    Main(
        _class='ideas',
        children=(
            H1(DESCRIPTION),

            *section.Body(
                context,
                'Initiatives',
                name:='Ideas for more ambitious efforts',
                children=article_collection.Body(
                    context,
                    name=name,
                    items=INITIATIVES,
                    wide=True,
                )
            ),

            *section.Body(
                context,
                "Variations on Others' Product Themes",
                name:='Playful reimaginings of existing consumer products',
                children=article_collection.Body(
                    context,
                    name=name,
                    items=VARIATIONS
                )
            ),

            *section.Body(
                context,
                'Realized by Others',
                name:='Things that occurred to me that others actually created',
                children=article_collection.Body(
                    context,
                    name=name,
                    items=REALIZED_BY_OTHERS
                )
            ),

            *section.Body(
                context,
                'Small Bites',
                name:='Selections from my notes',
                children=article_collection.Body(
                    context,
                    name=name,
                    items=SMALL_BITES
                )
            ),
        )
    ),
)
