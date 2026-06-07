# Evaluation Plan Analysis

This note develops the evaluation plan for the ProPresenter unofficial guide before updating `planning.md`. It is a planning document only; it does not implement the final RAG pipeline or directly edit the required project template.

## Evaluation Goals

The evaluation set should test whether the system can:

- Retrieve the right source document for narrow ProPresenter questions.
- Answer with concrete steps or settings from the retrieved documents.
- Handle both official product terms and volunteer-style wording.
- Avoid answering unrelated questions from outside the source corpus.
- Respond responsibly to vague questions by narrowing the topic, asking for clarification, or giving a clearly scoped high-level answer.

The final CodePath section only asks for 5 test questions, but it is useful to design a wider evaluation pool first. The final 5 should mostly be specific, answerable questions because those are easiest to grade as correct or incorrect.

## Answerable Specific Questions

These are strong candidates for the required 5-question evaluation table. Each question is specific enough that the expected answer can be checked against the source documents.

| # | Question | Expected correct answer | Primary source |
| --- | --- | --- | --- |
| S1 | How do I open the Stage Layout editor in ProPresenter, and what shortcut can I use on Mac and Windows? | Open the Stage Layout editor from `Screens > Edit Layouts`. The shortcut is `Command+4` on Mac or `Control+4` on Windows. | `using-a-stage-screen-to-its-full-potential.md`; `keyboard-shortcuts-in-propresenter.md` |
| S2 | In a Stage Display layout, what does the `Screen Preview` item let me show? | `Screen Preview` can show a preview of any configured audience or stage screen, allowing the stage layout to mirror what is happening on one of those screens. | `using-a-stage-screen-to-its-full-potential.md` |
| S3 | If my lower-thirds lyrics look different from the main auditorium lyrics, where should I check first? | Check the Looks window, especially the alternate theme selected for the Presentation layer on the lower-thirds screen. If lyrics are unexpectedly different, make sure an alternate theme is not applied next to `Presentation` for that screen. | `using-looks-to-show-different-screen-content-in-propresenter.md` |
| S4 | How can I change a Look Preset when a specific slide is triggered? | Right-click the slide, choose `Add Action > Audience Look`, then choose the desired Look Preset. When that slide is triggered, ProPresenter will trigger the Look Preset change. | `using-looks-to-show-different-screen-content-in-propresenter.md` |
| S5 | What are the two main ways to create a countdown for an Audience Screen described in the countdown article? | The article describes creating a Countdown Message that uses a timer token, and using Linked Text in a text box so the timer can be integrated into a presentation or Prop. | `how-to-create-a-countdown-for-an-audience-screen.md` |
| S6 | When using Linked Text for a countdown, what do the timer format options control? | The format options control which time segments are displayed: hours, minutes, seconds, and milliseconds. Each segment can show or hide leading zeros, hide itself when empty, or convert hidden larger units into smaller units depending on the selected option. | `how-to-create-a-countdown-for-an-audience-screen.md` |
| S7 | Why should I start a timer from a Header or from Timers instead of with a slide action in a looping announcement presentation? | Starting the timer from a Header or from Timers prevents the clock from resetting every time the looping slide is selected. Slide timer actions fire each time the slide is selected, so they are not recommended for an active slide in a looping presentation. | `how-to-create-a-countdown-for-an-audience-screen.md` |
| S8 | In ProPresenter's Bible tool, what are the three ways to search for scripture passages? | Select from the Book menu, type a specific passage or verse range and press Enter, or search by keyword in the search box. A specific translation should be selected first from the menu on the left. | `using-bibles-in-propresenter.md` |
| S9 | What does the `Break on New Verse` Bible slide option do, and when is `Verse References` available? | `Break on New Verse` creates new slides for each verse in a passage. `Verse References` is only available when `Break on New Verse` is selected. | `using-bibles-in-propresenter.md` |
| S10 | How do I route ProPresenter audio channel 1 to output channel 3? | In Audio Preferences, set the number of ProPresenter audio channels, open `Channel Routing` for the main output device, then click the cell at the intersection of ProPresenter Channel 1 and output Channel 3 so the box lights up. | `audio-routing-in-propresenter.md` |
| S11 | In the Audio Routing window, what do the `M`, `S`, and `T` buttons do? | `M` mutes a channel, `S` solos a channel, and `T` sends a tone to that channel. These can be used for troubleshooting audio signals. | `audio-routing-in-propresenter.md` |
| S12 | What keyboard shortcut clears all active content in ProPresenter on Mac and Windows? | `F1` clears all active content on both Mac and Windows. | `keyboard-shortcuts-in-propresenter.md` |
| S13 | What keyboard shortcut shows a slide on the Stage Display only? | `Command+0` on Mac or `Control+0` on Windows. | `keyboard-shortcuts-in-propresenter.md` |
| S14 | How do I create a Macro and add actions to it? | Click the `[M]` icon in Show Controls, click the small `+` button to create a Macro, then right-click the Macro and choose `Add Action`, or drag actions from `View > Action Palette` onto the Macro icon. | `using-macros-in-propresenter.md` |
| S15 | How can I trigger a Macro from a slide? | Right-click the slide, choose `Add Action > Add Macro`, then select the Macro. Alternatively, drag the desired Macro from Show Controls directly onto the slide. | `using-macros-in-propresenter.md` |

## Vague In-Domain Questions

These are useful for checking whether the system handles ambiguity well, but they should not be the main graded questions because there is no single exact answer.

