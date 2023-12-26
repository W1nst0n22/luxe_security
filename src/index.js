require('dotenv').config();
const { Client, IntentsBitField } = require('discord.js');

const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent,
    ],
});

client.on('ready', () => {
    console.log(`${client.user.tag} is on online.`);
});

client.on('messageCreate', (message) => {
    if (message.author.bot) {
        return;
    }

    console.log(message.content);
});

client.on('guildMemberAdd', (member) => {
    const guild = member.guild; // Get the guild
    const roleID = '1189082673193435186'; // Replace 'YOUR_ROLE_ID' with the actual role ID

    // Get the role based on the role ID
    const role = guild.roles.cache.get(roleID);

    if (role) {
        // Add the role to the member
        member.roles.add(role)
            .then(() => console.log(`Added role to ${member.user.tag}`))
            .catch(error => console.error('Error adding role:', error));
    } else {
        console.error('Role not found');
    }
});

client.on('interactionCreate', (interaction) => {
    if (!interaction.isChatInputCommand()) return;


    if(interaction.commandName === 'hey') {
        interaction.reply('hey!');
    }

    if(interaction.commandName === 'help') {
        interaction.reply('Do you need some help?');
    }

    console.log(interaction.commandName);
});

client.login(process.env.TOKEN)
    .catch(error => {
        console.error('Error during login: ', error);
    });
