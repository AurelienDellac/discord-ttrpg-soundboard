# DISCORD TTRPG SOUNDBOARD & BOTS
A soundboard to manage music and ambience (from local storage or youtbe) during your discord TTRPG sessions. I have built this tool for my very own purpose so it is a bit shaky but I decided to share it if it can help someone. I know that some built-in or online solutions exist for this but sometimes nothing match exactly your needs so you have to get your hands dirty. You can use this tool as you want, copy it, fork it do as you want. If you do some improvments do no hesitate to share it whith me to ensure everybody can enjoy it. 

## General overview
The tool consists of 2 Discord music bots and a soundboard displayed in a web view. The soundboard allow you to control the music played by the bots throught the interface. The interface should be responsive enough for every usage but it is not perfect (shaky I said!). 

![The soundboard](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/c114ffbe-a0fa-43b5-b62d-e13f9e368f43)


## Installation and configuration
### Technical aspects
The tool consists of 2 Discord music bots and a soundboard displayed in a web view. The soundboard allow you to control the music played by the bots throught the interface. The bots cannot be controlled throught the discord chat except for joining and leaving a voice channel. The idea is to have two bots to manage simulteanously music/ambience and the sound effects. But you can use the two bots in the way you want even just one if you prefer (just kick the other one from the vocal).

The bots are hosted with python and a Lavalink server (version 3.7.8).