| # | Question | Expected response behavior | Why it is vague |
| --- | --- | --- | --- |
| V1 | What are the best ProPresenter features for Sunday service? | The system should avoid ranking features as universally "best." It can mention common documented tools such as Looks, Stage Screens, Bibles, Timers, Messages, Props, Macros, and Audio Routing, then ask what workflow the user is trying to improve. | "Best" depends on the church's setup, operator role, and service needs. |
| V2 | How do I fix my screens? | The system should ask whether the issue is audience output, stage display, screen configuration, Looks, or a timer/message issue. It may suggest checking configured screens and whether Audience/Stage outputs are toggled on, but should not pretend to know the exact fix. | "Screens" could refer to audience screens, stage screens, Looks, layouts, outputs, or physical displays. |
| V3 | How should I set up lyrics? | The system should ask whether the user means normal auditorium lyrics, lower thirds, themes, Bible text, or different content on different screens. It may point to Themes and Looks as likely areas. | "Lyrics setup" is broad and may involve formatting, lower thirds, screens, themes, or presentation creation. |
| V4 | Why is my audio not working? | The system should ask what kind of audio is failing: media playback, audio input routing, output routing, SDI/NDI audio, or device selection. It can suggest checking Audio Preferences and Channel Routing but should keep the answer conditional. | Audio failure has many possible causes, and the documents only cover routing concepts, not every troubleshooting case. |
| V5 | How do I make ProPresenter easier for volunteers? | The system should give a scoped answer based on documented features: playlist templates, macros, clear stage layouts, themes, and show controls. It should say the docs do not provide a full volunteer training plan and ask what role the volunteers perform. | The corpus has feature documentation, not a complete volunteer onboarding curriculum. |

## Unrelated or Out-of-Scope Questions

These should test grounded generation. The system should not invent answers or use general world knowledge when the answer is not supported by retrieved ProPresenter documents.

| # | Question | Expected response behavior | Why it is out of scope |
| --- | --- | --- | --- |
| U1 | What is the best restaurant near my church for lunch after service? | The system should say the available ProPresenter documents do not contain restaurant recommendations and cannot answer from the provided sources. | The corpus is about ProPresenter, not local restaurants. |
| U2 | How do I configure Ableton Live tracks for worship playback? | The system should say the current sources do not cover Ableton Live setup. It may mention that the ProPresenter audio documents cover routing inside ProPresenter only. | Ableton is outside the ProPresenter source set. |
| U3 | What camera should we buy for livestreaming? | The system should say camera buying recommendations are not covered by the retrieved documents. | The corpus does not include livestream camera purchasing guidance. |
| U4 | Can you write a sermon on Romans 8? | The system should refuse to treat the ProPresenter Bible tool as sermon-writing source material. It can say the documents explain how to search and display Bible passages, not how to write sermons. | This is a content-generation request unrelated to ProPresenter operation. |
| U5 | What changed in the latest version of ProPresenter? | The system should say the current documents do not include release notes or current version changes unless a release-note source has been added. | Version changes are time-sensitive and not represented in the current corpus. |

## Recommended Final Five for `planning.md`

These five questions give a good spread across retrieval challenges: shortcuts, Looks, timers, Bibles, and audio routing. They are all specific enough to grade.

| # | Question | Expected answer |
| --- | --- | --- |
| 1 | How do I open the Stage Layout editor in ProPresenter, and what shortcut can I use on Mac and Windows? | Open the Stage Layout editor from `Screens > Edit Layouts`. The shortcut is `Command+4` on Mac or `Control+4` on Windows. |
| 2 | If my lower-thirds lyrics look different from the main auditorium lyrics, where should I check first? | Check the Looks window, especially the alternate theme selected for the Presentation layer on the lower-thirds screen. If lyrics are unexpectedly different, make sure an alternate theme is not applied next to `Presentation` for that screen. |
| 3 | Why should I start a timer from a Header or from Timers instead of with a slide action in a looping announcement presentation? | Starting the timer from a Header or from Timers prevents the clock from resetting every time the looping slide is selected. Slide timer actions fire each time the slide is selected, so they are not recommended for an active slide in a looping presentation. |
| 4 | What does the `Break on New Verse` Bible slide option do, and when is `Verse References` available? | `Break on New Verse` creates new slides for each verse in a passage. `Verse References` is only available when `Break on New Verse` is selected. |
| 5 | In the Audio Routing window, what do the `M`, `S`, and `T` buttons do? | `M` mutes a channel, `S` solos a channel, and `T` sends a tone to that channel. These can be used for troubleshooting audio signals. |

## Evaluation Rubric

For each specific question, grade two separate parts:

| Dimension | Accurate | Partially accurate | Inaccurate |
| --- | --- | --- | --- |
| Retrieval quality | Retrieved the source chunk that contains the answer, plus any helpful neighboring context. | Retrieved a related ProPresenter chunk but missed at least one key detail or source. | Retrieved unrelated chunks or no useful ProPresenter context. |
| Response accuracy | Answer matches the expected answer and does not add unsupported claims. | Answer is mostly right but incomplete, imprecise, or missing an important condition. | Answer contradicts the documents, invents information, or answers a different question. |

For vague questions, the ideal behavior is not necessarily a long answer. A good response should identify the ambiguity, offer the most relevant documented areas, and ask a clarifying question when needed.

For unrelated questions, the ideal behavior is a grounded refusal or limitation statement. The system should explain that the current ProPresenter source set does not contain enough information to answer, instead of filling the gap with general knowledge.

## Notes for Pipeline Testing

When the pipeline is implemented, run the recommended final five first. After that, run a few vague and unrelated prompts to check grounding behavior.

Useful signals to record:

- Which chunks were retrieved.
- Whether the top chunk contained the expected answer.
- Whether the generated response cited or named the correct source.
- Whether the model answered only from retrieved context.
- Whether vague prompts produced clarification instead of overconfident answers.
- Whether unrelated prompts were rejected as out of scope.
