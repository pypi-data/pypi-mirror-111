## Usage


        => Create folders named `plugins`, `addons`, `assistant` and `resources`.<br/>
        => Add your plugins in the `plugins` folder and others accordingly.<br/>
        => Create a `.env` file with `API_ID`, `API_HASH`, `STRING_SESSION`, 
        `TG_BOT_USER_NAME_BF_HER`, `TG_BOT_TOKEN_BF_HER` as mandatory environment variables.<br/>
        => Run `python -m GODBOY` to start the bot.<br/>
        
        ### Creating plugins
        To work everywhere
        
        ```python
        @bot.on(admin_cmd(pattern="start"))
        async def _(event):   
            await event.edit("GODBOY Is Started")   
        ```
        
        Assistant Plugins 👇
        
        ```python
        @god.on(events.NewMessage(pattern=("/start")))   
        async def _(event):   
            await god.send_message("Hi Master Your Assistant is in your service😇")   
        ```