### Download
To download the tool you can either clone the repository or download the soure code of the last [release](https://github.com/AurelienDellac/discord-ttrpg-soundboard/releases). If you use the second option, extract all the files from the downloaded archive. Once you have dowloaded the tool you can try to launch it. To facilitate this step I wrote a batch file managing the start of the different components. So you can just execute the file ``TTRPG_SOUNDBOARD_LAUNCHER.bat`` and the Soundboard should open as describe in [launching section](#launching). It is currently empty but the next step is to configure the bots.

### Bots configuration
As explain the soundboard consist in two discord bots for music. So to configure the soundboard you have to setup and configure these two bots. For those who don't know how it works I will explain all but the others can skip to the next step.

1. Developper portal
   - Go to the discord developper portal [application page](https://discord.com/developers/applications).
   - Login if not.
2. Register a bot (you will have to repeat this step for the second bot)
   - Create a new application (top right button) and name it (you can name the bot music and sound-effect for example) :
     
     ![screenshot](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/dd2f8eda-ca2b-4572-8f2e-380678374155)

   - Custom the general information and the bot image if you want.
   - Go to the ``Bot`` section on the left.
   - Scroll down to the ``Privileged Gateway Intents`` section
   - Accept the three intents and save changes :
     
     ![screenshot](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/f1c8ff09-67b6-4c57-a4e2-1deec4a74438)

   - Your bot is now setup repeat the operation for the second one.
3. Invite the bots to your discord server
   - Got to the ``OAuth2 --> URL Generator`` section on the left.
   - Chose the ``bot`` scope.
   - Select ``send messages``, ``send messages in threads``, ``connect`` and ``speak`` permissions :

     ![screenshot](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/3ad6e9bc-5f1f-41e7-ae05-6532b9119a39)
     
   - Copy the generated url at the bottom of the page.
   - Paste the link in your web browser.
   - Chose the server where you want to add the bot and validate all next steps.
   - Your bot should have been added to your server ! Repeat the operation for the second bot.
     
<br/>
 Now that your two bots are setup you have to setup your environment so the Soundboard can start the bots and use them.

### Environment configuration
To setup the environment you have to go to the Soundboard folder of the tool repertory. To ensure that you are in the right place there should be a ``main.py`` and a ``soundboard.py`` file. In this folder you have to create a ``.env`` file. To do that create a text document (.txt) named "txt". Open it in notepad and go to file, save as.  Name it ".env" and chose "all files" option in "Save as type" then save. Your ``.env`` file should have been created and you can delete the txt file.

You can now open the ``.env`` file with notepad (or any IDE/code editor) and add the following lines :

```env
DISCORD_BOT_MUSIC_TOKEN=
DISCORD_BOT_SE_TOKEN=
DISCORD_BOT_MUSIC_PREFIX=;;
DISCORD_BOT_SE_PREFIX=;;
LOCAL_STORAGE_FOLDER=absolute/path/to/folder/
```

There are 5 options in this file :
- the token of the first bot - music bot ;
- the token of the second bot - sound-effect bot ;
- the prefix for the first bot commands in discord ;
- the prefix of the second bot commands in discord ;
- the absolute path to the folder where the soundboard will search for local files (see [managing sounds](#managing-sounds-and-categories) for more information)

You can configure the last three options as you want. For the bots tokens go to your discord developper application page. The token can be found in the bot section of each application by clicking on ``reset token``. Then paste each token in the corresponding option.

You can now lauching the tool by executing the batch file and the bots should now be online in your discord server.

### Better launcher and shortcut
WIP

## Use
The tool consists of 2 Discord music bots and a soundboard displayed in a web view. The soundboard allow you to control the music played by the bots throught the interface. The bots cannot be controlled throught the discord chat except for joining and leaving a voice channel.

The idea is to have two bots to manage simulteanously music/ambience and the sound effects. But you can use the two bots in the way you want even just one if you prefer (just kick the other one from the vocal).

### Launching
When you launch the tool (a combination of batch, jar and python script) it opens a Windows console and a webview. You can minimize the console you will probably have no use for it. The webview contain the soundboard.

![The tool console](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/df596735-2349-4ba0-982f-d1efec75f9db)
![The soundboard](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/c114ffbe-a0fa-43b5-b62d-e13f9e368f43)

### Bots control
The soundboard consists in two main sections corresponding to each bot and the sounds are dispatched in differents sub categories. You can chose which sound each bot plays by clicking on a sound button. The sounds can come from local storage files or youtube links as explain in [the customization section](#customization). Each bot have a a list of commands at the bottom of its body :
- Pause
- Resume
- Stop
- Reset volume to default
- Lower volume
- Increase volume
- Switch on repeat one mode
- Switch off repeat one mode

![Bot commands on the soundboard](https://github.com/AurelienDellac/discord-ttrpg-soundboard/assets/33094417/873a97e5-f251-4331-9ecc-6b075ac372c2)

### Hiding categories
You can also hide a category by clicking on the top right corner eye icon. To show it back you can use the menu in the top right corner of the bot body. This menu can also be used to hide categories. Hiding categories can be useful for complex soundboards or for display issues.

### Closing
WIP

## Customization
### Managing sounds and categories
The sounds are managed through a `config.json` file located in Soundboard/soundboard_web/. There should be a `config.example.json` to start with that you can rename `config.json`. In this file you have two main sections which are `music` and `sound_effects` and each have an inner section named `sounds`. Do not change this labels if you don't want to affect the code. For each bot you have to define at least one category to put the sounds in but you can add as many categories as you want. You will just have to test how it displays to ensure a good utilisation.

To add a sound you have to precise its name (what display on the soundboard button) and its value. The value can be either :
- a local file by precising the tag `{sound_folder}` before the file name and extension. See [environment configuration](#environment-configuration) to configure the local store folder.
- a youtube link by precising the tag `{youtube}` before the video link.


There is an example of my `config.json` file for a Lord of the Rings session using either local files and youtube videos :
```json
"music" : {
    "sounds" : {
        "The Shire" : {
            "Day"                 : "{sound_folder}the-shire.mp3",
            "Night"               : "{sound_folder}the-shire-night.mp3",
            "Northern moors"      : "{sound_folder}windy-nature.mp3",
            "Inn"                 : "{sound_folder}the-shire-tavern.mp3",
            "Suspense"            : "{sound_folder}suspense.mp3"
        },
        "Other ambiences" : {
            "Waiting ambience (the witcher)"    : "{youtube}https://www.youtube.com/watch?v=zAAVbFToD10",
            "Waiting ambience (LOTR)"           : "{youtube}https://www.youtube.com/watch?v=IxQ6sBDoylQ",
            "Fight"                             : "{sound_folder}fight-low-level.mp3"
        }
    }
},
"sound_effects" : {
    "sounds" : {
        "Scenario effects" : {
            "Door knocking"            : "{sound_folder}se-door-knocking.mp3",
            "Dogs"                     : "{sound_folder}se-dogs-angry.mp3",
            "River"                    : "{sound_folder}river.mp3",
            "A Elbereth Gilthoniel"    : "{sound_folder}elbereth-gilthoniel.mp3"
        },
        "General effect" : {
            "Men/Women yelling"     : "{sound_folder}se-men-yelling.mp3",
            "Arrow"                 : "{sound_folder}se-arrow-wood.mp3",
            "Sword on shield"       : "{sound_folder}se-sword-wood.mp3",
            "Sword wound"           : "{sound_folder}se-sword-bloody.mp3",
            "Bloody sword wound"    : "{sound_folder}se-sword-very-bloody.mp3"
        }
    }
}
```

### Background
You can put any image in the background of the soundboard either ``.pnj``, ``.jpg`` or ``.gif``. The image will keep its size when put in the background so little images will be repeated and enormous images will be "zoomed". Personnaly I use a 1920x1080 of Rivendell as you can see in the example or in your soundboard as it is the default background. <ins>**I recommend using a JPG image**</ins> because there is an auto customization making the bot body header having a color based on the background (it's so fancy I love it lol).

To change the background just put your image in the ``/Soundboard/soundboard_web/media`` folder and rename it ``background`` (no caps).

### Title
WIP
