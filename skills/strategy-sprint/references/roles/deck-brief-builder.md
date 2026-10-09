# Deck Brief Builder

**Stage:** Communicate · **Role 24 of 24** · **Output:** `strategy-output/24-deck-brief-builder.md`

## Job

Turn the approved story into a production-ready slide brief any tool can build from: action titles, one message per slide, exhibit specs, source notes, appendix and speaker cues.

## Use when

- The recommendation is approved and needs a board, executive or committee deck.

## Skip when

- No Gate 3 approval yet.

## Needs (named, versioned inputs)

- Approved story and memo
- Ledger
- Audience, length and template constraints

## Method

1. Use `assets/templates/deck-brief.md`.
2. Write the action-title spine first: read the titles alone and the argument should hold.
3. One message per slide. For each: title, key point, exhibit type and the exact data with source IDs, caveat, and speaker cue.
4. Put proof in the appendix: method, sensitivities, source list.
5. Only approved claims. Mark the review status on the brief.
6. Offer the build path: a Slides artifact, a .pptx, or the user's own slide tool.

## Output sections

- Deck brief: audience and decision, title spine, slide-by-slide spec, appendix list, source notes
- Handoff block (`assets/templates/handoff.md`)

## Checks before handoff

- [ ] Titles alone tell the story.
- [ ] Every exhibit cites source IDs.
- [ ] No new claims.
- [ ] Every material claim labeled per `references/operating-rules.md`

## Stop and escalate if

- The deck needs a claim that is not approved.
- Any action outside the read-only default is needed.

## Hands to

The user's chosen slide tool, or `insight-storyteller` for a shorter version.
