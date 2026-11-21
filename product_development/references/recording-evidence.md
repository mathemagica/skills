# Working With Recordings And Screen Content

How to turn an authorized screen recording into evidence without inventing what
was on screen. Read the [workflow contract](workflow-contract.md) first: consent,
approved processing locations and handling scope come before any processing.

## Transcript

- Transcribe only with tools and destinations the owner approved. Local files do
  not mean local processing; check where a tool sends audio.
- Keep timestamps and speaker labels where the tool supports them. Note audio
  quality problems and uncertain passages instead of smoothing them over.
- A transcript is evidence of what was said, not of what was shown.

## Screen Content

If the agent can inspect video or images, look at the screen at the moments that
matter instead of relying on narration. Useful moments:

- Points where the transcript signals a demonstration ("let me show you," "see
  this column," "here's where it breaks").
- Scene changes, such as switching applications or opening a new screen.
- Any moment the owner refers back to later.

With an authorized local tool such as ffmpeg, for example:

Run these only after confirming ffmpeg is available, from the agreed private
workspace. Create a private `frames/` directory first. Extract only the selected
moments needed for discovery, not every frame of the recording. The scene-change
command is an optional alternative; it may produce many frames. Limit it to a
relevant clip or use explicit timestamps when volume is uncertain. Retain the
`showinfo` log if using scene-change frames so filenames can be mapped to source
timestamps; sequence numbers are not timestamps.

```sh
# One frame at a timestamp the transcript points to
ffmpeg -ss 00:12:30 -i recording.mp4 -frames:v 1 frames/t001230.png

# Frames at scene changes, keeping each frame's timestamp in the log
ffmpeg -i recording.mp4 -vf "select='gt(scene,0.3)',showinfo" -fps_mode vfr frames/scene_%04d.png
```

Adjust the scene threshold to the recording. Older ffmpeg versions use `-vsync vfr`
instead of `-fps_mode vfr`. Keep frames in the private project workspace.

Record each frame as evidence with its timestamp and a short factual description
of what it shows. Describe, don't interpret: "spreadsheet with columns Name,
Shift, Status; three rows highlighted red" rather than "the owner needs a
dashboard." Interpretation goes in the discovery brief, labeled as inference.

## When Visual Evidence Is Unavailable

If the agent cannot inspect the video, say so in the discovery brief and work
from the transcript. Ask the owner for screenshots or a short walkthrough of the
key screens rather than guessing. Never describe screens that were not inspected.

## Privacy

Screens often show more than intended: other people's names, customer records,
email, credentials. Do not copy such details into briefs, scopes or PRDs. Note
"sensitive data visible at 08:15, not transcribed" where relevant. Do not upload
unredacted frames to an image/AI service unless that sensitive data and destination
are authorized; permission to extract locally is not permission to transmit.
Follow the agreed retention and deletion policy. If none exists, ask before
deleting source material or derived evidence. Prefer redacted working copies;
do not overwrite originals without permission. Never put recordings, frames or
transcripts in a public repository.

## Third-Party Software On Screen

Owners often demonstrate an existing product's gaps. Record the gap and the
workaround, not the product's interface, wording or assets. Do not copy another
product's design, code, content or branding into the new product without
permission. "Their tool can't hold a waitlist" is evidence; their screen layout
is not a specification.
