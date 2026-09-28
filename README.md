# Darkcorner Discord bot

Slash command `/generate <prompt>` — the bot replies in-channel with the generated image.

## 1. Discord app (2 minutes, in a browser)

1. Go to https://discord.com/developers/applications → New Application → name it.
2. Bot tab → Reset Token → copy it. This is `DISCORD_TOKEN`.
3. General Information tab → copy Application ID. This is `CLIENT_ID`.
4. Installation tab → Install Link → add `applications.commands` scope → open the link and add the bot to your server.
5. (Optional, recommended) Right-click your server name → Copy Server ID. This is `GUILD_ID` — commands appear instantly instead of within the hour.

## 2. GitHub

Upload `index.js` and `package.json` to your repo (root folder).

## 3. Render

1. New → Web Service → connect the repo. Start command: `node index.js`.
2. Environment tab → add `DISCORD_TOKEN`, `CLIENT_ID`, and (optional) `GUILD_ID`. Never put the token in the code.
3. Deploy. Logs should show `Logged in as <name>` and `Registered /generate`.

## 4. Use it

In your server type `/generate prompt: a neon castle` — the image posts back to the channel.

## Notes

- Images come from Pollinations (free, no key) — plain generations, not your Perchance generator's styles.
- Render's free tier sleeps when idle, so the first command after a while can take ~a minute; later ones are fast.
- Only people in servers the bot was added to can use it.
