# Project Configuration

This project uses several configuration files and environment variables to store sensitive information and customizable settings. To keep your real configuration secure and avoid committing sensitive data to the repository, **example files** are provided.

## Configuration Files

- `config/config.example.json`  
  Just replace deeplol link (must be deeplol) and prompt. Change name to `config.json`.  

- `config/channels.example.json`  
  You will add channels with commands anyways so just change name to `channels.json`.

- `.env.example`  
  Input your own `OPENAI_API_KEY` and `DISCORD_BOT_TOKEN` here. You can get them at [OpenAI](https://platform.openai.com/signup) and [Discord Developer Portal](https://discord.com/developers/applications).
  Rename this file to `.env` and add your real secrets.