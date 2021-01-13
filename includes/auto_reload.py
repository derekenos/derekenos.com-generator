
from lib import NotDefined
from lib.htmlephant import Script

Head = lambda context: (
    Script(
"""
document.addEventListener("DOMContentLoaded", () => {
  const eventSource = new EventSource("/_events");
  eventSource.onmessage = event => {
    const [command, payload] = JSON.parse(event.data)
    switch(command) {
      case "reload":
        window.location.reload()
      break
      case "error":
        alert(payload)
      break
      default:
        console.error(`Unknown command "${command}" with payload: ${payload}`)
      break
    }
  }
})
"""
    ),
)

Body = NotDefined
