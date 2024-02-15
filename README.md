## Inspiration
As we were discussing hackathon ideas, we realized that we were communicating over Discord, an ever-growing platform. Most importantly, Discord is about community. With that and the theme in mind, we found that there are extremely limited built-in time functionalities. Take virtual hackathons for instance - Discord is one of the most common venues to host events of this nature. As participants, we want a way to clearly know when the submission deadline is approaching. On the other hand, the event organizers want a way to clearly communicate the schedules. What if there was a way to solve this problem by creating an all-in-one solution native to the Discord platform?

## What it does
Big Beautiful Clock is a Discord bot that can create shared clocks, stopwatches, timers, and alarms, sent in a single message. These time functions can be configured by timezone and interact with multiple users at the same time. The time displays can simply be deleted by deleting the message.

## How we built it
We implemented the Discord bot using Python and the Discord.py and datetime libraries.

## Challenges we ran into
A major issue that we ran into was the workflow. We have a single bot instance to work on, and multiple versions of the code. So, we had strictly one person running the bot at a time, to prevent it from double-editing messages or any other unpredictable behavior.

## Accomplishments that we're proud of
We are really proud of how we stored the message data of each time display. Obviously, there needs to be some way for the bot to access the messages that it has sent to edit it and change the display. Our solution to this was to simply annex Discord servers. More specifically, we created a channel that the bot reads and writes message data in, meaning that we don’t have to worry about storage space, and if we needed to search for specific content in a message, the already-implemented Discord search bar could be utilized.

## What we learned
For some of us, using Discord’s API as well as Python was a first time experience. Naturally, we learned a lot about these. Discord’s slash commands are also fairly new, so we also learned how to incorporate slash commands into our ideas. Finally, we learned the importance of planning well ahead and having a proper workflow. Doing these two things would have greatly helped in the efficiency of our programming and developing in general, as explained above.

## What's next for Big Beautiful Clock
One future addition that we hope to make is adding permissions for buttons and other functionalities. This would make it so that only the user that created the clock or timer would be able to edit it, stopping others from changing clocks that they didn’t create. Another change we hope to make is to change our method of reading and writing information more optimized in order to allow for scaling to hundreds of servers at the same time. Our method right now works great on a smaller scale but would definitely need to be fine-tuned if we wanted to have the bot in more servers.
