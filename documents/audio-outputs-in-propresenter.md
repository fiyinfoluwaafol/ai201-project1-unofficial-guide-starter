---
title: "Audio Outputs in ProPresenter"
source: "https://support.renewedvision.com/hc/en-us/articles/360052697694-Audio-Outputs-in-ProPresenter"
type: "official_docs"
product: "ProPresenter"
---

# Audio Outputs in ProPresenter
Audio Outputs are available to set up in the Audio tab of ProPresenter Settings. This tab shows the adjustable channel count, the Media Inspector audio output, the Main audio output, as well as SDI & NDI audio output. All of these outputs can have their own custom channel routing, by clicking on the routing button. The volume on all of these outputs can be adjusted from the slider as well.

![Audio Tab of ProPresenter Settings.png](/hc/article_attachments/34667899698323)

In the above user interface, you can adjust the amount of audio channels ProPresenter can process, for audio inputs and outputs. Should you be live streaming with ProPresenter, it is generally recommended that you choose a Channel Count of at least 4, two for the main left and right outs, and two for left and right inputs.

By default, the Inspector area is set to "Listen on Main", which just means that this output is set to whatever the Main device is set to, below it.

The Main area is to choose the device used for your main audio output from ProPresenter. You can adjust the delay for the output in this area as well.

The SDI & NDI area is for choosing the ability to send audio over NDI as well as audio over the BlackMagic Design SDK, through their drivers, and not through system audio.

### Channel Routing

You can route ProPresenter's audio channels to the channels of your output device here as well.

![Audio tab of ProPresenter Settings_Routing.png](/hc/article_attachments/34667884956179)

Audio routing as shown in the image above, can be broken down into a relatively simple concept. The rows on the left hand side are the device of where audio currently is, and the columns across the top are the device of where you're wanting to send audio. This is this way in every audio routing window within ProPresenter.

 More information on Audio Routing can be found [here](https://support.renewedvision.com/hc/en-us/articles/360052696094).

If you are outputting your main audio output via either NDI or SDI, you should enable the SDI & NDI option. More information on this output type is available in our article [here](https://support.renewedvision.com/hc/en-us/articles/360053282613). *(NOTE: if you are only using SDI or NDI for your audio output, you should choose "None" for you "Main" output and enable the SDI & NDI option.)*
