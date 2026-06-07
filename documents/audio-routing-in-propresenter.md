---
title: "Audio Routing in ProPresenter"
source: "https://support.renewedvision.com/hc/en-us/articles/360052696094-Audio-Routing-in-ProPresenter"
type: "official_docs"
product: "ProPresenter"
---

# Audio Routing in ProPresenter
ProPresenter's audio engine allows for inputs from multiple audio devices to be routed in to any of up to 16 internal ProPresenter audio channels. These can then be routed out to the channels of a primary audio output device, as well as SDI/NDI feeds with separate routing. For example, you can input any or all of the channels coming into your computer from a mixing console to ProPresenter's internal channels, specify the internal channels used for any audio or video played back from ProPresenter, and route these ProPresenter channels to the channels of your output device.

In addition to simple default setups (Channel 1 is Left, Channel 2 is Right, etc.), ProPresenter is capable of fully customizing your audio setup,  This article will discuss how you route both Audio Inputs and Outputs inside of the program. 

## Routing Audio Outputs

You can customize what ProPresenter audio channels go to specific channels on your audio output device. In the Audio Preferences pane, you first specify the number of channels of audio you want ProPresenter to process. Then, clicking on Channel Routing for your main output device will bring up a window that allows this custom routing.

The left side of the Audio Routing window shows you ProPresenter Channels based on the number you specified in the channel count. You can click on the channel name to rename it if desired. To the right are the channels supported by your output device.

![Audio tab of ProPresenter Settings_Routing.png](/hc/article_attachments/34668299344147)

Click on the cells where you want the audio to be heard.  For example, if you want ProPresenter’s Channel 1 to output to Channel 3 of your output, click on the cell at the intersection of those two selections and the box will light up. To turn off a cell, click on it again.  Click on the **M** next to a channel to Mute that channel. Click **S** to Solo that channel. Click **T** to send a Tone to that channel. You can turn these functions on and off for as many channels as you wish, which is a great tool for troubleshooting audio signals in your system.

On the top left of the routing windowpane, you can click on the **M** to mute all of the channels. If you have one or more channels solo'd, click the **S** in the top left to turn them all off at the same time. Click on the Mapping drop-down and select **Auto** to automatically route ProPresenter channels to their counterparts on the output (1:1: 2:2, etc.). **Clear** removes all of the current routes.

Media played back in ProPresenter can also be routed to specific ProPresenter Channels. By default, the audio channels of your media will be routed to the corresponding ProPresenter channel (1:1, 2:2, etc). You can access individual Audio Routing for a specific Media Action in the Cue Inspector's Audio tab (right click on the media action, choose "Inspector", then select the audio tab on the right of the inspector window). You will only be able to access the Audio tab if the Media Action you're viewing in the Inspector has audio embedded within it.

![Inspector Audio Routing.png](/hc/article_attachments/34668299346579)

Just like in the routing for outputs, the inspector's left side lists all of the audio channels for the piece of media that is selected. The top lists the audio channels that are available in ProPresenter.

Click on the cell of the row/column that you want the audio to play in. Click on the **Mapping** drop-down and select **Auto** to autofill the cells and **Clear** to remove all of the selected cells.

## Routing Audio Inputs

The option for routing audio inputs allows you to use devices such as USB audio interfaces and choose how channels of the device are routed to the internal ProPresenter channels. 

To set this up, go to the "Input" tab of ProPresenter Preferences and select your Audio Input device from the device list on the left.  More information on how to add Audio Inputs is available [here](https://support.renewedvision.com/hc/en-us/articles/360053484013).  

Select your Audio Input source and you will see all incoming channels from the Source appear in the bottom part of the window.  You can then click the Routing button to choose what channels from the Input go to what channels of your ProPresenter channels. 

![EVO8 Routing_V2.png](/hc/article_attachments/34668299350291)

Once you open the Routing window, you’ll notice that the left side shows your Input channels and the top shows your ProPresenter Audio channels.  Selecting Auto will match the channels up in the standard way (input channel 1 routes to ProPresenter channel 1 and so on).  If you wish to customize this, you would simply click on the cell at the intersection of those two selections and the box will light up.  So, in the example above, Channels 3 and 4 on the input would be sent to Channels 1 and 2 of your output.
