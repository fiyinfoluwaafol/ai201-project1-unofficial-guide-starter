---
title: "Using Looks to Show Different Screen Content in ProPresenter"
source: "https://support.renewedvision.com/hc/en-us/articles/360041407174-Using-Looks-to-Show-Different-Screen-Content-in-ProPresenter"
type: "official_docs"
product: "ProPresenter"
---

# Using Looks to Show Different Screen Content in ProPresenter
The Looks window allows you to choose which layers visually appear on each audience screen you’ve setup. This could be used if you only wanted to show the media layer on one screen or not the other, only wanted to show messages on one screen, etc.

![Screenshot 2024-11-15 at 4.14.53 PM.png](/hc/article_attachments/35466543774739)

What you should see in this window are several rows that show what layer they are in ProPresenter’s Output. With the “Enable Identify” feature you can see this visually as to what is going to your Output. You will also notice that each screen you have set up as an audience screen in [Screen Configuration](/hc/en-us/articles/360041879173) shows up as a column in this window as well, so you can choose what layer of ProPresenter’s output shows up on each screen. To edit what appears on a Stage Screen you would follow the steps in this [Stage Screen Layout Article](/hc/en-us/articles/360041407794).

Each setting you create and save in this menu is called a “Look Preset”, and you can have an infinite amount of these Look Presets. To rename a Look Preset, click in the name area in the header of the Looks menu. To remove a Look Preset, simply right click on one and press “Delete."  

### **Example Use**

Now we'll walk through an example use of the looks feature in ProPresenter. In this example, let's say you have three screens: one at the front of your auditorium that is getting both media and lyrics, one that is sending to your stream that is just getting lyrics in a different format(lower thirds), and one that is sending announcement slides to your lobby that is just getting the [Announcement Layer.](/hc/en-us/articles/360041809953)

In order to do this, you would turn the slide layer for both the "Main Screen" and "Lower Thirds" screen, the media layer for just the "Main Screen" and the Announcement Layer for just the "Lobby" screen. In addition, you will open dropdown for the Presentation layer in the "Lower Thirds" screen and choose the alternate theme that will determine how the text on this screen appears. You would not do this for the "Main Screen" because you would want your "Main Screen" lyrics to appear as they do in your created presentation.

If ever your lyrics appear differently on a screen than they do in a presentation and you don't want that to happen, you should check to make sure that an alternate theme is not applied here in the looks window next to "Presentation"

![Screenshot 2024-11-15 at 4.29.57 PM.png](/hc/article_attachments/35466543776531)

### **Changing Look Presets**

**To change a look preset inside of the Looks window, if you have more than one available, simply choose one from your list, and select “Make Live”.**

A second way to change looks is with Slide Actions. When you have multiple Looks set up in the Looks window, you can right-click on a slide, hover on Add Action->Audience Look->Choose the desired look preset. Now, when you trigger that Slide, you will trigger a Look Preset change. 

![Screenshot 2024-11-15 at 4.39.30 PM.png](/hc/article_attachments/35466819932563)

A third way to change a look preset is via the Screens Menu in the top Menu Bar. Simply Click on Screens->Live: Name of Current Look->Choose the desired look preset.

![Screenshot 2024-11-15 at 4.41.11 PM.png](/hc/article_attachments/35466793990675)

Finally, you can add a Look Preset to a [Macro](/hc/en-us/articles/4402663090323) by right clicking on a Macro in Show Controls->Add Action->Choose desired look preset. 

![Screenshot 2024-11-15 at 4.44.56 PM.png](/hc/article_attachments/35466793997075)
