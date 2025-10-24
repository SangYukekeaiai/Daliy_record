#!/usr/bin/env python3
import time
import argparse
import pyttsx3
import sys
import platform

def say(engine, text, volume=1.0, rate=None, voice=None):
    if engine is None:
        # Fallback: print + terminal bell
        print(text)
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.Beep(880, 300)
            else:
                sys.stdout.write("\a"); sys.stdout.flush()
        except Exception:
            pass
        return
    if volume is not None:
        engine.setProperty('volume', max(0.0, min(1.0, volume)))
    if rate is not None:
        engine.setProperty('rate', rate)
    if voice is not None:
        # try to pick a voice that contains the substring (case-insensitive)
        for v in engine.getProperty("voices"):
            if voice.lower() in (v.name.lower() + " " + str(v.id).lower()):
                engine.setProperty("voice", v.id)
                break
    engine.say(text)
    engine.runAndWait()

def fmt_mmss(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"

def countdown(total_seconds, label):
    start = time.time()
    end = start + total_seconds
    try:
        while True:
            left = end - time.time()
            if left <= 0:
                break
            # One-line live timer
            sys.stdout.write(f"\r[{label}] {fmt_mmss(left)} remaining ")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.stdout.write("\nInterrupted. Exiting.\n")
        sys.stdout.flush()
        raise
    finally:
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()

def run_cycle(engine, work_s, short_s, long_s, cycles, long_every, vol, rate, voice):
    for i in range(1, cycles + 1):
        # Work
        say(engine, f"Focus session {i} started. Time to work!", vol, rate, voice)
        countdown(work_s, f"WORK {i}/{cycles}")
        say(engine, "Work session finished. Time to rest!", vol, rate, voice)

        # Decide break length
        use_long = (long_s > 0) and (i % long_every == 0) and (i != cycles)
        if i == cycles:
            break  # done—no break after last cycle
        if use_long:
            say(engine, "Long break begins.", vol, rate, voice)
            countdown(long_s, f"LONG BREAK ({i}/{cycles})")
        else:
            say(engine, "Short break begins.", vol, rate, voice)
            countdown(short_s, f"SHORT BREAK ({i}/{cycles})")

        say(engine, "Break over. Start working!", vol, rate, voice)

def main():
    p = argparse.ArgumentParser(
        description="Pomodoro timer with spoken alerts (offline TTS).")
    p.add_argument("--work", type=int, default=25, help="Work minutes (default: 25)")
    p.add_argument("--short", type=int, default=5, help="Short break minutes (default: 5)")
    p.add_argument("--long", type=int, default=15, help="Long break minutes (default: 15)")
    p.add_argument("--cycles", type=int, default=4, help="Number of work sessions (default: 4)")
    p.add_argument("--long-every", type=int, default=4, help="Use a long break every N sessions (default: 4)")
    p.add_argument("--volume", type=float, default=1.0, help="Voice volume 0.0–1.0 (default: 1.0)")
    p.add_argument("--rate", type=int, default=None, help="Speech rate (words/min; engine-dependent)")
    p.add_argument("--voice", type=str, default=None, help="Voice name substring (e.g., 'english', 'female', 'zho')")
    p.add_argument("--silent", action="store_true", help="Disable TTS; use bell + text only")
    args = p.parse_args()

    engine = None
    if not args.silent:
        try:
            engine = pyttsx3.init()
        except Exception:
            print("Warning: pyttsx3 init failed; running in silent mode.", file=sys.stderr)

    work_s  = max(1, args.work)  * 60
    short_s = max(0, args.short) * 60
    long_s  = max(0, args.long)  * 60

    try:
        run_cycle(engine, work_s, short_s, long_s, args.cycles, max(1, args.long_every),
                  args.volume, args.rate, args.voice)
        say(engine, "All sessions complete. Great job! Remember to stretch and hydrate.", args.volume, args.rate, args.voice)
    except KeyboardInterrupt:
        say(engine, "Timer stopped. See you next time.", args.volume if engine else None, args.rate, args.voice)

if __name__ == "__main__":
    main()
