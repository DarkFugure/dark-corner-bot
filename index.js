const { Client, GatewayIntentBits, REST, Routes, SlashCommandBuilder, EmbedBuilder } = require("discord.js");

const TOKEN = process.env.DISCORD_TOKEN;
const CLIENT_ID = process.env.CLIENT_ID;
const GUILD_ID = process.env.GUILD_ID || null;

if (!TOKEN || !CLIENT_ID) {
  console.error("Missing DISCORD_TOKEN or CLIENT_ID env vars. Set them in the Render dashboard.");
  process.exit(1);
}

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once("ready", async () => {
  console.log("Logged in as " + client.user.tag);
  const cmd = new SlashCommandBuilder()
    .setName("generate")
    .setDescription("Generate an image from a prompt")
    .addStringOption((o) => o.setName("prompt").setDescription("What to draw").setRequired(true));
  try {
    const rest = new REST({ version: "10" }).setToken(TOKEN);
    if (GUILD_ID) {
      await rest.put(Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID), { body: [cmd.toJSON()] });
      console.log("Registered /generate in guild " + GUILD_ID);
    } else {
      await rest.put(Routes.applicationCommands(CLIENT_ID), { body: [cmd.toJSON()] });
      console.log("Registered global /generate (can take up to an hour to appear everywhere)");
    }
  } catch (e) {
    console.error("Command registration failed:", e);
  }
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isChatInputCommand() || interaction.commandName !== "generate") return;
  const prompt = interaction.options.getString("prompt", true);
  await interaction.deferReply();
  const seed = Math.floor(Math.random() * 1000000);
  const url =
    "https://image.pollinations.ai/prompt/" + encodeURIComponent(prompt) + "?seed=" + seed + "&nologo=true";
  try {
    const embed = new EmbedBuilder()
      .setTitle("Generated image")
      .setDescription(prompt.length > 2000 ? prompt.slice(0, 2000) : prompt)
      .setImage(url)
      .setColor(0x5865f2);
    await interaction.editReply({ embeds: [embed] });
  } catch (e) {
    console.error(e);
    await interaction.editReply("Image generation failed, try again.");
  }
});

client.login(TOKEN);
