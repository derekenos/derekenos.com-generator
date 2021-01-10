
from lib.htmlephant import Style

Head = lambda context: (
    Style(
"""
* {
  font-family: sans-serif;
}

body {
  background-color: #373366;
  color: #eef;
  margin: 0;
}

body > * {
  padding: 0.4rem 1rem;
}

video,
img,
iframe {
  border-radius: 8px;
}

a:link,
a:visited {
  color: #aaf;
}

a:hover,
a:active {
  color: #eef;
}

h1 {
  font-size: 1.4rem;
  font-weight: normal;
  line-height: 1.4rem;
}

h2 {
  font-size: 1rem;
  font-weight: normal;
  margin-bottom: .4rem;
}

h3 {
  font-size: 1rem;
  font-weight: normal;
  line-height: .8rem;
  font-style: italic;
  margin-top: 0;
  opacity: 0.8;
}

nav {
  display: table;
  width: 100%;
  padding: 0;
}

nav > ol {
  display: table-row;
  justify-content: center;
}

nav > ol > li {
  display: table-cell;
  font-size: 1.2rem;
  text-align: center;
  border: solid #262255 1px;
}

nav > ol > li.current {
  border-bottom: none;

}

nav > ol > li > a {
  text-decoration: none;
  display: block;
  width: 100%;
  background-color: #151144;
  padding: 1rem 0;
}

nav > ol > li > a:hover {
  text-decoration: underline;
}

iframe,
img,
video {
  max-width: 100%;
}

.content {
  display: flex;
  flex-flow: column;
  padding: 0 0 2rem 0;
}

body > h1 {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 1rem;
  border: solid 1px #222;
}

.item {
  padding: 1rem;
}

.item.wide {
  max-width: none;
}

.contact ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

@media screen and (min-width: 1024px) {
  nav {
    display: block;
    border-bottom: solid #888 1px;
  }

  nav > ol {
    justify-content: center;
  }

  nav > ol > li {
    padding: 1rem 0 1rem 4rem;
    font-size: 1.2rem;
    text-align: left;
    border: none;
  }

  nav > ol > li > a {
    background-color: transparent;
  }

  .content {
    flex-flow: row wrap;
    justify-content: space-between;
    padding: 0 3rem 2rem 3rem;
  }

  .item {
    max-width: 400px;
  }
}

.patreon-widget {
  position: fixed !important;
  bottom: 0.5rem;
  right: 0.5rem;
  opacity: 0.85;
  animation: fade-in 1s ease-in;
}

@keyframes fade-in {
  0% { opacity: 0 }
  100% { opacity: 0.85 }
}
"""
    ),
)
