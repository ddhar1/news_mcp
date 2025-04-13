# CurrentNews MCP 

Another basic MCP to help me search the news with the [Current News API](https://www.currentsapi.services/en)

# Usage with Claude Desktop

Add the following to your claude_desktop_config.json:
```
{
  "globalShortcut": "",
  "mcpServers": {
    "lastfm": {
            "command": "uv",
            "args": [
                "--directory",
                "DIR/TO/REPO/HERE",
                "run",
                "main.py"
            ],
            "env": {
        "LASTFM_API_KEY": "CURRENTSNEWS_API_KEY"}
        }

  }
}
```
# Example
![example of getting latest news](howitworks.png)