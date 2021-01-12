
from lib import NotDefined
from lib.htmlephant import Script

Head = lambda context: (
    Script(
"""
document.addEventListener("DOMContentLoaded", () => {
  const eventSource = new EventSource("/_events");
  eventSource.onmessage = event => {
    const command = JSON.parse(event.data)

    // DEBUG
    console.debug(`got command: ${command}`)

    switch(command) {
      case "reload":
        window.location.reload()
      break
      default:
        console.error(`Unknown command: ${command}`)
      break
    }
  }
})
"""
    ),
)

Body = NotDefined
