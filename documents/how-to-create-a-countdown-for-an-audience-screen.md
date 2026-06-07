---
title: "How to Create a Countdown for an Audience Screen"
source: "https://support.renewedvision.com/hc/en-us/articles/360050786794-How-to-Create-a-Countdown-for-an-Audience-Screen"
type: "official_docs"
product: "ProPresenter"
---

# How to Create a Countdown for an Audience Screen
**This article is Part Two of a series of articles on using timers on Audience Screens and Stage Screens. Since all of these features are interconnected, each article references topics covered in other articles. Use the links below to navigate between each part of this series.**

Part One: [Setting up Timers in ProPresenter 7](/hc/en-us/articles/360050782494)

Part Two: You're reading it!

Part Three: [Using Timers on Stage Screens](/hc/en-us/articles/360053250613)

In Part One of this series, you learned how to set up timers. Now it's time to turn those timers into Countdowns that can be shown on your Audience Screen(s). There will be some assumptions of prior knowledge at various steps in this article. If you aren't sure how to do a specific step, take a look at the [User Guide](https://learn.renewedvision.com/propresenter) for additional help.

There are several ways to show a timer on screen. While they all work similarly, there are some differences among them. We'll cover several options in this article, but you may also want to [watch this tutorial video](https://renewedvision.com/propresenter/tutorials/#215277) for additional information and to see the different methods being used in real time.

## Basic Countdown

The first method we'll cover is the simplest option. If you're familiar with previous versions of ProPresenter, this is the same way you are used to showing a countdown. We will simply be creating a Countdown Message to show the timer over whatever you're showing on screen.

Before you can show a timer on a screen, you need to create a theme for it. Click on Themes in the toolbar and select New Theme. Give your new theme a name.

Once the Theme Editor is open, add a new text box and style the text the way you want your timer to look. Keep in mind what you will be showing in the text box. If you plan on using it to show a 5-minute countdown, you may want to enter "5:00" in the text box so that you can make sure the text box is big enough to show the timer.

![Screenshot 2026-04-23 at 8.40.33 AM.png](/hc/article_attachments/51075815909011)

For this method, we don't need to worry about using Linked Text. We'll cover that in other methods. Once you have created your text box and formatted it the way you want your timer to look, you can close the Theme Editor.

Open Messages from the toolbar. You may need to click on the + in the top right corner and create a new message for your countdown. Click the "Edit" button in the top right corner to expand all of the options available for your new message if it isn't already selected.

You can add a token by opening the drop-down menu where it says "Add a Token". These are dynamically linked to text boxes that are available for Messages and to all of the timers you have created. You can see that we have already selected our Countdown token by clicking on "Add a Token", hovering on the timer, and choosing this timer named "Countdown" (yours will be whatever you have named your timers). Most of the tokens add text boxes that you can fill out. We won't be looking at this in this article. However, we will show adding text along with the token. You can type directly in the box in the middle and have the text shown alongside the clock. 

![Screen_Shot_2022-01-28_at_2.21.52_PM.png](/hc/article_attachments/4416558799251)

There are several options that you can adjust for your countdown message. Directly below the tokens are the theme and the behavior setting. Select the theme you created earlier. The Dismiss options control what happens with the clock. There are three options available. It requires you to manually clear the message when the timer reaches zero. After the timer expires, the message will be removed when it reaches zero (or the specified end time, depending on the type of timer you're using). After Time Expires is kind of like a Go To Next Timer. If you select one of these options, it controls how long the message is kept on screen. This is not generally an option you will use with a countdown message.

![Screen_Shot_2020-08-19_at_3.32.25_PM.png](/hc/article_attachments/360085178674)

The rest of the options are ones you're already familiar with from the Timer screen. You can override the default Timer options here if you need to make any changes. You can select a custom transition for Messages. If you don't select anything, the global slide transition will be used. You can click the Show button to start a countdown or show a message from this screen. Any active message can be cleared from the list on the left. To delete an existing message, click on it in the list on the left and press the delete key on your keyboard. You can also enable overrun, which lets the timer continue counting after the duration has been reached. This can be useful for communicating to presenters on stage that they are over the allotted time for this segment.

## 

## Countdown Using Linked Text

The next option for displaying a countdown is to use Linked Text. This option lets you get more creative with how your timer is shown and integrated into your presentation. By using Linked Text, you can integrate your timer into a presentation or a Prop.

Add your text box and style it the way you want your numbers to look. Check the box next to Linked Text on the Text tab, then select the Timer you need. You will notice that your placeholder text changes to a series of numbers. This is the default text used with all Linked Text timers and cannot currently be changed.

![Screen_Shot_2020-08-19_at_3.15.14_PM.png](/hc/article_attachments/360085170774)

You will also see an additional set of Format options below this option. The Format settings control which numbers are shown with the timer. From left to right, the settings are hours, minutes, seconds, and milliseconds. Each time segment has additional options when you click the button. Let's take a look at the options for minutes. Each time segment has the same options.

- **m:** Always show the minutes but hide leading zeros
- **mm:** Always show the minutes and show leading zeros
- ~~**m**~~**:** If there are minutes, then it shows them with no leading zeros; if there are no minutes, then it doesn't show them
- ~~**mm**~~**:** If there are minutes, then it shows them with leading zeros; if there are no minutes, then it doesn't show them
- **- -:** Hide the minutes text and it will convert the time to seconds

![time_options.png](/hc/article_attachments/360078404774)

Adjust these settings to see how they affect your timer until you find a combination that you're happy with. Let's take a quick look at how these settings work. If your timer is 1 hour and 15 minutes. That time could be displayed at 01:15:00.00. By changing the options, you will change how that timer is displayed. You could show that timer at 1:15:00.00. 1:15:00, 1:15, 75:00, 4500, plus a few other combinations.

## Starting a Timer

There are several ways to start a timer. You're already familiar with two of these, which are to start it from Timers or Messages. The other two methods are designed to give you more flexibility with starting your timer when you need it, and also give you the additional option to reset the timer or change the settings if necessary.

The first method we'll look at is starting your timer with a Header. You can add headers to a playlist by clicking the + button and selecting New Header at the top of your playlist.

![Screen_Shot_2020-08-19_at_4.25.58_PM.png](/hc/article_attachments/360085191454)

This will add a new header to your playlist. You can click to rename it in the playlist or by clicking on the gear icon in the Show area of the screen, shown below. You can also set a color for the header.

Headers can be used to start, reset, stop, or update an existing timer. The first option lets you select the timer you want to trigger. The second box lets you Start, Stop, or Reset the selected timer. If you check the Set Configuration box, you'll see the additional settings shown in the second screenshot below. You can update an existing timer and even change the clock type entirely. This can be particularly helpful if you run countdowns or elapsed timers for each segment of your service or event on your stage screen. You will also need to use this option to reset your timer if you didn't reset it via Timers. Click Trigger to make the header do whatever you set the timer options to.

If you are embedding a timer on one of your slides in an announcement loop (like shown in the video linked at the top), you would want to start your timer with a Header or from Timers to prevent the clock from resetting every time.

![Screenshot 2026-04-23 at 10.05.57 AM.png](/hc/article_attachments/51075845799443)![Screenshot 2026-04-23 at 10.07.01 AM.png](/hc/article_attachments/51075815910547)

The second method for starting a timer is via slide actions. Right-click on a slide, select Add Action, select Timer, and then select the time you want to start. After you select the timer, you will be given the same options available in the Header. Configure the timer with the necessary settings. Every time this slide is selected, the Timer Action will be triggered, so you don't want to use this method on an active slide in a looping presentation. If you add a slide and then disable it, you can add actions to that slide. You can manually click on a disabled slide, but it will be ignored in a looping presentation.

![Screenshot 2026-04-23 at 10.09.37 AM.png](/hc/article_attachments/51075815910803) ![Screen_Shot_2020-08-19_at_4.54.07_PM.png](/hc/article_attachments/360085194354)

If you added your timer to a Prop, you can also trigger the Prop with an Action. You will need to click on the Action Palette option to access the Props Action. Drag it onto the slide, then select the Prop you want to start with. You will still need to use one of the covered methods to start the timer.

![Screenshot 2026-04-23 at 10.11.55 AM.png](/hc/article_attachments/51075845801235)
