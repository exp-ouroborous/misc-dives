# Markdown To HTML

## What question are we exploring?

Can a static page load a real Python package in Pyodide and use it for Markdown conversion?

## What did we try?

We used Pyodide's `micropip` support to install the Python `markdown` package in the browser, then called a local `convert_markdown` helper.

## What did we learn?

Pyodide can run more than stdlib demos, but package installation adds a visible loading step and needs clear failure messaging.

## What should happen next, if anything?

Add a small extension selector only when a package or extension is known to work well in Pyodide.
